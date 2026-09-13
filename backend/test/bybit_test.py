import asyncio
import logging

from quanterm.exchange.bybit.ws import BybitWebsocket


async def main():
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    logger.debug("Starting test")
    ws = BybitWebsocket()
    await ws.connect()
    # await ws.subscribe(set(["trade_stream.btc-usdt"]))
    await ws.subscribe(set(["kline_stream.btc-usdt.1m"]))
    await asyncio.sleep(100)

    return


if __name__ == "__main__":
    asyncio.run(main())
