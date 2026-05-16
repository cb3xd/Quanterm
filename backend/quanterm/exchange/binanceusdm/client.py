from typing import override
from quanterm.bus.base import EventBus
from quanterm.exchange.base import Exchange
import quanterm.exchange.binanceusdm.external_api as external_api
from quanterm.exchange.binanceusdm.ws import BinanceWebsocket


class BinanceUSDM(Exchange):
    @override
    async def get_symbols(self) -> set[str]:
        symbols = await external_api.fetch_symbols()
        return symbols

    @override
    async def ws_instance(self, event_bus: EventBus) -> BinanceWebsocket:
        return BinanceWebsocket(event_bus)
