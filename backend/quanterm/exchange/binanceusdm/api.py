import logging
from typing import override

import aiohttp
from fastapi import HTTPException
import msgspec
from quanterm.exchange.binanceusdm.api_schemas import (
    Candle,
    ExchangeInfo,
    KlineData,
)
from quanterm.external_api.base import BaseAPI
from quanterm.types import KlineIntervals


class BinanceAPI(BaseAPI):
    def __init__(self) -> None:
        url = "https://fapi.binance.com/fapi/v1"
        super().__init__(url)

    @override
    async def fetch_symbols(self) -> set[str]:
        logging.getLogger("uvicorn").info("Fetching symbols")
        exchange_info = await self.fetch_exchange_info()
        symbols = set()
        for symbol in exchange_info.symbols:
            symbols.add(f"{symbol.base_asset.lower()}-{symbol.quote_asset.lower()}")
        return symbols

    @override
    async def fetch_exchange_info(self):
        session = await self._get_session()
        async with session.get(f"{self.url}/exchangeInfo") as r:
            r.raise_for_status()
            raw_bytes = await r.read()
            data = msgspec.json.decode(raw_bytes, type=ExchangeInfo)
            return data

    @override
    async def fetch_kline(self, symbol: str, interval: KlineIntervals):
        params = {"symbol": symbol.replace("-", "").upper(), "interval": interval}
        session = await self._get_session()
        async with session.get(f"{self.url}/klines", params=params) as r:
            try:
                r.raise_for_status()
            except Exception:
                raise HTTPException(r.status, detail=f"Invalid Symbol: {symbol}")
            raw_bytes = await r.read()
            klines = msgspec.json.decode(raw_bytes, type=list[Candle])

            return KlineData(symbol=symbol, interval=interval, candles=klines)
