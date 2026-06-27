import asyncio
import logging

from typing import override
import msgspec
import websockets
import json
from quanterm.exchange.binanceusdm.schemas import (
    PACKET_MAPPERS,
    StreamRouterType,
)
from quanterm.exchange.binanceusdm.utils import format_id
from quanterm.websocket.base import BaseWS


class BinanceEnvelope(msgspec.Struct):
    stream: str | None
    packet: StreamRouterType = msgspec.field(name="data")


_envelope_decoder = msgspec.json.Decoder(BinanceEnvelope)

logging.getLogger("websockets").setLevel(logging.CRITICAL)


class BinanceWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self.uri: str = "wss://fstream.binance.com/market/stream"
        self.encoder = msgspec.json.Encoder()
        self.max_streams: int = 1024
        self._reconnect_delay: float = 1.0
        self._max_delay: float = 60.0

    @override
    async def connect(self) -> None:
        delay = self._reconnect_delay
        try:
            self.websocket: (
                websockets.ClientConnection | None
            ) = await websockets.connect(self.uri, ping_interval=20, ping_timeout=10)
            self._reconnect_delay = 1.0
            self._watch_task: asyncio.Task[None] | None = asyncio.create_task(
                self._listen()
            )
        except (TimeoutError, OSError, websockets.WebSocketException) as e:
            print(f"WS reconnect in {delay}s: {e}")
            await asyncio.sleep(delay)
            self._reconnect_delay = min(delay * 2, self._max_delay)
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

        print("WS Disconnected, attempting reconnect")
        await self.connect()

    @override
    async def subscribe(self, events: set[str]):

        if self.active_streams.__len__() == self.max_streams:
            print("Max streams reached")
            return

        if self.websocket is None:
            print("Connect first.")
            return

        events = events.difference(self.active_streams)

        self.active_streams.update(events)
        formatted_events: set[str] = set()
        for event in events:
            formatted_events.add(format_id(event))
        if formatted_events.__len__() <= 0:
            return
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": list(formatted_events),
        }
        await self.websocket.send(json.dumps(subscribe_message))

    @override
    async def _on_message(self, raw: bytes):
        try:
            if raw.startswith(b'{"result"}'):
                return
            msg = _envelope_decoder.decode(raw)
            if msg.packet is None:
                return
            formatted_data = PACKET_MAPPERS.get(type(msg.packet))
            if formatted_data is None:
                return
            formatted_data = formatted_data(msg.packet)
            await self.event_bus.publish(formatted_data.event_id, formatted_data)
        except msgspec.ValidationError:
            pass
        except Exception as e:
            print("WS Error:", e)
