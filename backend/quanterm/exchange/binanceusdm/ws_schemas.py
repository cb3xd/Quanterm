from msgspec import Struct, field
from quanterm.exchange.constants import ExchangeID
from quanterm.types import KlineIntervals, StreamTypes


class BinanceTradePacket(Struct, tag_field="e", tag="aggTrade", kw_only=True):
    symbol: str = field(name="s")
    event_time: int = field(name="E")
    price: str = field(name="p")
    size: str = field(name="q")
    is_buy: bool = field(name="m")
    exchange_id: ExchangeID = ExchangeID.binanceusdm
    stream_type: StreamTypes = StreamTypes.trade_stream


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


class BinanceKlinePacket(Struct, tag_field="e", tag="kline", kw_only=True):
    symbol: str = field(name="s")
    event_time: int = field(name="E")
    kline: BinanceKlineData = field(name="k")
    stream_type: StreamTypes = StreamTypes.kline_stream


class BinanceMarketData(Struct, tag_field="e", tag="markPriceUpdate"):
    event_time: int = field(name="E")
    symbol: str = field(name="s")
    mark_price: str = field(name="p")
    average_price: str = field(name="ap")
    index_price: str = field(name="i")
    funding_rate: str = field(name="r")
    next_funding_time: int = field(name="T")
    market_type: int = field(name="st")
