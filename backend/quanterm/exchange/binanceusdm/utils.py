from quanterm.exchange.binanceusdm.streams import MarketStreams
from quanterm.types import KlineIntervals, StreamTypes


stream_type_map = {
    StreamTypes.trade_stream: MarketStreams.TRADES,
    StreamTypes.kline_stream: MarketStreams.KLINE,
}


def get_stream_id(
    symbol: str, stream_type: StreamTypes, interval: KlineIntervals | None
) -> str | None:
    _stream_type = stream_type_map.get(stream_type)
    if _stream_type is None:
        print("(utils.py) Invalid stream type")
        return
    if interval:
        return f"{symbol}@{_stream_type}{interval}"
    else:
        return f"{symbol}@{_stream_type}"
