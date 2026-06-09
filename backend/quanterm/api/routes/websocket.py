import asyncio
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from msgspec import Struct, DecodeError
import msgspec
from msgspec.json import Encoder
from quanterm.api.socket_types import PACKET_DECODER, Packet
from quanterm.bus.base import get_event_bus

event_bus = get_event_bus()
router = APIRouter()
encoder = Encoder()


async def ws_loop(websocket: WebSocket, listeners: dict):
    while True:
        try:
            data = await websocket.receive_bytes()
            msg = PACKET_DECODER.decode(data)
            print(msg)
        except WebSocketDisconnect:
            print("ℹ️ Client disconnected cleanly.")
            break

        except DecodeError as e:
            import traceback

            print("❌ Invalid packet format.")
            traceback.print_exception(e)
            break

        except ValueError:
            await websocket.send_text("Invalid packet format.")
            break

        except Exception as e:
            import traceback

            # Safety net for actual unexpected system code crashes
            print("⚠️ Unexpected crash detected inside WS loop.")
            traceback.print_exception(e)
            break


@router.websocket("/ws")
async def ws_route(websocket: WebSocket):
    await websocket.accept()
    listeners = {}

    try:
        await ws_loop(websocket=websocket, listeners=listeners)
    finally:
        print(
            f"🧹 Sweeping up: Clearing {len(listeners)} active event bus listeners..."
        )
        for listener in set(listeners.values()):
            try:
                listener.unregister()
            except Exception:
                pass
