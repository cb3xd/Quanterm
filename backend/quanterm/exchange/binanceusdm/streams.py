from enum import StrEnum
from quanterm.exchange.base import StreamDefinition
from quanterm.exchange.binanceusdm.schemas import BinanceTrade, map_trade


class MarketStreams(StrEnum):
    TRADES = "aggTrade"
    MARK_PRICE = "markPrice"
    MARK_PRICE_ALL = "!markPrice@arr"
    MINITICKER = "miniTicker"
    MINITICKER_ALL = "!miniTicker@arr"
    TICKER = "ticker"
    TICKER_ALL = "!ticker@arr"
    LIQUIDATIONS = "forceOrder"
    LIQUIDATIONS_ALL = "!forceOrder@arr"


class BinanceStreamDefinitions:
    streams = {
        "aggTrade": StreamDefinition(
            schema=BinanceTrade,
            mapper=map_trade,
        )
    }
