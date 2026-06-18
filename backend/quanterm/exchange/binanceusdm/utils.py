from quanterm.exchange.binanceusdm.streams import BinanceMarketStreams
from quanterm.types import KlineIntervals, StreamTypes


stream_type_map = {
    StreamTypes.trade_stream: BinanceMarketStreams.TRADES,
    StreamTypes.kline_stream: BinanceMarketStreams.KLINE,
}


def format_id(event_id: str) -> str:
    parts = event_id.split(".")
    symbol = parts[1].lower()
    stream_type = StreamTypes(parts[0])
    interval = None
    _stream_type = stream_type_map.get(stream_type)
    if _stream_type is None:
        raise ValueError(f"Invalid stream type {stream_type}")
    if parts.__len__() == 3:
        interval = KlineIntervals(parts[2])
        return f"{symbol}@{_stream_type}{interval}"
    else:
        event = f"{symbol}@{_stream_type}"
        return event
