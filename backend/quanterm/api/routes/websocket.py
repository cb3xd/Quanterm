from enum import StrEnum
from fastapi import WebSocket, APIRouter
from msgspec import DecodeError, Struct, json, convert
from quanterm.bus.base import get_event_bus
from quanterm.schemas import FastApiSubscribePacket

event_bus = get_event_bus()
router = APIRouter()


class Methods(StrEnum):
    SUBSCRIBE = "SUBSCRIBE"


class Packet(Struct):
    method: Methods
    params: dict


sub_decoder = json.Decoder(FastApiSubscribePacket)
packet_decoder = json.Decoder(Packet)


@router.websocket("/ws/{exchange}/streams")
async def ws_route(websocket: WebSocket, exchange: str):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            msg = packet_decoder.decode(data.encode())
            if msg.method == "SUBSCRIBE":
                param_dict = msg.params
                param_dict["event_id"] = f"{exchange}.subscribe"
                params = convert(param_dict, FastApiSubscribePacket)
                await event_bus.publish(params.event_id, params)
        except DecodeError:
            print("Invalid request.")
            continue
