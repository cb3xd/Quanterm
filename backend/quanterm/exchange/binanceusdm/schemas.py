from typing import Any, Callable

from msgspec import Struct, field, json
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.symbol_registry import symbol_registry
from quanterm.schemas import (
    AggregateMarketDataPacket,
    KlinePacket,
    MarketDataPacket,
    TradePacket,
)
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
    )


class BinanceMarketData(Struct, tag_field="e", tag="markPriceUpdate"):
    event_time: int = field(name="E")
    symbol: str = field(name="s")
    mark_price: str = field(name="p")
    average_price: str = field(name="ap")
    index_price: str = field(name="i")
    funding_rate: str = field(name="r")
    next_funding_time: int = field(name="T")
    market_type: int = field(name="st")


def map_market_data(packets: list[BinanceMarketData]):
    market_data: dict[str, MarketDataPacket] = {}
    for pair_data in packets:
        if pair_data.market_type == 2:
            continue
        dashed_symbol = symbol_registry.get_dash_format(pair_data.symbol.lower())
        if dashed_symbol is None:
            continue
        market_data[dashed_symbol] = MarketDataPacket(
            event_time=pair_data.event_time,
            market_price=pair_data.mark_price,
            average_price=pair_data.average_price,
            index_price=pair_data.index_price,
            funding_rate=pair_data.funding_rate,
            next_funding_time=pair_data.next_funding_time,
        )

    return AggregateMarketDataPacket(
        exchange_id=ExchangeID.binanceusdm, market_data=market_data
    )


def list_mapper(packets: list):
    if not packets:
        return
    packet_type = type(packets[0])
    packet_mapper = PACKET_MAPPERS.get(packet_type)

    if packet_mapper is None:
        return

    mapped_packet = packet_mapper(packets)
    return mapped_packet


StreamRouterType = BinanceTradePacket | BinanceKlinePacket | list[BinanceMarketData]

WS_DECODER = json.Decoder(StreamRouterType)

PACKET_MAPPERS: dict[Any, Callable] = {
    BinanceTradePacket: map_trade,
    BinanceKlinePacket: map_kline,
    list: list_mapper,
    BinanceMarketData: map_market_data,
}
