from abc import ABC
from quanterm.exchange.base_bridge import BaseBridge
from quanterm.external_api.base import BaseAPI
from quanterm.websocket.base import BaseWS


class Exchange(ABC):
    def __init__(self, ws: BaseWS, bridge: BaseBridge, api: BaseAPI) -> None:
        self.ws = ws
        self.bridge = bridge
        self.api = api

    async def connect_websocket(self):
        await self.ws.connect()
