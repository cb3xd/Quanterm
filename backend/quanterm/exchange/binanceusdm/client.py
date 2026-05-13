from typing import override
from quanterm.bus.base import EventBus
from quanterm.exchange.base import Exchange
import quanterm.exchange.binanceusdm.api as api
from quanterm.exchange.binanceusdm.ws import BinanceWebsocket


class BinanceUSDM(Exchange):
    @override
    async def get_symbols(self) -> set[str]:
        symbols = await api.fetch_symbols()
        return symbols

    @override
    def get_stream_id(self, symbol: str, stream_type: str) -> str:
        return f"{symbol.lower()}@{stream_type}"

    @override
    async def ws_instance(self, event_bus: EventBus) -> BinanceWebsocket:
        self.websocket = BinanceWebsocket(event_bus)
        return self.websocket
