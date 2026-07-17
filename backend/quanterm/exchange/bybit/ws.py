import asyncio

import msgspec
import websockets


class BinanceEnvelope(msgspec.Struct):
    topic: str
    data: list[]
