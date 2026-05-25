from fastapi import APIRouter
from quanterm.exchange.exchange_manager import manager

router = APIRouter()


@router.get("/all_exchange_symbols")
async def get_all_exchange_symbols():
    return await manager.get_all_symbols()
