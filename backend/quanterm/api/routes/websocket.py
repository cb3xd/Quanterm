import asyncio
from typing import Any
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from msgspec import DecodeError, Struct, convert, json, to_builtins
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
    if msg.method != FastApiMethods.SUBSCRIBE:
        return None
    param_dict = msg.params
    param_dict["event_id"] = f"{param_dict.get('exchange_id')}.subscribe"

    return convert(param_dict, FastApiSubscribePacket)


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
            # 1. Listen for new inbound messages
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

            # Prevent duplicate event bus listeners for the same connection
            if event_id in listeners:
                continue

            # 2. Defensive closure with a strict write timeout
            def make_callback(eid):
                async def send_to_client(data: Struct):
                    try:
                        print(data)
                        await asyncio.wait_for(
                            websocket.send_bytes(encoder.encode(data)),
                            timeout=1,
                        )
                    except Exception as e:
                        print(e)
                        # Auto-evict from the local tracker if writes fail
                        if eid in listeners:
                            try:
                                listeners[eid].unregister()
                            except Exception:
                                pass
                            del listeners[eid]

                return send_to_client

            # Attach to the global event bus
            listener = event_bus.on(event_id, make_callback(event_id))
            listeners[event_id] = listener

            # Fire-and-forget publish execution
            await event_bus.publish(params.event_id, params)

        except WebSocketDisconnect:
            # Caught first! Prevents normal disconnections from spamming your error logs
            print("ℹ️ Client disconnected cleanly.")
            break

        except DecodeError:
            print("❌ Invalid packet format.")
            continue

        except Exception as e:
            import traceback

            # Safety net for actual unexpected system code crashes
            print("⚠️ Unexpected crash detected inside WS loop.")
            traceback.print_exception(e)
            break


@router.websocket("/ws")
async def ws_route(websocket: WebSocket):
    await websocket.accept()
    listeners: dict[str, Any] = {}

    try:
        await ws_loop(websocket=websocket, listeners=listeners)
    finally:
        # This block is structurally guaranteed to run by the python runtime,
        # even if Uvicorn forcefully cancels the task via an asyncio.CancelledError.
        print(
            f"🧹 Sweeping up: Clearing {len(listeners)} active event bus listeners..."
        )
        for listener in list(listeners.values()):
            try:
                listener.unregister()
            except Exception:
                pass
