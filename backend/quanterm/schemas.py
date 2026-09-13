from msgspec import Struct


class TradePacket(Struct):
    exchange_id: str
    symbol: str
    price: str
    size: str
    event_time: int
    is_buy: bool
    event_id: str | None = None


class KlinePacket(Struct):
    exchange_id: str
    event_time: int
    open_time: int
    close_time: int
    symbol: str
    interval: str
    open_price: str
    close_price: str
    high_price: str
    low_price: str
    volume: str
    is_closed: bool
    trade_count: int | None = None
    taker_buy_base_volume: str | None = None
    taker_buy_quote_volume: str | None = None
    event_id: str | None = None


class MarketDataPacket(Struct):
    event_time: int
    market_price: str
    average_price: str
    index_price: str
    funding_rate: str
    next_funding_time: int


class AggregateMarketDataPacket(Struct):
    exchange_id: str
    market_data: dict[str, MarketDataPacket]
    event_id: str | None = None
