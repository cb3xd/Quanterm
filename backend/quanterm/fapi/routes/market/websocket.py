import asyncio
import collections
from enum import StrEnum
from fastapi import WebSocket
from msgspec import Struct, json
from quanterm.bus.base import get_event_bus
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange import manager
from quanterm.fapi.routers import ws_router
from quanterm.websocket import JSON_ENCODER


class FapiMethods(StrEnum):
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"


class Subscribe(Struct, tag_field="method", tag=str(FapiMethods.SUBSCRIBE)):
    events: set[str]
    exchange: ExchangeID


class Unsubscribe(Struct, tag_field="method", tag=str(FapiMethods.UNSUBSCRIBE)):
    events: set[str]
    exchange: ExchangeID


_msg_types = Subscribe | Unsubscribe
_msg_decoder = json.Decoder(_msg_types)
_msg_encoder = JSON_ENCODER
_event_bus = get_event_bus()


class ConnectionState:
    """Shared state between the send and receive loops for one socket."""

    def __init__(self):
        self.queue: collections.deque[bytes] = collections.deque(maxlen=4000)
        self.data_available = asyncio.Event()
        self.disconnected = False

    async def queue_packet(self, packet: Struct):
        self.queue.append(_msg_encoder.encode(packet))
        self.data_available.set()


async def _send_loop(websocket: WebSocket, state: ConnectionState):
    while not state.disconnected:
        try:
            if not state.queue:
                state.data_available.clear()
                await state.data_available.wait()
                continue
            await websocket.send_bytes(state.queue.popleft())
        except Exception:
            state.disconnected = True


async def _handle_message(message: Subscribe | Unsubscribe, state: ConnectionState):
    if isinstance(message, Unsubscribe):
        return

    exchange = manager.get_exchange(message.exchange)
    await exchange.ws.subscribe(message.events)

    for event in message.events:
        event_id = f"{message.exchange}.{event}"
        _event_bus.on(event_id, state.queue_packet)


async def _receive_loop(websocket: WebSocket, state: ConnectionState):
    while not state.disconnected:
        try:
            data = await websocket.receive_bytes()
            message = _msg_decoder.decode(data)
            await _handle_message(message, state)
        except Exception:
            state.disconnected = True


async def websocket_loop(websocket: WebSocket):
    state = ConnectionState()
    try:
        async with asyncio.TaskGroup() as task_group:
            task_group.create_task(_send_loop(websocket, state))
            task_group.create_task(_receive_loop(websocket, state))
    finally:
        _event_bus.unregister_all(state.queue_packet)


@ws_router.websocket("")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket_loop(websocket)
