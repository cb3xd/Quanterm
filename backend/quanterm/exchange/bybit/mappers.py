import logging
from typing import Any, Callable

import msgspec

from quanterm.exchange.bybit.streams import BybitMarketStreams
from quanterm.exchange.bybit.ws_schemas import BybitKlinePacket, BybitTradePacket
from quanterm.schemas import KlinePacket, TradePacket
from quanterm.types import KlineIntervals


_interval_map = {
    "D": KlineIntervals.daily,
    "720": KlineIntervals.hour_12,
    "360": KlineIntervals.hour_6,
    "240": KlineIntervals.hour_4,
    "120": KlineIntervals.hour_2,
    "60": KlineIntervals.hourly,
    "30": KlineIntervals.minute_30,
    "15": KlineIntervals.minute_15,
    "5": KlineIntervals.minute_5,
    "3": KlineIntervals.minute_3,
    "1": KlineIntervals.minute,
}


def map_list(packets: BybitEnvelope) -> list[msgspec.Struct]:
    result: list[msgspec.Struct] = []
    for packet in packets.data:
        mapper = PACKET_MAPPERS.get(packets.topic[0])
        logging.getLogger("test").debug(f"{__name__} - {mapper}:{packets.topic[0]}")
        if mapper is None:
            break
        formatted_data = mapper(packet, packets.topic[len(packets.topic) - 1])
        result.append(formatted_data)
    return result


def map_trade(trade: BybitTradePacket, symbol: str):
    if type(trade) is not BybitTradePacket:
        trade = msgspec.convert(trade, BybitTradePacket)
    return TradePacket(
        symbol=symbol,
        exchange_id=trade.exchange_id,
        price=trade.price,
        size=trade.size,
        event_time=trade.time_filled,
        is_buy=(trade.side_of_taker == "Buy"),
    )


def map_kline(kline: BybitKlinePacket, symbol: str):
    if type(kline) is not BybitKlinePacket:
        kline = msgspec.convert(kline, BybitKlinePacket)
    interval = _interval_map.get(kline.interval)
    print(interval, "BALLS")
    if interval is None:
        raise ValueError("Invalid interval")
    return KlinePacket(
        exchange_id=kline.exchange_id,
        event_time=kline.kline_start_time,
        open_time=kline.kline_start_time,
        close_time=kline.kline_close_time,
        symbol=symbol,
        interval=interval,
        open_price=kline.open_price,
        high_price=kline.high_price,
        close_price=kline.close_price,
        low_price=kline.low_price,
        volume=kline.volume,
        is_closed=kline.is_closed,
    )


class BybitEnvelope(msgspec.Struct):
    topic: list[str] | str
    data: list = msgspec.field(name="data")


PACKET_MAPPERS: dict[Any, Callable] = {
    BybitMarketStreams.TRADES: map_trade,
    list: map_list,
    BybitMarketStreams.KLINE: map_kline,
}
