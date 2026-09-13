import asyncio
import logging
from typing import override

import msgspec
import websockets

from quanterm.websocket.base import BaseWS


class BybitWebsocket(BaseWS):
    def __init__(self) -> None:
        super().__init__()
        self.uri = "wss://stream.bybit.com/v5/public/linear"
        self.encoder = msgspec.json.Encoder()
        self.max_streams = 500
        self._reconnect_delay = 1.0
        self._max_delay = 60.0

    @override
    async def connect(self) -> None:
        delay = self._reconnect_delay
        try:
            self.websocket: (
                websockets.ClientConnection | None
            ) = await websockets.connect(self.uri, ping_interval=20, ping_timeout=10)
            self._reconnect_delay = 1.0
            self._watch_task: asyncio.Task[None] | None = asyncio.create_task(
                self._listen()
            )
        except (TimeoutError, OSError, websockets.WebSocketException) as e:
            logging.getLogger("uvicorn").warning(f"Bybit WS reconnect in {delay}s: {e}")
            await asyncio.sleep(delay)
            self._reconnect_delay = min(delay * 2, self._max_delay)
            await self.connect()
