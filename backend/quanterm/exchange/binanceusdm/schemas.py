from msgspec import Struct, field, json
from typing import Union

from quanterm.bus.utils import generate_event_id
from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import StreamEvent
from quanterm.types import KlineIntervals, StreamTypes


class BinanceStreamEvent(StreamEvent, tag_field="e"):
    event_id: str


class BinanceTradePacket(BinanceStreamEvent, tag="aggTrade", kw_only=True):
    symbol: str = field(name="s")
    event_time: int = field(name="E")
    price: str = field(name="p")
    quantity: str = field(name="q")
    is_buyer: bool = field(name="m")
    exchange_id: ExchangeID = ExchangeID.binanceusdm
    stream_type: StreamTypes = StreamTypes.trade_stream
    event_id: str = ""

    def __post_init__(self):
        self.event_id = generate_event_id(
            ExchangeID.binanceusdm, self.symbol, self.stream_type, extra=None
        )


class BinanceKlineData(Struct):
    kline_start_time: int = field(name="t")
    kline_close_time: int = field(name="T")
    interval: KlineIntervals = field(name="i")
    open_price: str = field(name="o")
    high_price: str = field(name="h")
    low_price: str = field(name="l")
    close_price: str = field(name="c")
    trade_count: int = field(name="n")
    is_closed: bool = field(name="x")
    taker_buy_base_asset_volume: str = field(name="V")
    taker_buy_quote_asset_volume: str = field(name="Q")


class BinanceKlinePacket(BinanceStreamEvent, tag="kline", kw_only=True):
    symbol: str = field(name="s")
    event_time: int = field(name="E")
    kline: BinanceKlineData = field(name="k")
    stream_type: StreamTypes = StreamTypes.kline_stream
    event_id: str = ""

    def __post_init__(self):
        self.event_id = generate_event_id(
            exchange_id=ExchangeID.binanceusdm,
            symbol=self.symbol,
            event_type=self.stream_type,
            extra=self.kline.interval,
        )


StreamRouterType = Union[BinanceTradePacket, BinanceKlinePacket]

WS_DECODER = json.Decoder(StreamRouterType)
