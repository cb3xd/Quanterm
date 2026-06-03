from fastapi import APIRouter
from msgspec import Struct, json, to_builtins
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager

router = APIRouter()
_encoder = json.Encoder()


@router.get("/price_change/{exchange_id}")
async def get_ticker_price_change(symbol: str, exchange_id: ExchangeID):
    exchange = manager.get_exchange(exchange_id)
    ticker_price_change: Struct = await exchange.api.fetch_price_change(symbol)
    return to_builtins(ticker_price_change)
