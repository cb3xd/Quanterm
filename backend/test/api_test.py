import asyncio

from quanterm.exchange.binanceusdm.external_api import BinanceAPI


async def main():
    api = BinanceAPI()
    test = await api.fetch_symbols()
    print(test)


asyncio.run(main())
