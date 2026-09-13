from fastapi import Response
from quanterm.registries import SYMBOL_REGISTRY
from quanterm.fapi.routers import api_router
from quanterm.websocket import JSON_ENCODER


@api_router.get("/symbols")
async def get_all_exchange_symbols():
    symbols = await SYMBOL_REGISTRY.get_all_symbols()
    serialized_bytes = JSON_ENCODER.encode(symbols)
    return Response(content=serialized_bytes, media_type="application/json")
