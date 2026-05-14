import asyncio
from abc import ABC, abstractmethod
from websockets import ClientConnection, ConnectionClosed, Data
from quanterm.bus.base import EventBus


class BaseWS(ABC):
    def __init__(self, event_bus: EventBus) -> None:
        self.active_streams: set[str] = set()
        self.uri: str = ""
        self.websocket: ClientConnection | None = None
        self._watch_task: asyncio.Task[None] | None = None
        self.event_bus: EventBus = event_bus

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def subscribe(self, symbols: list[str]) -> None: ...

    @abstractmethod
    async def _on_message(self, raw: Data) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    async def _listen(self) -> None:
        if self.websocket is None:
            print("Connect first")
            return
        while True:
            try:
                async for msg in self.websocket:
                    await self._on_message(msg)
            except ConnectionClosed:
                print("Reconnecting..")
                await asyncio.sleep(1)
                await self.connect()
