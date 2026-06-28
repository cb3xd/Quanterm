import asyncio
import collections
from enum import StrEnum
import logging
from fastapi import APIRouter, WebSocket
from msgspec import Struct, json
from quanterm.bus.base import get_event_bus
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager

router = APIRouter()


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
_msg_encoder = json.Encoder()
_event_bus = get_event_bus()

logger = logging.getLogger("uvicorn")


async def websocket_loop(websocket: WebSocket):
    queue = collections.deque(maxlen=4000)
    data_available = asyncio.Event()
    disconnected = False

    async def queue_packet(packet: Struct):
        queue.append(_msg_encoder.encode(packet))
        data_available.set()

    async def send_loop():
        nonlocal disconnected
        while not disconnected:
            try:
                if queue:
                    await websocket.send_bytes(queue.popleft())
                else:
                    data_available.clear()
                    await data_available.wait()

            except Exception:
                disconnected = True
                break

    async def receive_loop():
        nonlocal disconnected
        while not disconnected:
            try:
                data = await websocket.receive_bytes()
                message = _msg_decoder.decode(data)
                exchange = manager.get_exchange(message.exchange)

                if type(message) is Unsubscribe:
                    continue
                events = message.events

                event_ids = set(
                    map(lambda event_id: message.exchange + "." + event_id, events)
                )
                for event_id in event_ids:
                    _event_bus.on(event_id, queue_packet)
                await exchange.ws.subscribe(events)
            except Exception:
                disconnected = True
                break

    try:
        async with asyncio.TaskGroup() as task_group:
            task_group.create_task(send_loop())
            task_group.create_task(receive_loop())
    finally:
        _event_bus.unregister_all(queue_packet)


@router.websocket("/ws")
async def ws_router(websocket: WebSocket):
    await websocket.accept()
    await websocket_loop(websocket)
