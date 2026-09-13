import asyncio
import logging

from typing import override
import msgspec
import websockets
import json
from quanterm.exchange.binanceusdm.mappers import PACKET_MAPPERS, StreamRouterType
from quanterm.exchange.binanceusdm.utils import format_id
from quanterm.exchange.constants import ExchangeID
from quanterm.websocket.base import BaseWS


class BinanceEnvelope(msgspec.Struct):
    stream: str
    packet: StreamRouterType = msgspec.field(name="data")


class BinanceWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self._uri: str = "wss://fstream.binance.com/market/stream"
        self._max_streams: int = 1024
        self._reconnect_delay: float = 1.0
        self._max_delay: float = 60.0
        self._envelope_decoder = msgspec.json.Decoder(BinanceEnvelope)
        self._exchange_id = ExchangeID.binanceusdm

    def _get_stream_keys(self, events: set[str]) -> dict[str, str]:
        """Convert events to their stream keys"""
        return {event: format_id(event) for event in events}

    @override
    async def _subscribe(self, events: set[str]):
        if self._websocket is None:
            raise RuntimeError(f"{self._exchange_id}: websocket not connected")

        events = events.difference(self._active_streams)
        stream_key_map = self._get_stream_keys(events)

        if not stream_key_map:
            return

        for event, key in stream_key_map.items():
            self._stream_registry.register(f"{ExchangeID.binanceusdm}.{event}", key)

        self._active_streams.update(events)
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": list(stream_key_map.values()),
        }
        await self._websocket.send(json.dumps(subscribe_message))

    @override
    async def unsubscribe(self, events: set[str]) -> None:
        await super().unsubscribe(events)

    @override
    async def _on_message(self, raw: bytes):
        try:
            if raw.startswith(b'{"result"}'):
                return

            msg = self._envelope_decoder.decode(raw)
            if msg.packet is None:
                return
            msg_type = type(msg.packet)

            formatted_data = PACKET_MAPPERS.get(msg_type)

            if formatted_data is None:
                return
            event_id = self._stream_registry.get_event_id(msg.stream)
            if event_id is None:
                return
            formatted_data = formatted_data(msg.packet)
            formatted_data.event_id = event_id
            await self._event_bus.publish(event_id, formatted_data)
        except msgspec.ValidationError:
            pass
        except Exception:
            return
