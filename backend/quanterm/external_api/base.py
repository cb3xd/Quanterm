from abc import ABC, abstractmethod

import aiohttp
import msgspec
from msgspec import Struct
from msgspec.json import Decoder

from quanterm.types import KlineIntervals


class BaseAPI(ABC):
    def __init__(
        self,
        url: str,
    ) -> None:
        self.url: str = url
        self._encoder = msgspec.json.Encoder()
        self._session: aiohttp.ClientSession | None = None
        self._kline_decoder: Decoder
        self._orderbook_snapshot_decoder: Decoder

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    @abstractmethod
    async def fetch_symbols(self) -> set[str]: ...

    @abstractmethod
    async def fetch_exchange_info(self) -> Struct: ...

    @abstractmethod
    async def fetch_kline(self, symbol: str, interval: KlineIntervals) -> Struct: ...

    @abstractmethod
    async def fetch_orderbook_snapshot(self, symbol: str) -> Struct: ...
