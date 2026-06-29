from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quanterm.exchange.exchange_manager import manager
from quanterm.fapi.routes.market.kline import router as kline_router
from quanterm.fapi.routes.market.symbol_price_change import (
    router as price_change_router,
)
from quanterm.fapi.routes.market.symbols import router as symbols_router
from quanterm.fapi.routes.market.websocket import router as websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.connect_all_websockets()
    yield
    await manager.close_all()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router)
app.include_router(symbols_router, prefix="/api")
app.include_router(price_change_router, prefix="/api")
app.include_router(kline_router, prefix="/api")
