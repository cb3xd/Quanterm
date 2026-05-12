from quanterm.exchange.binanceusdm.client import BinanceUSDM
from quanterm.exchange.binanceusdm.streams import MarketStreams
import asyncio


# Test and sample code
async def main():
    binanceusdm = BinanceUSDM()
    ws = await binanceusdm.ws_instance()
    await ws.connect()
    symbol = binanceusdm.get_stream_id("btcusdt", MarketStreams.TRADES)
    await ws.subscribe(symbol)
    await asyncio.sleep(3)
    await ws.disconnect()
    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
