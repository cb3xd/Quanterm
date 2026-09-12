from fastapi import Response
from msgspec import json
from quanterm.registries import SYMBOL_REGISTRY
from quanterm.fapi.routers import api_router

_encoder = json.Encoder()


@api_router.get("/symbols")
async def get_all_exchange_symbols():
    symbols = await SYMBOL_REGISTRY.get_all_symbols()
    serialized_bytes = _encoder.encode(symbols)
    return Response(content=serialized_bytes, media_type="application/json")
