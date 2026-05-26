import asyncio

import msgspec

from quanterm.exchange.binanceusdm.external_api import fetch_kline
from quanterm.types import KlineIntervals


async def main():
    test = await fetch_kline("btcusdt", KlineIntervals.minute)
    print(test.candles[1])


asyncio.run(main())
