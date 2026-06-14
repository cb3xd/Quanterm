from enum import StrEnum

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from msgspec import Struct, json

from quanterm.exchange.constants import ExchangeID

router = APIRouter()


class FapiMethods(StrEnum):
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"
    LIST_EVENTS = "list_events"


class Message(Struct, tag_field="method"):
    pass


class Subscribe(Message, tag=str(FapiMethods.SUBSCRIBE)):
    params: set[str]


class Unsubscribe(Message, tag=str(FapiMethods.UNSUBSCRIBE)):
    params: set[str]


class ListEvents(Message, tag=str(FapiMethods.LIST_EVENTS)):
    params: ExchangeID


_msg_types = Subscribe | Unsubscribe | ListEvents
_msg_decoder = json.Decoder(_msg_types)


async def websocket_loop(websocket: WebSocket):
    while True:
        try:
            data = await websocket.receive_bytes()
            message = _msg_decoder.decode(data)
            print(message)
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
