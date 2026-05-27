from enum import StrEnum
from quanterm.schemas import StreamDefinition
from quanterm.types import KlineIntervals
from quanterm.exchange.binanceusdm.schemas import (
    BinanceTrade,
    BinanceKlineEnvelope,
    map_trade,
    map_kline,
)


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
    KLINE = "kline_"


class BinanceStreamDefinitions:
    streams = {
        "aggTrade": StreamDefinition(
            schema=BinanceTrade,
            mapper=map_trade,
        )
    }

    # Add kline streams for each interval
    for interval in KlineIntervals:
        streams[f"kline_{interval.value}"] = StreamDefinition(
            schema=BinanceKlineEnvelope,
            mapper=map_kline,
        )
