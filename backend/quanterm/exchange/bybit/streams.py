from enum import StrEnum


class BybitMarketStreams(StrEnum):
    TRADES = "publicTrade"
    TICKER = "tickers"
    KLINE = "kline"
