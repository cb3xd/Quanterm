import asyncio
import json
from typing import override

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
        self._logger.info(
            f"{self._exchange_id}: subscribed to {events.__len__()} events"
        )

        await self._websocket.send(json.dumps(subscribe_message))

    @override
    async def _unsubscribe(self, events: set[str]):
        return NotImplemented

    @override
    async def _on_message(self, raw: bytes) -> None:
        try:
            if raw.startswith(b'{"success":"false"'):
                raise RuntimeError(f"{self._exchange_id}: subscription failed\n{raw}")
            if raw.startswith(b'{"success":'):
                self._logger.debug(
                    f"{self._exchange_id}: ignoring subscription acknowledgement"
                )
                return

            msg = self._envelope_decoder.decode(raw)
            topic = msg.topic
            if len(topic) < 2:
                raise RuntimeError(
                    f"{self._exchange_id}: invalid topic format (no dot): {topic}"
                )

            event_id = self._stream_registry.get_event_id(topic)

            if event_id is None:
                raise KeyError(f"{self._exchange_id}: {topic} not found in registry.")

            msg.topic = msg.topic.split(".")[0]
            msg_dtype = type(msg.data)
            data_mapper = PACKET_MAPPERS.get(msg_dtype)

            if data_mapper is None:
                raise RuntimeError(
                    f"{self._exchange_id}: data mapper for {type(msg.data)} not found."
                )

            formatted_data = data_mapper(msg)

            if formatted_data is None or not isinstance(formatted_data, list):
                raise RuntimeError(
                    f"{self._exchange_id}: failed to format data\n{msg}\n"
                )
            await asyncio.gather(
                *[self._event_bus.publish(event_id, event) for event in formatted_data],
                return_exceptions=False,
            )

        except Exception as e:
            raise RuntimeError(f"{self._exchange_id}: {e}") from e
