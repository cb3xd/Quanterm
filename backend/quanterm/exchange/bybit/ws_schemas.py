from msgspec import Struct, field

from quanterm.exchange.constants import ExchangeID
from quanterm.types import StreamTypes


class BybitTradePacket(Struct):
    time_filled: int = field(name="T")
    symbol: str = field(name="s")
    side_of_taker: str = field(name="S")
    size: str = field(name="v")
    price: str = field(name="p")
    exchange_id: ExchangeID = ExchangeID.bybit
    stream_type: StreamTypes = StreamTypes.trade_stream


class BybitKlinePacket(Struct):
    kline_start_time: int = field(name="start")
    kline_close_time: int = field(name="end")
    interval: str = field(name="interval")
    open_price: str = field(name="open")
    high_price: str = field(name="high")
    low_price: str = field(name="low")
    close_price: str = field(name="close")
    volume: str = field(name="volume")
    is_closed: bool = field(name="confirm")
    exchange_id: ExchangeID = ExchangeID.bybit
