from quanterm.exchange.bybit.streams import BybitMarketStreams
from quanterm.types import KlineIntervals, StreamTypes

_stream_type_map = {
    StreamTypes.trade_stream: BybitMarketStreams.TRADES,
    StreamTypes.kline_stream: BybitMarketStreams.KLINE,
    StreamTypes.market_price: BybitMarketStreams.TICKER,
}
_interval_map = {
    KlineIntervals.daily: "D",
    KlineIntervals.hour_12: "720",
    KlineIntervals.hour_6: "360",
    KlineIntervals.hour_4: "240",
    KlineIntervals.hour_2: "120",
    KlineIntervals.hourly: "60",
    KlineIntervals.minute_30: "30",
    KlineIntervals.minute_15: "15",
    KlineIntervals.minute_5: "5",
    KlineIntervals.minute_3: "3",
    KlineIntervals.minute: "1",
}


# eid format: stream_type.pair-usdt.(optional)interval
def format_id(event_id: str) -> str:
    parts = event_id.split(".")

    stream_type = StreamTypes(parts[0])
    stream_type = _stream_type_map.get(stream_type)

    symbol = parts[1].replace("-", "").upper()
    interval = None

    if stream_type is None:
        raise ValueError(f"Invalid stream type {stream_type}")
    if parts.__len__() == 3:
        interval = _interval_map.get(KlineIntervals(parts[2]))
        if interval is None:
            raise ValueError(f"Unsupported interval {interval}")
        return f"{stream_type}.{interval}.{symbol}"
    else:
        return f"{stream_type}.{symbol}"
