from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quanterm.exchange.exchange_manager import manager
from quanterm.exchange.symbol_registry import symbol_registry
from quanterm.fapi.routers import ws_router, api_router
from quanterm.fapi.routes import market  # noqa: F401 registers routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.connect_all_websockets()
    await symbol_registry.get_all_symbols()
    yield
    await manager.close_all()


app = FastAPI(lifespan=lifespan)

app.include_router(ws_router, prefix="/ws")
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://localhost(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
