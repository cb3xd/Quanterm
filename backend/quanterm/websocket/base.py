import asyncio
import logging
from abc import ABC, abstractmethod
from websockets import ClientConnection, ConnectionClosed
import websockets
from quanterm.bus.base import EventBus, get_event_bus
from quanterm.exchange.constants import ExchangeID
from quanterm.registries import STREAM_REGISTRY
from quanterm.websocket import JSON_ENCODER

uvicorn_logger = logging.getLogger("uvicorn")

logger: logging.Logger
if uvicorn_logger.hasHandlers():
    logger = uvicorn_logger
else:
    logger = logging.getLogger("test")

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s] - %(message)s"))
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.info("Testing environment logger enabled")


class BaseWS(ABC):
    def __init__(self) -> None:
        self._active_streams: set[str] = set()
        self._stream_registry = STREAM_REGISTRY
        self._uri: str
        self._websocket: ClientConnection | None = None
        self._watch_task: asyncio.Task[None] | None = None
        self._event_bus: EventBus = get_event_bus()
        self._max_streams: int
        self._encoder = JSON_ENCODER
        self._exchange_id: ExchangeID
        self._max_delay: float = 60.0
        self._reconnect_delay: float = 1.0

    @abstractmethod
    async def _subscribe(self, events: set[str]) -> None: ...
    async def subscribe(self, events: set[str]) -> None:
        if self._active_streams.__len__() == self._max_streams:
            logger.warning(f"{self._exchange_id}: max streams reached.")
            return
        if self._websocket is None:
            logger.warning(f"{self._exchange_id}: connect first.")
            return

        logger.info(f"{self._exchange_id}: subscribing to {events}")
        await self._subscribe(events)

    @abstractmethod
    async def _unsubscribe(self, events: set[str]) -> None: ...
    async def unsubscribe(self, events: set[str]) -> None:
        if self._active_streams == 0:
            logger.warning(
                f"{self._exchange_id}: no active streams to unsubscribe from."
            )
            return
        if self._websocket is None:
            logger.warning(f"{self._exchange_id}: connect first.")
            return

        logger.info(f"{self._exchange_id}: unsubscribing to {events}")
        await self._unsubscribe(events)

    @abstractmethod
    async def _on_message(self, raw: bytes) -> None: ...

    async def connect(self) -> None:
        logger.info(f"{self._exchange_id}: connecting")
        delay = self._reconnect_delay
        try:
            self._websocket = await websockets.connect(
                self._uri, ping_interval=20, ping_timeout=10
            )
            self._reconnect_delay = 1.0
            self._watch_task = asyncio.create_task(self._listen())
            logger.info(f"{self._exchange_id}: connected")
        except (TimeoutError, OSError, websockets.WebSocketException) as e:
            logger.error(f"{self._exchange_id}: {e}")
            logger.error(f"{self._exchange_id}: reconnecting in {delay}s")
            await asyncio.sleep(delay)
            self._reconnect_delay = min(delay * 2, self._max_delay)
            await self.connect()

    async def disconnect(self) -> None:
        logger.info(f"{self._exchange_id}: disconnecting")
        if self._watch_task:
            _ = self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass
            self._watch_task = None

        if self._websocket:
            await self._websocket.close()
            self._websocket = None
        self._active_streams.clear()
        logger.info(f"{self._exchange_id}: disconnected")

    async def _listen(self) -> None:
        if self._websocket is None:
            return

        while True:
            try:
                msg = await self._websocket.recv(decode=False)
                asyncio.create_task(self._on_message(msg))
            except ConnectionClosed as e:
                code = e.rcvd.code if e.rcvd else e.sent.code if e.sent else 1006
                reason = (
                    e.rcvd.reason if e.rcvd else e.sent.reason if e.sent else "unknown"
                )
                logger.warning("WS closed %s: %s %s", self._uri, code, reason)
                await self.disconnect()
                return
