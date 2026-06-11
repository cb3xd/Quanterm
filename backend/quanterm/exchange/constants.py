from enum import StrEnum

from quanterm.tcp.byte_mappings import register_byte_map


@register_byte_map
class ExchangeID(StrEnum):
    binanceusdm = "binanceusdm"
    bybit = "bybit"
    mexc = "mexc"
    deribit = "deribit"
