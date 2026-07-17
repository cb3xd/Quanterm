import websockets
import asyncio


async def main():
    url = "wss://fstream.binance.com/streams/market"
    async with websockets.connect(url) as ws:
        print("Connected")
        await ws.recv()


if __name__ == "__main__":
    asyncio.run(main())
