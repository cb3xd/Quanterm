import asyncio
from typing import override
import msgspec
import websockets
import json
from quanterm.exchange.binanceusdm.schemas import (
    WS_DECODER,
    StreamRouterType,
)
from quanterm.websocket.base import BaseWS


class BinanceEnvelope(msgspec.Struct):
    stream: str | None
    packet: StreamRouterType = msgspec.field(name="data")


_envelope_decoder = msgspec.json.Decoder(BinanceEnvelope)


class BinanceWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self.uri: str = "wss://fstream.binance.com/market/stream"
        self.msg_decoder = WS_DECODER
        self.encoder = msgspec.json.Encoder()
        self.max_streams: int = 1024

    @override
    async def connect(self) -> None:
        try:
            self.websocket: (
                websockets.ClientConnection | None
            ) = await websockets.connect(self.uri)
            self._watch_task: asyncio.Task[None] | None = asyncio.create_task(
                self._listen()
            )
        except TimeoutError:
            print("Your connection is slow as shit. Reconnecting...")
            await self.connect()

    @override
    async def disconnect(self) -> None:
        if self._watch_task:
            _ = self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass

            self._watch_task = None

        if self.websocket:
            await self.websocket.close()
            self.websocket = None

        print("WS Disconnected")

    @override
    async def subscribe(self, events: set[str]):
        if self.active_streams.__len__() == self.max_streams:
            print("Max streams reached")
            return

        if self.websocket is None:
            print("Connect first.")
            return

        events = self.active_streams - events

        self.active_streams.union(events)
        subscribe_message = {"method": "SUBSCRIBE", "params": events}

        await self.websocket.send(json.dumps(subscribe_message))

    @override
    async def _on_message(self, raw: bytes):
        try:
            msg = _envelope_decoder.decode(raw)
            if msg.packet.data is None:
                return
            await self.event_bus.publish(msg.packet.data.event_id, msg.packet.data)
        except msgspec.ValidationError:
            print(raw)
            pass
        except Exception as e:
            print("WS Error:", e)
