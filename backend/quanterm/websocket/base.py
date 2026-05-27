import asyncio
from abc import ABC, abstractmethod
from websockets import ClientConnection, ConnectionClosed
from quanterm.bus.base import EventBus, get_event_bus


class BaseWS(ABC):
    def __init__(self) -> None:
        self.active_streams: set[str] = set()
        self.uri: str = ""
        self.websocket: ClientConnection | None = None
        self._watch_task: asyncio.Task[None] | None = None
        self.event_bus: EventBus = get_event_bus()
        self.max_streams: int

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def subscribe(self, stream_id: str) -> None: ...

    @abstractmethod
    async def _on_message(self, raw: bytes) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    async def _listen(self) -> None:
        if self.websocket is None:
            print("Connect first")
            return

        while True:
            try:
                msg = await self.websocket.recv(decode=False)
                await self._on_message(msg)
            except ConnectionClosed:
                print("Reconnecting..")
                await asyncio.sleep(1)
                await self.connect()
