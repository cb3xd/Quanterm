import asyncio
import logging
from abc import ABC, abstractmethod
from websockets import ClientConnection, ConnectionClosed
import websockets
from quanterm.bus.base import EventBus, get_event_bus
from quanterm.exchange.constants import ExchangeID
from quanterm.registries import STREAM_REGISTRY
from quanterm.websocket import JSON_ENCODER


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
        self._logger: logging.Logger
        self.init_logger()

    def init_logger(self) -> None:
        uvicorn_logger = logging.getLogger("uvicorn")

        if uvicorn_logger.hasHandlers():
            self._logger = uvicorn_logger
        else:
            self._logger = logging.getLogger("test")

            if not self._logger.handlers:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter("[%(levelname)s] - %(message)s"))
                self._logger.addHandler(handler)

            self._logger.setLevel(logging.INFO)
            self._logger.propagate = False
            self._logger.info("Testing environment logger enabled")

    @abstractmethod
    async def _subscribe(self, events: set[str]) -> None: ...
    async def subscribe(self, events: set[str]) -> None:
        if self._active_streams.__len__() == self._max_streams:
            self._logger.warning(f"{self._exchange_id}: max streams reached.")
            return
        if self._websocket is None:
            self._logger.warning(f"{self._exchange_id}: connect first.")
            return

        self._logger.info(
            f"{self._exchange_id}: subscribing to {events.__len__()} events"
        )
        await self._subscribe(events)
        self._logger.info(
            f"{self._exchange_id}: subscribed to {events.__len__()} events"
        )

    @abstractmethod
    async def _unsubscribe(self, events: set[str]) -> None: ...
    async def unsubscribe(self, events: set[str]) -> None:
        if self._active_streams == 0:
            self._logger.warning(
                f"{self._exchange_id}: no active streams to unsubscribe from."
            )
            return
        if self._websocket is None:
            self._logger.warning(f"{self._exchange_id}: connect first.")
            return

        self._logger.info(f"{self._exchange_id}: unsubscribing to {events}")
        await self._unsubscribe(events)

    @abstractmethod
    async def _on_message(self, raw: bytes) -> None: ...

    async def connect(self) -> None:
        self._logger.info(f"{self._exchange_id}: connecting")
        delay = self._reconnect_delay
        try:
            self._websocket = await websockets.connect(
                self._uri, ping_interval=20, ping_timeout=10
            )
            self._reconnect_delay = 1.0
            self._watch_task = asyncio.create_task(self._listen())
            self._logger.info(f"{self._exchange_id}: connected")
        except (TimeoutError, OSError, websockets.WebSocketException) as e:
            self._logger.error(f"{self._exchange_id}: {e}")
            self._logger.error(f"{self._exchange_id}: reconnecting in {delay}s")
            await asyncio.sleep(delay)
            self._reconnect_delay = min(delay * 2, self._max_delay)
            await self.connect()

    async def disconnect(self) -> None:
        self._logger.info(f"{self._exchange_id}: disconnecting")
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
        self._logger.info(f"{self._exchange_id}: disconnected")

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
                self._logger.warning("WS closed %s: %s %s", self._uri, code, reason)
                await self.disconnect()
                return
