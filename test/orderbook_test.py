import asyncio

from quanterm.exchange.binanceusdm.api import BinanceAPI

api = BinanceAPI()


async def main():
    ob = await api.fetch_orderbook_snapshot("BTC-USDT")
    print(ob)


asyncio.run(main())
