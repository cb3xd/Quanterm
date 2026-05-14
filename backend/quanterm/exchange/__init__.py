from quanterm.exchange.base import Exchange
from quanterm.exchange.binanceusdm.client import BinanceUSDM


ExchangeRegistry: dict[str, Exchange] = {"binanceusdm": BinanceUSDM()}
