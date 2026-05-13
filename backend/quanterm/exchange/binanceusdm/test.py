from quanterm.exchange.binanceusdm.client import BinanceUSDM
from quanterm.exchange.binanceusdm.streams import MarketStreams
import asyncio


# Test and sample code
async def main():
    binanceusdm = BinanceUSDM()
    ws = await binanceusdm.ws_instance()
    await ws.connect()

    symbols = await binanceusdm.get_symbols()
    for symbol in symbols:
        stream_id = binanceusdm.get_stream_id(symbol, MarketStreams.TRADES)
        await ws.subscribe(stream_id)
        await asyncio.sleep(0.15)

    await asyncio.sleep(100)
    await ws.disconnect()
    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
