from fastapi import Response
from msgspec import json
from quanterm.exchange.symbol_registry import symbol_registry
from quanterm.fapi.routers import api_router

_encoder = json.Encoder()


@api_router.get("/symbols")
async def get_all_exchange_symbols():
    symbols = await symbol_registry.get_all_symbols()
    serialized_bytes = _encoder.encode(symbols)
    return Response(content=serialized_bytes, media_type="application/json")
