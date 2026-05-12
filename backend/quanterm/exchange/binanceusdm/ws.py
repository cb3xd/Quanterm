import asyncio
import websockets
import json
from quanterm.websocket.base import BaseWS


class BinanceWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self.uri = "wss://fstream.binance.com/market/stream"

    async def connect(self) -> None:
        self.websocket = await websockets.connect(self.uri)
        self._watch_task = asyncio.create_task(self._listen())

    async def disconnect(self) -> None:
        if self._watch_task:
            self._watch_task.cancel()
            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass

            self._watch_task = None

        if self.websocket:
            await self.websocket.close()
            self.websocket = None

        print("WS Disconnected")

    async def subscribe(self, stream_id: str):
        if self.websocket is None:
            print("Connect first.")
            return
        if stream_id in self.active_streams:
            print(f"[{stream_id}] Stream already exists!")
            return

        self.active_streams.add(stream_id)
        subscribe_message = {"method": "SUBSCRIBE", "params": [stream_id], "id": 1}

        await self.websocket.send(json.dumps(subscribe_message))

    async def unsubscribe(self, stream_id: str):
        if self.websocket is None:
            print("Connect first.")
            return

        if stream_id in self.active_streams:
            unsub_message = {"method": "UNSUBSCRIBE", "params": [stream_id]}
            self.active_streams.remove(stream_id)
            await self.websocket.send(json.dumps(unsub_message))
        else:
            print(f"Stream {stream_id} does not exist!")

    async def _on_message(self, raw):
        print(f"Processing: {raw}")
