import asyncio

from quanterm.bus.base import get_event_bus
from quanterm.exchange.binanceusdm.ws import BinanceWebsocket


async def foo(data):
    print(data)


async def main():
    ws = BinanceWebsocket()
    await ws.connect()
    await ws.subscribe(set(["btcusdt@aggTrade", "ethusdt@aggTrade"]))

    event_bus = get_event_bus()
    event_bus.on("binanceusdm.trade_stream.btcusdt", foo)
    await asyncio.sleep(100)


if __name__ == "__main__":
    asyncio.run(main())
