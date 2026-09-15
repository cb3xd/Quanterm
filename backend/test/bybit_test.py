import asyncio
import logging

from quanterm.exchange.binanceusdm.ws import BinanceWebsocket
from quanterm.exchange.bybit.api import BybitAPI
from quanterm.exchange.bybit.ws import BybitWebsocket


async def main():
    ws = BybitWebsocket()
    ws2 = BinanceWebsocket()

    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    logger.debug("Starting test")

    await ws2.connect()
    await ws.connect()
    await ws2.subscribe(set(["trade_stream.btc-usdt"]))
    await ws.subscribe(set(["kline_stream.btc-usdt.1m"]))
    await asyncio.sleep(3)

    logger.debug("Test 1 passed")

    api = BybitAPI()
    einfo = await api.fetch_exchange_info()
    logger.debug(f"{einfo.current_page.next_page_cursor}")
    logger.debug("Test 2 passed")

    await api.close()
    await ws.disconnect()
    await ws2.disconnect()

    logger.debug("All tests passed")


if __name__ == "__main__":
    asyncio.run(main())
