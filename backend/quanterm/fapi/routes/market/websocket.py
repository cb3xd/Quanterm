from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


async def websocket_loop(websocket: WebSocket):
    while True:
        try:
            data = await websocket.receive_bytes()
            print(data)
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
