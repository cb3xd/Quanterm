import logging

from msgspec import Struct, json, to_builtins
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager
from quanterm.types import KlineIntervals
from quanterm.fapi.routers import api_router

_encoder = json.Encoder()


@api_router.get("/kline/{exchange_id}")
async def get_kline(symbol: str, exchange_id: ExchangeID, interval: KlineIntervals):
    exchange = manager.get_exchange(exchange_id)
    kline: Struct = await exchange.api.fetch_kline(symbol, interval)
    return to_builtins(kline)
