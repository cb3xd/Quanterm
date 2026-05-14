from abc import ABC, abstractmethod
from enum import IntEnum, StrEnum
from typing import Callable, Type
from msgspec import Struct
from quanterm.websocket.base import BaseWS


class TradePacket(Struct, frozen=False):
    exchange_id: int
    symbol: str
    price: str
    size: str
    normal_size: str
    timestamp: int
    maker: bool
    event_id: int


class StreamTypes(IntEnum):
    trade_stream = 1


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


class ExchangeID(IntEnum):
    binanceusdm = 1


class StreamDefinition:
    def __init__(self, schema: Type[Struct], mapper: Callable) -> None:
        self.schema = schema
        self.mapper = mapper


class Exchange(ABC):
    def __init__(self) -> None:
        self.websocket: BaseWS | None

    @abstractmethod
    async def get_symbols(self) -> set[str]: ...

    @abstractmethod
    def get_stream_id(self, symbol: str, stream_type: str) -> str: ...

    @abstractmethod
    async def ws_instance(self) -> BaseWS: ...
