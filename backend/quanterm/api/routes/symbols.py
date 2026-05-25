from fastapi import APIRouter, Response
from msgspec import json
from quanterm.exchange.exchange_manager import manager

router = APIRouter()
_encoder = json.Encoder()


@router.get("/all_exchange_symbols")
async def get_all_exchange_symbols():
    symbols = await manager.get_all_symbols()
    serialized_bytes = _encoder.encode(symbols)
    return Response(content=serialized_bytes, media_type="application/json")
