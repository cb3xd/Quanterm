from msgspec import Struct, field, json
from quanterm.bus.utils import generate_event_id
from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import KlinePacket, StreamEvent, TradePacket
from quanterm.types import KlineIntervals, StreamTypes


class BinanceStreamEvent(StreamEvent, tag_field="e"):
    event_id: str


class BinanceTradePacket(BinanceStreamEvent, tag="aggTrade", kw_only=True):
    symbol: str = field(name="s")
    event_time: int = field(name="E")
    price: str = field(name="p")
    size: str = field(name="q")
    is_buy: bool = field(name="m")
    exchange_id: ExchangeID = ExchangeID.binanceusdm
    stream_type: StreamTypes = StreamTypes.trade_stream
    event_id: str = ""
    data: TradePacket | None = None

    def __post_init__(self):
        self.event_id = generate_event_id(
            ExchangeID.binanceusdm, self.symbol, self.stream_type, extra=None
        )
        self.data = TradePacket(
            exchange_id=ExchangeID.binanceusdm,
            symbol=self.symbol,
            price=self.price,
            size=self.size,
            event_time=self.event_time,
            event_id=self.event_id,
            is_buy=self.is_buy,
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
    base_asset_volume: str = field(name="v")
    taker_buy_base_asset_volume: str = field(name="V")
    taker_buy_quote_asset_volume: str = field(name="Q")


class BinanceKlinePacket(BinanceStreamEvent, tag="kline", kw_only=True):
    symbol: str = field(name="s")
    event_time: int = field(name="E")
    kline: BinanceKlineData = field(name="k")
    stream_type: StreamTypes = StreamTypes.kline_stream
    event_id: str = ""
    data: KlinePacket | None = None

    def __post_init__(self):
        self.event_id = generate_event_id(
            exchange_id=ExchangeID.binanceusdm,
            symbol=self.symbol,
            event_type=self.stream_type,
            extra=self.kline.interval,
        )
        self.data = KlinePacket(
            exchange_id=ExchangeID.binanceusdm,
            open_time=self.kline.kline_start_time,
            close_time=self.kline.kline_close_time,
            symbol=self.symbol,
            interval=self.kline.interval,
            open_price=self.kline.open_price,
            high_price=self.kline.high_price,
            low_price=self.kline.low_price,
            close_price=self.kline.close_price,
            volume=self.kline.base_asset_volume,
            trade_count=self.kline.trade_count,
            is_closed=self.kline.is_closed,
            taker_buy_base_volume=self.kline.taker_buy_base_asset_volume,
            taker_buy_quote_volume=self.kline.taker_buy_quote_asset_volume,
            event_id=self.event_id,
        )


StreamRouterType = BinanceTradePacket | BinanceKlinePacket

WS_DECODER = json.Decoder(StreamRouterType)
