from fastapi import WebSocket, APIRouter
from msgspec import DecodeError, json, convert
from quanterm.api.types import FastApiMethods, Packet
from quanterm.bus.base import get_event_bus
from quanterm.schemas import FastApiSubscribePacket

event_bus = get_event_bus()
router = APIRouter()


packet_decoder = json.Decoder(Packet)
sub_decoder = json.Decoder(FastApiSubscribePacket)


def process_message(msg: Packet, exchange_id: str):
    if msg.method == FastApiMethods.SUBSCRIBE:
        param_dict = msg.params
        param_dict["event_id"] = f"{exchange_id}.subscribe"
        if param_dict.get("interval") is None:
            param_dict["interval"] = None
        params = convert(param_dict, FastApiSubscribePacket)
        print(params)
        return params


@router.websocket("/ws/{exchange}/streams")
async def ws_route(websocket: WebSocket, exchange: str):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            msg = packet_decoder.decode(data.encode())
            params = process_message(msg=msg, exchange_id=exchange)
            if params is None:
                print("You did something wrong nigga")
            else:
                await event_bus.publish(params.event_id, params)
        except DecodeError as e:
            print("Invalid request.")
            print(e)
            continue
