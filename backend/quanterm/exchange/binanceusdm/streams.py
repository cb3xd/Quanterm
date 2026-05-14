from enum import StrEnum
from quanterm.schemas import StreamDefinition
from quanterm.types import KlineIntervals
from quanterm.exchange.binanceusdm.schemas import (
    BinanceTrade,
    BinanceKline,
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

    KLINE_1M = "kline_1m"
    KLINE_3M = "kline_3m"
    KLINE_5M = "kline_5m"
    KLINE_15M = "kline_15m"
    KLINE_30M = "kline_30m"

    KLINE_1H = "kline_1h"
    KLINE_2H = "kline_2h"
    KLINE_4H = "kline_4h"
    KLINE_6H = "kline_6h"
    KLINE_8H = "kline_8h"
    KLINE_12H = "kline_12h"

    KLINE_1D = "kline_1d"
    KLINE_3D = "kline_3d"
    KLINE_1W = "kline_1w"
    KLINE_1M_MO = "kline_1M"  # Note: Capital 'M' denotes Month


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
            schema=BinanceKline,
            mapper=map_kline,
        )
