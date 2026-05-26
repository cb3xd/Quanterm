from contextlib import asynccontextmanager
from fastapi import FastAPI
from quanterm.api.routes.websocket import router as ws_router
from quanterm.api.routes.symbols import router as symbols_router
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager.get_exchange(ExchangeID.binanceusdm)
    await manager.connect_all_websockets()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ws_router)
app.include_router(symbols_router, prefix="/api")
