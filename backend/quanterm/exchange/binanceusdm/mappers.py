from typing import Any, Callable

from msgspec import convert

from quanterm.exchange.binanceusdm.types import FuturesType
from quanterm.registries import SYMBOL_REGISTRY
from quanterm.exchange.binanceusdm.ws_schemas import (
    BinanceKlinePacket,
    BinanceTradePacket,
    BinanceMarketData,
)

from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import (
    KlinePacket,
    TradePacket,
    MarketDataPacket,
    AggregateMarketDataPacket,
)


def map_trade(packet: BinanceTradePacket) -> TradePacket:
    if type(packet) is not BinanceTradePacket:
        packet = convert(packet, BinanceTradePacket)
    return TradePacket(
        symbol=packet.symbol,
        exchange_id=ExchangeID.binanceusdm,
        price=packet.price,
        size=packet.size,
        event_time=packet.event_time,
        is_buy=packet.is_buy,
    )


def map_kline(packet: BinanceKlinePacket) -> KlinePacket:
    if type(packet) is not BinanceKlinePacket:
        packet = convert(packet, BinanceKlinePacket)
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


def map_market_data(packets: list[BinanceMarketData]) -> AggregateMarketDataPacket:
    if type(packets) is not list:
        raise RuntimeError(
            f"{__name__} map_market_data(): Packet of type {type(packets)} passed to data mapper is not a list."
        )
    market_data: dict[str, MarketDataPacket] = {}
    for pair_data in packets:
        if type(pair_data) is not BinanceMarketData:
            raise RuntimeError(
                f"{__name__} map_market_data(): pair data for {pair_data.symbol} is not of type BinanceMarketData."
            )
        if pair_data.market_type is not FuturesType.USDM:
            continue
        dashed_symbol = SYMBOL_REGISTRY.get_dash_format(pair_data.symbol.lower())
        if dashed_symbol is None:
            raise RuntimeError(
                f"{__name__} map_market_data(): {pair_data.symbol} is not registered."
            )
        market_data[dashed_symbol] = MarketDataPacket(
            event_time=pair_data.event_time,
            market_price=pair_data.mark_price,
            average_price=pair_data.average_price,
            index_price=pair_data.index_price,
            funding_rate=pair_data.funding_rate,
            next_funding_time=pair_data.next_funding_time,
            exchange_id=ExchangeID.binanceusdm,
        )

    return AggregateMarketDataPacket(
        exchange_id=ExchangeID.binanceusdm,
        data=market_data,
    )


def list_mapper(packets: list):
    if not packets:
        raise RuntimeError(f"{__name__} list_mapper(): Packets does not exist/is None.")

    packet_type = type(packets[0])
    packet_mapper = PACKET_MAPPERS.get(packet_type)

    if packet_mapper is None:
        raise RuntimeError(
            f"{__name__} list_mapper(): packet_mapper does not exist for packet type {packet_type}."
        )

    mapped_packet = packet_mapper(packets)
    return mapped_packet


StreamRouterType = BinanceTradePacket | BinanceKlinePacket | list[BinanceMarketData]

PACKET_MAPPERS: dict[Any, Callable] = {
    BinanceTradePacket: map_trade,
    BinanceKlinePacket: map_kline,
    list: list_mapper,
    BinanceMarketData: map_market_data,
}
