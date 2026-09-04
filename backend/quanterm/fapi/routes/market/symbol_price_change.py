from fastapi import HTTPException
from msgspec import Struct, json, to_builtins
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager
from quanterm.fapi.routers import api_router
from quanterm.fapi.utils import validate_symbol

_encoder = json.Encoder()


@api_router.get("/price_change/{exchange_id}")
async def get_ticker_price_change(symbol: str, exchange_id: ExchangeID):
    validate_symbol(symbol)

    exchange = manager.get_exchange(exchange_id)
    ticker_price_change = await exchange.api.fetch_price_change(symbol)
    return to_builtins(ticker_price_change)
