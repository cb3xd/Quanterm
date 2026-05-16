from contextlib import asynccontextmanager
from fastapi import FastAPI
from quanterm.bus.base import get_event_bus
from quanterm.exchange.binanceusdm.bridge import BinanceFapiWebsocketBridge
from quanterm.exchange.binanceusdm.client import BinanceUSDM
from quanterm.api.routes.websocket import router

event_bus = get_event_bus()
binanceusdm = BinanceUSDM()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ws = await binanceusdm.ws_instance(event_bus)
    bridge = BinanceFapiWebsocketBridge(ws)
    await ws.connect()
    print("Binance WS backend connected")

    yield

    await ws.disconnect()
    print("Binance WS backend disconnected")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
