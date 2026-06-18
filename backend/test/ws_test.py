import asyncio

import websockets
import msgspec

encoder = msgspec.json.Encoder()


def sub():
    return encoder.encode(
        {
            "method": "sub",
            "events": [
                "trade_stream.btcusdt",
                "trade_stream.xrpusdt",
                "trade_stream.solusdt",
                "trade_stream.ethusdt",
            ],
            "exchange": "binanceusdm",
        }
    )


def list_events():
    return encoder.encode({"method": "list_events", "exchange": "binanceusdm"})


async def test():
    while True:
        async with websockets.connect("ws://localhost:8000/ws") as ws:
            await ws.send(sub())

            await ws.send(list_events())
            while True:
                print(await ws.recv())


asyncio.run(test())
