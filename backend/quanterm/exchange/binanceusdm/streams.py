from enum import StrEnum


class BinanceMarketStreams(StrEnum):
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
