from abc import ABC, abstractmethod
import aiohttp
from msgspec import Struct
from msgspec.json import Decoder
from quanterm.types import KlineIntervals
from quanterm.websocket import JSON_ENCODER


class BaseAPI(ABC):
    def __init__(
        self,
        url: str,
    ) -> None:
        self.url: str = url
        self._encoder = JSON_ENCODER
        self._session: aiohttp.ClientSession | None = None
        self._decoder = Decoder()

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
