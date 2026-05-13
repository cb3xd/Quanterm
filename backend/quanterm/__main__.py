from msgspec import Struct
from quanterm.bus.base import EventBus
from quanterm.exchange.binanceusdm.client import BinanceUSDM
from quanterm.exchange.binanceusdm.streams import MarketStreams
import asyncio


async def foo(data: Struct) -> None:
    print("Received by function 1!")


async def foo2(data: Struct) -> None:
    print("Received by function 2!")


async def foo3(data: Struct) -> None:
    print("Received by function 3!")


async def main():
    binanceusdm = BinanceUSDM()
    event_bus = EventBus()
    ws = await binanceusdm.ws_instance(event_bus)

    await ws.connect()

    symbols = ["btcusdt", "ethusdt", "solusdt"]
    for symbol in symbols:
        stream_id = binanceusdm.get_stream_id(symbol, MarketStreams.TRADES)
        await ws.subscribe(stream_id)
        await asyncio.sleep(0.15)

    symbol = binanceusdm.get_stream_id("btcusdt", MarketStreams.TRADES)
    print(symbol)
    event_bus.on(symbol, foo)
    event_bus.on(symbol, foo2)
    event_bus.on(symbol, foo3)
    await asyncio.sleep(100)

    await ws.disconnect()
    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
