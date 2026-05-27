from fastapi import APIRouter, Response
from msgspec import json
from quanterm.exchange.exchange_manager import manager

router = APIRouter()
_encoder = json.Encoder()


@router.get("/kline")
async def get_kline():
    symbol = 
    return Response(content=serialized_bytes, media_type="application/json")
