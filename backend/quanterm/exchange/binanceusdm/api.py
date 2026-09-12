from typing import override

import aiohttp
from fastapi import HTTPException
import msgspec
from msgspec.json import Encoder
from quanterm.exchange.binanceusdm.api_schemas import (
    Candle,
    ExchangeInfo,
    TickerPriceChange,
)
from quanterm.external_api.base import BaseAPI
from quanterm.types import KlineIntervals


class BinanceAPI(BaseAPI):
    def __init__(self) -> None:
        url = "https://fapi.binance.com/fapi/v1"
        kline_decoder = msgspec.json.Decoder(list[Candle])
        self.encoder = Encoder()
        self.price_change_decoder = msgspec.json.Decoder(TickerPriceChange)
        self._session: aiohttp.ClientSession | None = None
        super().__init__(url, kline_decoder)

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    @override
    async def fetch_symbols(self) -> set[str]:
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
            klines = self.kline_decoder.decode(raw_bytes)
            kline_dataset = {
                "symbol": symbol,
                "interval": interval,
                "candles": klines,
            }

            return kline_dataset

    @override
    async def fetch_price_change(self, symbol: str):
        params = {"symbol": symbol.replace("-", "").upper()}

        session = await self._get_session()
        async with session.get(f"{self.url}/ticker/24hr", params=params) as r:
            try:
                r.raise_for_status()
            except Exception:
                raise HTTPException(r.status, detail=f"Invalid Symbol: {symbol}")
            raw_bytes = await r.read()

            ticker_price_change = self.price_change_decoder.decode(raw_bytes)
            return ticker_price_change
