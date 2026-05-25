from contextlib import asynccontextmanager
from fastapi import FastAPI
from quanterm.api.routes.websocket import router as ws_router
from quanterm.api.routes.symbols import router as symbols_router
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager.get_exchange(ExchangeID.binanceusdm)
    await manager.connect_all_websockets()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(ws_router)
app.include_router(symbols_router, prefix="/api")
