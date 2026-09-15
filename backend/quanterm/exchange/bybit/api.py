import logging
from typing import override
from msgspec import json
from quanterm.exchange.bybit.api_schemas import TickerData
from quanterm.external_api.base import BaseAPI


class BybitAPI(BaseAPI):
    def __init__(self) -> None:
        url = "https://api.bybit.com/v5/market"
        super().__init__(url)

    @override
    async def fetch_exchange_info(self):
        session = await self._get_session()
        async with session.get(
            f"{self.url}/instruments-info", params={"category": "linear", "limit": 1000}
        ) as r:
            r.raise_for_status()
            raw_bytes = await r.read()
            decoded_response = json.decode(raw_bytes, type=TickerData)
            return decoded_response

    @override
    async def fetch_symbols(self) -> set[str]:
        logging.getLogger("uvicorn").info("Fetching symbols for bybit")
        ticker_data = await self.fetch_exchange_info()
        symbols = set()
        for symbol in ticker_data.current_page.symbols:
            symbols.add(f"{symbol.base_coin.lower()}-{symbol.quote_coin.lower()}")
        return symbols

    @override
    async def fetch_kline(self, symbol: str, interval):
        return
