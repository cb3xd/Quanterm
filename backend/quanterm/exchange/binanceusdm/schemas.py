from quanterm.bus.utils import generate_event_id
from quanterm.exchange.constants import ExchangeID
from quanterm.types import KlineIntervals, StreamTypes
from quanterm.schemas import TradePacket, KlinePacket
from msgspec import Struct


class BinanceTrade(Struct):
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


class BinanceKlineData(Struct):
    t: int
    T: int
    s: str
    i: KlineIntervals
    f: int
    L: int
    o: str
    h: str
    l: str
    c: str
    v: str
    n: int
    x: bool
    q: str
    V: str
    Q: str


class BinanceKlineEnvelope(Struct):
    # {
    #   "e": "kline",     // Event type
    #   "E": 1638747660000,   // Event time
    #   "s": "BTCUSDT",    // Symbol
    #   "k": {
    #     "t": 1638747660000, // Kline start time
    #     "T": 1638747719999, // Kline close time
    #     "s": "BTCUSDT",  // Symbol
    #     "i": "1m",      // Interval
    #     "f": 100,       // First trade ID
    #     "L": 200,       // Last trade ID
    #     "o": "0.0010",  // Open price
    #     "c": "0.0020",  // Close price
    #     "h": "0.0025",  // High price
    #     "l": "0.0015",  // Low price
    #     "v": "1000",    // Base asset volume
    #     "n": 100,       // Number of trades
    #     "x": false,     // Is this kline closed?
    #     "q": "1.0000",  // Quote asset volume
    #     "V": "500",     // Taker buy base asset volume
    #     "Q": "0.500",   // Taker buy quote asset volume
    #     "B": "123456"   // Ignore
    #   }
    # }

    e: str
    E: int
    s: str
    k: BinanceKlineData  # We'll parse the inner dict separately in the mapper


class Packet(Struct):
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
            ExchangeID.binanceusdm, trade.s, StreamTypes.trade_stream, None
        ),
    )


def map_kline(kl: BinanceKlineEnvelope) -> KlinePacket:
    kline_data = kl.k
    return KlinePacket(
        exchange_id=ExchangeID.binanceusdm,
        open_time=kline_data.t,
        close_time=kline_data.T,
        symbol=kl.s,
        interval=kline_data.i,
        open_price=kline_data.o,
        close_price=kline_data.c,
        high_price=kline_data.h,
        low_price=kline_data.l,
        volume=kline_data.v,
        trades=kline_data.n,
        is_closed=kline_data.x,
        quote_volume=kline_data.q,
        taker_buy_base_volume=kline_data.V,
        taker_buy_quote_volume=kline_data.Q,
        event_id=generate_event_id(
            ExchangeID.binanceusdm,
            kl.s,
            StreamTypes.kline_stream,
            extra=kline_data.i,
        ),
    )
