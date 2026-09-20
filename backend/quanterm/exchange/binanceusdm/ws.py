from typing import override
import msgspec
import json
from quanterm.exchange.binanceusdm.mappers import PACKET_MAPPERS, StreamRouterType
from quanterm.exchange.binanceusdm.utils import format_id
from quanterm.exchange.constants import ExchangeID
from quanterm.websocket.base import BaseWS


class BinanceEnvelope(msgspec.Struct):
    stream: str
    packet: StreamRouterType = msgspec.field(name="data")


class ErrorMessage(msgspec.Struct):
    code: int
    msg: str


class BinanceWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self._uri: str = "wss://fstream.binance.com/market/stream"
        self._max_streams: int = 1024
        self._reconnect_delay: float = 1.0
        self._max_delay: float = 60.0
        self._envelope_decoder = msgspec.json.Decoder(BinanceEnvelope)
        self._error_decoder = msgspec.json.Decoder(ErrorMessage)
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
        self._logger.info(
            f"{self._exchange_id}: subscribed to {events.__len__()} events"
        )

    @override
    async def _unsubscribe(self, events: set[str]) -> None:
        return

    @override
    async def _on_message(self, raw: bytes):
        try:
            if raw.startswith(b'{"result"'):
                self._logger.info(
                    f"{self._exchange_id}: ignoring subscription acknowledgement."
                )
                return
            if raw.startswith(b'{"code"'):
                msg = self._error_decoder.decode(raw)
                raise RuntimeError(msg)

            msg = self._envelope_decoder.decode(raw)

            msg_type = type(msg.packet)

            event_id = self._stream_registry.get_event_id(msg.stream)
            if event_id is None:
                raise RuntimeError(
                    f"{self._exchange_id}: event id for {msg.stream} is not registered."
                )

            data_mapper = PACKET_MAPPERS.get(msg_type)

            if data_mapper is None:
                raise RuntimeError(
                    f"{self._exchange_id}: data mapper for {msg_type} not found."
                )

            formatted_data = data_mapper(msg.packet)
            formatted_data.event_id = event_id
            await self._event_bus.publish(event_id, formatted_data)

        except Exception as e:
            raise RuntimeError(f"{self._exchange_id}: {e}") from e
