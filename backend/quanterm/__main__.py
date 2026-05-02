import asyncio
from quanterm.data.event_bus import EventBus
from quanterm.data.events import StreamType
from quanterm.websocket_handlers.websocket_handler import WebsocketHandler
from quanterm.data.data_normalizer import DataNormalizer
from typing import Any


async def store_to_df(data: Any):
    print(data)


async def main():
    bus = EventBus()
    normalizer = DataNormalizer(event_bus=bus)
    ob_outqueue = normalizer.orderbook_stream_queue
    ws_handler = WebsocketHandler(exchange_id="binanceusdm")
    pair = "BTCUSDT"
    bus.on(f"{pair}@{StreamType.ORDERBOOK}", store_to_df)
    ob_stream = await ws_handler.subscribe(
        pair, stream_type=StreamType.ORDERBOOK, out_queue=ob_outqueue
    )
    asyncio.create_task(coro=normalizer.process_trades())
    try:
        await asyncio.sleep(1200)
    finally:
        await ws_handler.close()


if __name__ == "__main__":
    asyncio.run(main())
