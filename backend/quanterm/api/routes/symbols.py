from fastapi import APIRouter, Response
from msgspec import json
from quanterm.exchange.registry import EXCHANGE_REGISTRY
from quanterm.exchange.symbol_registry import symbol_registry

router = APIRouter()
_encoder = json.Encoder()


@router.get("/all_exchange_symbols")
async def get_all_exchange_symbols():
    symbols = await symbol_registry.get_all_symbols()
    serialized_bytes = _encoder.encode(symbols)
    print(EXCHANGE_REGISTRY)
    return Response(content=serialized_bytes, media_type="application/json")
