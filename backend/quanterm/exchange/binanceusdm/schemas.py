import msgspec

from quanterm.bus.utils import generate_event_id
from quanterm.exchange.base import ExchangeID, StreamTypes, TradePacket


class BinanceTrade(msgspec.Struct):
    # {
    #   "e": "aggTrade",  // Event type
    #   "E": 123456789,   // Event time
    #   "s": "BTCUSDT",   // Symbol
    #   "a": 5933014,		  // Aggregate trade ID
    #   "p": "0.001",     // Price
    #   "q": "100",       // Quantity with all the market trades
    #   "nq": "100",      // Normal quantity without the trades involving RPI orders
    #   "f": 100,         // First trade ID
    #   "l": 105,         // Last trade ID
    #   "T": 123456785,   // Trade time
    #   "m": true,        // Is the buyer the market maker?
    #   }

    e: str
    E: int
    a: int
    s: str
    p: str
    q: str
    nq: str
    f: int
    l: int
    T: int
    m: bool


class Packet(msgspec.Struct):
    stream: str
    data: dict


def map_trade(trade: BinanceTrade) -> TradePacket:
    return TradePacket(
        exchange_id=ExchangeID.binanceusdm,
        symbol=trade.s,
        price=trade.p,
        size=trade.q,
        normal_size=trade.nq,
        timestamp=trade.T,
        maker=trade.m,
        event_id=generate_event_id(
            ExchangeID.binanceusdm, trade.s, StreamTypes.trade_stream
        ),
    )
