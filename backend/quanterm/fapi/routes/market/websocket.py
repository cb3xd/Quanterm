from enum import StrEnum

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from msgspec import Struct, json

from quanterm.bus.base import get_event_bus
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager

router = APIRouter()


class FapiMethods(StrEnum):
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"
    LIST_EVENTS = "list_events"


class Subscribe(Struct, tag_field="method", tag=str(FapiMethods.SUBSCRIBE)):
    events: set[str]
    exchange: ExchangeID


class Unsubscribe(Struct, tag_field="method", tag=str(FapiMethods.UNSUBSCRIBE)):
    events: set[str]
    exchange: ExchangeID


class ListEvents(Struct, tag_field="method", tag=str(FapiMethods.LIST_EVENTS)):
    exchange: ExchangeID


_msg_types = Subscribe | Unsubscribe | ListEvents
_msg_decoder = json.Decoder(_msg_types)
_msg_encoder = json.Encoder()
_event_bus = get_event_bus()


async def websocket_loop(websocket: WebSocket):
    while True:
        try:
            data = await websocket.receive_bytes()
            message = _msg_decoder.decode(data)
            exchange = manager.get_exchange(message.exchange)
            if type(message) is ListEvents:
                # exchange.ws.active_streams returns a set
                continue
            if type(message) is Unsubscribe:
                continue
            events = message.events

            event_ids = set(
                map(lambda event_id: message.exchange + "." + event_id, events)
            )

            async def send_msg(packet: Struct):
                await websocket.send_bytes(_msg_encoder.encode(packet))

            for event_id in event_ids:
                _event_bus.on(event_id, send_msg)

            await exchange.ws.subscribe(events)

        except WebSocketDisconnect:
            print("Client disconnected cleanly.")
            break


@router.websocket("/ws")
async def ws_router(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket_loop(websocket)
    finally:
        print("Cleaning up.")
