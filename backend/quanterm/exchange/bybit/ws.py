import json
from typing import Any, override

import msgspec


from quanterm.exchange.bybit.mappers import (
    PACKET_MAPPERS,
    BybitEnvelope,
)
from quanterm.exchange.bybit.utils import format_id
from quanterm.exchange.constants import ExchangeID
from quanterm.websocket.base import BaseWS


class BybitWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self._uri = "wss://stream.bybit.com/v5/public/linear"
        self._max_streams = 500
        self._reconnect_delay = 1.0
        self._max_delay = 60.0
        self._exchange_id = ExchangeID.bybit
        self._envelope_decoder = msgspec.json.Decoder(BybitEnvelope)

    def _get_stream_keys(self, events: set[str]) -> dict[str, str]:
        return {event: format_id(event) for event in events}

    @override
    async def _subscribe(self, events: set[str]) -> None:
        if self._websocket is None:
            raise RuntimeError(f"{self._exchange_id}: websocket not connected")

        events = events.difference(self._active_streams)
        stream_key_map = self._get_stream_keys(events)

        if not stream_key_map:
            return

        for event, key in stream_key_map.items():
            self._stream_registry.register(f"{self._exchange_id}.{event}", key)

        self._active_streams.update(events)
        subscribe_message = {
            "op": "subscribe",
            "args": list(stream_key_map.values()),
        }

        await self._websocket.send(json.dumps(subscribe_message))

    @override
    async def _unsubscribe(self, events: set[str]) -> None:
        return

    @override
    async def _on_message(self, raw: bytes) -> None:
        try:
            if raw.startswith(b'{"success":'):
                return
            msg = self._envelope_decoder.decode(raw)
            topic = msg.topic
            msg.topic = msg.topic.split(".")
            msg_type = type(msg.data)
            data_mapper = PACKET_MAPPERS.get(msg_type)

            if data_mapper is None:
                return

            formatted_data = data_mapper(msg)

            if formatted_data is None:
                return

            event_id = self._stream_registry.get_event_id(topic)

            if event_id is None:
                return

            for event in formatted_data:
                event.event_id = event_id
                self._logger.info(event.event_id)
                await self._event_bus.publish(event_id, event)

        except Exception as e:
            self._logger.exception(f"{self._exchange_id}: {e}")
            pass

        return
