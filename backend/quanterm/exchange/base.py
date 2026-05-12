from abc import ABC, abstractmethod
from typing import Callable, Type
from quanterm.websocket.base import BaseWS
import msgspec


class TradePacket(msgspec.Struct):
    exchange_id: int
    symbol_id: int
    price: float
    size: float
    ts: int


class StreamDefinition:
    def __init__(
        self, stream_id: str, schema: Type[msgspec.Struct], mapper: Callable
    ) -> None:
        self.stream_id = stream_id
        self.decoder = msgspec.json.Decoder(schema)
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
