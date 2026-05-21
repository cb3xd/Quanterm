from typing import Any
from fastapi import WebSocket, APIRouter
from msgspec import DecodeError, Struct, json, to_builtins
from quanterm.api.types import FastApiMethods, Packet
from quanterm.bus.base import get_event_bus
from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import FastApiSubscribePacket
from quanterm.types import KlineIntervals, StreamTypes

event_bus = get_event_bus()
router = APIRouter()


class Parameters(Struct):
    symbol: str
    event_id: str
    exchange_id: ExchangeID
    stream_type: StreamTypes
    interval: KlineIntervals


packet_decoder = json.Decoder(Packet)
encoder = json.Encoder()
sub_decoder = json.Decoder(FastApiSubscribePacket)


def process_message(msg: Packet):
    if msg.method == FastApiMethods.SUBSCRIBE:
        param_dict = msg.params
        param_dict["event_id"] = f"{param_dict.get('exchange_id')}.subscribe"
        if param_dict.get("interval") is None:
            param_dict["interval"] = None
        params_encoded = encoder.encode(param_dict)
        params = sub_decoder.decode(params_encoded)
        return params


def generate_event_id(
    exchange_id: str,
    symbol: str,
    stream_type: StreamTypes,
    interval: KlineIntervals | None,
):
    event_id = f"{exchange_id}.{symbol}.{stream_type}"
    if interval:
        event_id += f".{interval}"
    return event_id


async def ws_loop(websocket: WebSocket, listeners: dict[str, Any]):
    while True:
        try:
            data = await websocket.receive_text()
            msg = packet_decoder.decode(data.encode())
            params = process_message(msg=msg)
            if params is None:
                continue

            exchange_id = params.event_id.split(".")[0]
            event_id = generate_event_id(
                exchange_id,
                params.symbol,
                params.stream_type,
                params.interval,
            )

            async def send_to_client(data: Struct):
                try:
                    await websocket.send_json(to_builtins(data))
                except Exception as e:
                    print(e)

            listener = event_bus.on(event_id, send_to_client)
            listeners[event_id] = listener
            await event_bus.publish(params.event_id, params)
        except DecodeError as e:
            print("Invalid request.")
            print(e)
            continue
        except Exception as e:
            print(f"WS Error: {e}")
            break


@router.websocket("/ws")
async def ws_route(websocket: WebSocket):
    await websocket.accept()
    listeners: dict[str, Any] = {}
    await ws_loop(websocket=websocket, listeners=listeners)
    for listener in listeners.values():
        listener.unregister()
