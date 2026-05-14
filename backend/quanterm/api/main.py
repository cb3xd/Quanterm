from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from quanterm.bus.base import get_event_bus
from quanterm.exchange.binanceusdm.client import BinanceUSDM

event_bus = get_event_bus()
binanceusdm = BinanceUSDM()
app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ws = await binanceusdm.ws_instance(event_bus)

    await ws.connect()
    print("Binance WS backend connected")
    yield

    await ws.disconnect()
    print("Binance WS backend disconnected")


app = FastAPI(lifespan=lifespan)
