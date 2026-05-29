import asyncio
from typing import override
import msgspec
import websockets
import json
from quanterm.schemas import StreamDefinition, TradePacket
from quanterm.exchange.binanceusdm.schemas import Packet
from quanterm.exchange.binanceusdm.streams import BinanceStreamDefinitions
from quanterm.websocket.base import BaseWS


class BaseEnvelope(msgspec.Struct):
    stream: str | None = None
    id: int | None = None


_envelope_decoder = msgspec.json.Decoder(BaseEnvelope)


class BinanceWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self.uri: str = "wss://fstream.binance.com/market/stream"
        self.streams: dict[str, StreamDefinition] = BinanceStreamDefinitions.streams
        self.msg_decoder: msgspec.json.Decoder[Packet] = msgspec.json.Decoder(Packet)
        self.max_streams: int = 1024

    @override
    async def connect(self) -> None:
        self.websocket: websockets.ClientConnection | None = await websockets.connect(
            self.uri
        )
        self._watch_task: asyncio.Task[None] | None = asyncio.create_task(
            self._listen()
        )

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
    async def subscribe(self, stream_id: str):
        if self.active_streams.__len__() == self.max_streams:
            print("Max streams reached")
            return

        if self.websocket is None:
            print("Connect first.")
            return

        if stream_id in self.active_streams:
            print(f"[{stream_id}] Stream already exists!")
            return

        self.active_streams.add(stream_id)
        subscribe_message = {"method": "SUBSCRIBE", "params": [stream_id], "id": 1}

        await self.websocket.send(json.dumps(subscribe_message))

    @override
    async def _on_message(self, raw: bytes):
        try:
            envelope = _envelope_decoder.decode(raw)
            if envelope.stream is None:
                return

            packet = self.msg_decoder.decode(raw)

            stream_type = packet.stream.split("@")[1]
            stream = self.streams[stream_type]

            data = stream.mapper(msgspec.convert(packet.data, stream.schema))

            await self.event_bus.publish(data.event_id, data)
        except Exception as e:
            print(e)
