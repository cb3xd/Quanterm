from msgspec import Struct
from quanterm.bus.base import EventBus
from quanterm.types import StreamTypes
from quanterm.exchange.binanceusdm.client import BinanceUSDM
from quanterm.exchange.binanceusdm.streams import MarketStreams
import asyncio


async def foo(data: Struct) -> None:
    pass


async def foo2(data: Struct) -> None:
    print(data)


async def foo3(data: Struct) -> None:
    print("Received by function 3!")


async def main():
    binanceusdm = BinanceUSDM()
    event_bus = EventBus()
    ws = await binanceusdm.ws_instance(event_bus)

    await ws.connect()

    symbols = await binanceusdm.get_symbols()
    for symbol in symbols:
        print(f"Subscribing to: {symbol}@aggTrade")
        await ws.subscribe(f"{symbol}@aggTrade")
        event_bus.on("binanceusdm.{symbol}.trade_stream", foo2)
        await asyncio.sleep(0.15)

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
