from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quanterm.exchange.exchange_manager import manager
from quanterm.fapi.routes.market.websocket import router as websocket_router
import tracemalloc


@asynccontextmanager
async def lifespan(app: FastAPI):
    tracemalloc.start(10)
    await manager.connect_all_websockets()
    yield
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
