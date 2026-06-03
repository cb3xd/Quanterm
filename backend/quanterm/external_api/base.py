from abc import ABC, abstractmethod
from typing import Any
from msgspec import Struct
from msgspec.json import Decoder
from quanterm.types import KlineIntervals


class BaseAPI(ABC):
    def __init__(
        self,
        url: str,
        kline_decoder: Decoder[list[Any]],
    ) -> None:
        self.url: str = url
        self.kline_decoder = kline_decoder

    @abstractmethod
    async def fetch_symbols(self) -> set[str]: ...

    @abstractmethod
    async def fetch_exchange_info(self) -> Struct: ...

    @abstractmethod
    async def fetch_kline(self, symbol: str, interval: KlineIntervals) -> Struct: ...

    @abstractmethod
    async def fetch_price_change(self, symbol: str) -> Struct: ...
