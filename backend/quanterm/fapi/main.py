from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quanterm.bus.base import get_event_bus
from quanterm.exchange.exchange_manager import manager
from quanterm.fapi.routes.market.symbols import router as symbols_router
from quanterm.fapi.routes.market.websocket import router as websocket_router
import tracemalloc
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")


async def monitor():
    _event_bus = get_event_bus()
    while True:
        logger.info(f"Active listeners: {len(_event_bus._listeners)}")
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    tracemalloc.start(10)
    await manager.connect_all_websockets()
    asyncio.create_task(monitor())
    yield
    await manager.close_all()
    tracemalloc.stop()


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
