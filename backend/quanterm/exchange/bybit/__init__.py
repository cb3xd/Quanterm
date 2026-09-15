from quanterm.exchange.base import Exchange
from quanterm.exchange.bybit.api import BybitAPI
from quanterm.exchange.bybit.ws import BybitWebsocket
from quanterm.exchange.constants import ExchangeID
from quanterm.registries.exchange_registry import register_exchange


@register_exchange(ExchangeID.bybit)
class Bybit(Exchange):
    def __init__(self):
        super().__init__(ws=BybitWebsocket(), api=BybitAPI())
