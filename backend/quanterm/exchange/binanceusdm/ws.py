import asyncio
import msgspec
import websockets
import json
from quanterm.schemas import TradePacket
from quanterm.exchange.binanceusdm.schemas import Packet
from quanterm.exchange.binanceusdm.streams import BinanceStreamDefinitions
from quanterm.websocket.base import BaseWS


class BinanceWebsocket(BaseWS):
    def __init__(self, event_bus) -> None:
        super().__init__(event_bus)
        self.uri = "wss://fstream.binance.com/market/stream"
        self.streams = BinanceStreamDefinitions.streams
        self.msg_decoder = msgspec.json.Decoder(Packet)
        self.max_streams = 1024

    async def connect(self) -> None:
        self.websocket = await websockets.connect(self.uri)
        self._watch_task = asyncio.create_task(self._listen())

    async def disconnect(self) -> None:
        if self._watch_task:
            self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass

            self._watch_task = None

        if self.websocket:
            await self.websocket.close()
            self.websocket = None

        print("WS Disconnected")

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

    async def _on_message(self, raw: str):
        if "stream" not in raw:
            return

        packet = self.msg_decoder.decode(raw.encode())

        stream_type = packet.stream.split("@")[1]
        stream = self.streams[stream_type]

        data: TradePacket = stream.mapper(msgspec.convert(packet.data, stream.schema))

        await self.event_bus.publish(data.event_id, data)
