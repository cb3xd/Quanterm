from quanterm.exchange.base import Exchange
from quanterm.exchange.binanceusdm.api import BinanceAPI
from quanterm.exchange.binanceusdm.ws import BinanceWebsocket
from quanterm.exchange.constants import ExchangeID
from quanterm.registries.exchange_registry import register_exchange


@register_exchange(ExchangeID.binanceusdm)
class BinanceUSDM(Exchange):
    def __init__(self) -> None:
        ws = BinanceWebsocket()
        api = BinanceAPI()
        super().__init__(ws=ws, api=api)
