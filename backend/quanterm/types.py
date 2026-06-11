from enum import StrEnum

from quanterm.tcp.byte_mappings import register_byte_map


@register_byte_map
class StreamTypes(StrEnum):
    trade_stream = "trade_stream"
    kline_stream = "kline_stream"


@register_byte_map
class KlineIntervals(StrEnum):
    minute = "1m"
    minute_3 = "3m"
    minute_5 = "5m"
    minute_15 = "15m"
    minute_30 = "30m"
    hourly = "1h"
    hour_2 = "2h"
    hour_4 = "4h"
    hour_6 = "6h"
    hour_12 = "12h"
    daily = "1d"
    day_3 = "3d"
    weekly = "1w"
    monthly = "1m"
