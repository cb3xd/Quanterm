from quanterm.exchange.base import Exchange
from quanterm.exchange.binanceusdm.bridge import BinanceFapiWebsocketBridge
from quanterm.exchange.binanceusdm.external_api import BinanceAPI
from quanterm.exchange.binanceusdm.ws import BinanceWebsocket
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.registry import register_exchange


@register_exchange(ExchangeID.binanceusdm)
class BinanceUSDM(Exchange):
    def __init__(self, manager) -> None:
        ws = BinanceWebsocket()
        api = BinanceAPI()
        bridge = BinanceFapiWebsocketBridge(ws=ws)
        super().__init__(ws=ws, bridge=bridge, api=api)
