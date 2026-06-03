from msgspec import Struct
from typing import Type, Callable

from quanterm.types import KlineIntervals, StreamTypes


class StreamEvent(Struct):
    event_id: str


class TradePacket(Struct, frozen=False):
    exchange_id: str
    symbol: str
    price: str
    size: str
    normal_size: str
    timestamp: int
    is_buy: bool
    event_id: str


class KlinePacket(Struct, frozen=False):
    exchange_id: str
    open_time: int
    close_time: int
    symbol: str
    interval: str
    open_price: str
    close_price: str
    high_price: str
    low_price: str
    volume: str
    trades: int
    is_closed: bool
    quote_volume: str
    taker_buy_base_volume: str
    taker_buy_quote_volume: str
    event_id: str


class FastApiSubscribePacket(Struct, omit_defaults=True):
    event_id: str
    symbol: str
    stream_type: StreamTypes
    interval: KlineIntervals | None = None


class StreamDefinition:
    def __init__(self, schema: Type[Struct], mapper: Callable) -> None:
        self.schema = schema
        self.mapper = mapper
