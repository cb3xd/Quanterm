import asyncio

import websockets
import msgspec


async def test():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        encoder = msgspec.json.Encoder()

        msg = encoder.encode(
            {
                "method": "sub",
                "events": ["trade_stream.btcusdt"],
                "exchange": "binanceusdm",
            }
        )
        await ws.send(msg)


asyncio.run(test())
