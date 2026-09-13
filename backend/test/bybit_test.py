import asyncio
import logging

from quanterm.exchange.binanceusdm.ws import BinanceWebsocket
from quanterm.exchange.bybit.ws import BybitWebsocket


async def main():
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    logger.debug("Starting test")
    ws = BybitWebsocket()
    ws2 = BinanceWebsocket()
    await ws2.connect()
    await ws.connect()
    await ws2.subscribe(set(["trade_stream.btc-usdt"]))
    await ws.subscribe(set(["kline_stream.btc-usdt.1m"]))
    await asyncio.sleep(100)

    return


if __name__ == "__main__":
    asyncio.run(main())
