from msgspec import Struct


class Packet(Struct, kw_only=True):
    exchange_id: str
    event_time: int
    event_id: str | None = None


class TradePacket(Packet, kw_only=True):
    exchange_id: str
    symbol: str
    price: str
    size: str
    event_time: int
    is_buy: bool


class KlinePacket(Packet, kw_only=True):
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


class MarketDataPacket(Packet, kw_only=True):
    event_time: int
    market_price: str
    average_price: str
    index_price: str
    funding_rate: str
    next_funding_time: int


class AggregateMarketDataPacket(Packet, kw_only=True):
    exchange_id: str
    market_data: dict[str, MarketDataPacket]
