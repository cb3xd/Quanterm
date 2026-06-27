from abc import ABC
from quanterm.external_api.base import BaseAPI
from quanterm.websocket.base import BaseWS


class Exchange(ABC):
    def __init__(self, ws: BaseWS, api: BaseAPI) -> None:
        self.ws = ws
        self.api = api

    async def connect_websocket(self):
        await self.ws.connect()

    async def close(self):
        await self.api.close()
