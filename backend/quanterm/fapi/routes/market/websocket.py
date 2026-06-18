from enum import StrEnum

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from msgspec import Struct, json

from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager
from quanterm.types import KlineIntervals, StreamTypes

router = APIRouter()


class FapiMethods(StrEnum):
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"
    LIST_EVENTS = "list_events"


class Subscribe(Struct, tag_field="method", tag=str(FapiMethods.SUBSCRIBE)):
    events: set[str]
    exchange: ExchangeID


class Unsubscribe(Struct, tag_field="method", tag=str(FapiMethods.UNSUBSCRIBE)):
    streams: list[str]
    exchange: ExchangeID


class ListEvents(Struct, tag_field="method", tag=str(FapiMethods.LIST_EVENTS)):
    exchange: ExchangeID


_msg_types = Subscribe | Unsubscribe | ListEvents
_msg_decoder = json.Decoder(_msg_types)


async def websocket_loop(websocket: WebSocket):
    while True:
        try:
            data = await websocket.receive_bytes()
            message = _msg_decoder.decode(data)
            events = message.events
            exchange = manager.get_exchange(message.exchange)

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
