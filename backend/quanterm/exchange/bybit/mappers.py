from typing import Any, Callable

import msgspec

from quanterm.exchange.bybit.ws_schemas import BybitTradePacket
from quanterm.schemas import TradePacket


def map_trade(packet: list[BybitTradePacket]):
    trades: list[TradePacket] = []
    for trade in packet:
        trades.append(
            TradePacket(
                symbol=trade.symbol,
                exchange_id=trade.exchange_id,
                price=trade.price,
                size=trade.size,
                event_time=trade.time_filled,
                is_buy=(trade.side_of_taker is "Buy"),
            )
        )

    return trades


StreamRouterType = list[BybitTradePacket]


PACKET_MAPPERS: dict[Any, Callable] = {BybitTradePacket: map_trade}
