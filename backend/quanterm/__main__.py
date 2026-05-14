from msgspec import Struct
from quanterm.bus.base import EventBus
from quanterm.bus.utils import generate_event_id
from quanterm.types import ExchangeID, StreamTypes
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

    print("Subscribing to KLINE")
    symbol = binanceusdm.get_stream_id("btcusdt", MarketStreams.KLINE_1M)
    await ws.subscribe(symbol)

    event_id = generate_event_id(
        ExchangeID.binanceusdm, "btcusdt", StreamTypes.kline_stream, "1m"
    )
    print(f"listening to {event_id}")
    event_bus.on(event_id, foo2)
    await asyncio.sleep(20)

    await ws.disconnect()
    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
