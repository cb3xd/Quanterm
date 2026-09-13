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
