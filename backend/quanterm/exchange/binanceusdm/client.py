from typing import override
from quanterm.exchange.base import Exchange
from quanterm.exchange.binanceusdm.bridge import BinanceFapiWebsocketBridge
import quanterm.exchange.binanceusdm.external_api as external_api
from quanterm.exchange.binanceusdm.ws import BinanceWebsocket
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.registry import register_exchange


@register_exchange(ExchangeID.binanceusdm)
class BinanceUSDM(Exchange):
    def __init__(self, manager) -> None:
        ws = BinanceWebsocket()
        bridge = BinanceFapiWebsocketBridge(ws=ws)
        super().__init__(ws=ws, bridge=bridge)

    @override
    async def get_symbols(self) -> set[str]:
        symbols = await external_api.fetch_symbols()
        return symbols
