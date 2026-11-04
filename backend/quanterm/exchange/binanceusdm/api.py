import logging
from typing import override

import msgspec
from fastapi import HTTPException
from msgspec.json import Decoder

from quanterm.exchange.binanceusdm.api_schemas import (
    Candle,
    ExchangeInfo,
    KlineData,
    OrderbookData,
)
from quanterm.external_api.base import BaseAPI
from quanterm.orderbook import LocalOrderbook
from quanterm.types import KlineIntervals


class BinanceAPI(BaseAPI):
    def __init__(self) -> None:
        url = "https://fapi.binance.com/fapi/v1"
        self._orderbook_snapshot_decoder = Decoder(OrderbookData)
        self._kline_decoder = Decoder(list[Candle])
        super().__init__(url)

    @override
    async def fetch_symbols(self) -> set[str]:
        logging.getLogger("uvicorn").info("Fetching symbols")
        exchange_info = await self.fetch_exchange_info()
        symbols: set[str] = set()
        for symbol in exchange_info.symbols:
            symbols.add(f"{symbol.base_asset.lower()}-{symbol.quote_asset.lower()}")
        return symbols

    @override
    async def fetch_exchange_info(self):
        session = await self._get_session()
        async with session.get(f"{self.url}/exchangeInfo") as r:
            r.raise_for_status()
            if r.status != 200:
                raise HTTPException(r.status)
            raw_bytes = await r.read()
            data = msgspec.json.decode(raw_bytes, type=ExchangeInfo)
            return data

    @override
    async def fetch_kline(self, symbol: str, interval: KlineIntervals):
        params = {"symbol": symbol.replace("-", "").upper(), "interval": interval}
        session = await self._get_session()
        async with session.get(f"{self.url}/klines", params=params) as r:
            r.raise_for_status()

            if r.status != 200:
                raise HTTPException(r.status, detail=f"Invalid Symbol: {symbol}")

            raw_bytes = await r.read()
            klines = self._kline_decoder.decode(raw_bytes)

            return KlineData(symbol=symbol, interval=interval, candles=klines)

    @override
    async def fetch_orderbook_snapshot(self, symbol: str):
        params = {"symbol": symbol.replace("-", "").upper(), "limit": 1000}
        session = await self._get_session()
        async with session.get(f"{self.url}/depth", params=params) as r:
            r.raise_for_status()

            if r.status != 200:
                raise HTTPException(r.status)

            raw_bytes = await r.read()
            data = self._orderbook_snapshot_decoder.decode(raw_bytes)

            return LocalOrderbook(
                symbol=symbol,
                event_time=data.E,
                transaction_time=data.T,
                bids=data.bids,
                asks=data.asks,
            )
