import asyncio

from quanterm.exchange.binanceusdm.ws import BinanceWebsocket


ws = BinanceWebsocket()


async def main():
    await ws.connect()


asyncio.run(main())
