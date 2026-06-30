import asyncio
import logging
from abc import ABC, abstractmethod
from websockets import ClientConnection, ConnectionClosed
from quanterm.bus.base import EventBus, get_event_bus
from quanterm.exchange.stream_registry import get_stream_registry

logger = logging.getLogger("uvicorn")


class BaseWS(ABC):
    def __init__(self) -> None:
        self.active_streams: set[str] = set()
        self.stream_registry = get_stream_registry()
        self.uri: str = ""
        self.websocket: ClientConnection | None = None
        self._watch_task: asyncio.Task[None] | None = None
        self.event_bus: EventBus = get_event_bus()
        self.max_streams: int

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def subscribe(self, events: set[str]) -> None: ...

    @abstractmethod
    async def _on_message(self, raw: bytes) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    async def _listen(self) -> None:
        if self.websocket is None:
            return

        while True:
            try:
                msg = await self.websocket.recv(decode=False)
                asyncio.create_task(self._on_message(msg))
            except ConnectionClosed as e:
                code = e.rcvd.code if e.rcvd else e.sent.code if e.sent else 1006
                reason = (
                    e.rcvd.reason if e.rcvd else e.sent.reason if e.sent else "unknown"
                )
                logger.warning("WS closed %s: %s %s", self.uri, code, reason)
                await self.disconnect()
                return
