from typing import Callable

from msgspec import Struct, field, json
from quanterm.bus.utils import generate_event_id
from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import KlinePacket, TradePacket
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


def map_trade(packet: BinanceTradePacket):
    return TradePacket(
        symbol=packet.symbol,
        exchange_id=ExchangeID.binanceusdm,
        price=packet.price,
        size=packet.size,
        event_time=packet.event_time,
        is_buy=packet.is_buy,
        event_id=generate_event_id(
            ExchangeID.binanceusdm, packet.symbol.lower(), StreamTypes.trade_stream
        ),
    )


def map_kline(packet: BinanceKlinePacket):
    return KlinePacket(
        exchange_id=ExchangeID.binanceusdm,
        event_time=packet.event_time,
        symbol=packet.symbol,
        open_time=packet.kline.kline_start_time,
        close_time=packet.kline.kline_close_time,
        interval=packet.kline.interval,
        open_price=packet.kline.open_price,
        high_price=packet.kline.high_price,
        low_price=packet.kline.low_price,
        close_price=packet.kline.close_price,
        volume=packet.kline.base_asset_volume,
        trade_count=packet.kline.trade_count,
        is_closed=packet.kline.is_closed,
        taker_buy_base_volume=packet.kline.taker_buy_base_asset_volume,
        taker_buy_quote_volume=packet.kline.taker_buy_quote_asset_volume,
        event_id=generate_event_id(
            ExchangeID.binanceusdm,
            packet.symbol.lower(),
            StreamTypes.kline_stream,
            extra=packet.kline.interval,
        ),
    )


StreamRouterType = BinanceTradePacket | BinanceKlinePacket

WS_DECODER = json.Decoder(StreamRouterType)

PACKET_MAPPERS: dict[type[Struct], Callable] = {
    BinanceTradePacket: map_trade,
    BinanceKlinePacket: map_kline,
}
