from quanterm.data.events import StreamType
from pydantic import BaseModel
import ccxt.pro as ccxtpro
import asyncio


class WebsocketHandler:
    def __init__(self, exchange_id: str, out_queue: asyncio.Queue) -> None:
        self.exchange = getattr(ccxtpro, exchange_id)()
        self.out_queue: asyncio.Queue[Any] = out_queue
        self._active_streams: dict[str, asyncio.Task] = {}

    async def subscribe(self, pair: str, stream_type: StreamType):
        stream_id = f"{pair}@{stream_type}"
        if stream_id in self._active_streams:
            print("Stream already exists!")
            return stream_id
        self._active_streams[stream_id] = asyncio.create_task(
            self._watch_stream(stream_id=stream_id)
        )
        return stream_id

    async def unsubscribe(self, stream_id: str):
        task = self._active_streams.pop(stream_id, None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            print(f"Ended Stream [{stream_id}]")

    async def close(self):
        await self.exchange.close()

    async def _watch_stream(self, stream_id: str):
        backoff = 1
        pair = stream_id.split("@")[0]
        stream_type = stream_id.split("@")[1]
        while self._active_streams.get(stream_id):
            try:
                events = await getattr(self.exchange, stream_type)(pair)
                await self.out_queue.put(events)
                backoff = 1

            except Exception:
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 60)
