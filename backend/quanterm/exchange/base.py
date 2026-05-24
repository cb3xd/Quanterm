from abc import ABC, abstractmethod

from quanterm.exchange.base_bridge import BaseBridge
from quanterm.websocket.base import BaseWS


class Exchange(ABC):
    def __init__(self, ws: BaseWS, bridge: BaseBridge) -> None:
        self.ws = ws
        self.bridge = bridge

    @abstractmethod
    async def get_symbols(self) -> set[str]: ...

    async def connect_websocket(self):
        await self.ws.connect()
