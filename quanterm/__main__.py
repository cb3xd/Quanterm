import asyncio
from quanterm.data.event_bus import EventBus
from quanterm.data.events import StreamType
from quanterm.websocket_handlers.websocket_handler import WebsocketHandler
from quanterm.data.data_normalizer import DataNormalizer
from rich.table import Table
from rich.console import Console
from typing import Any

console = Console()


async def display_orderbook(data: Any):
    print("Orderbook Received")


async def display_trades(data: Any):
    print("Trades Received")


async def main():
    bus = EventBus()
    normalizer = DataNormalizer(event_bus=bus)
    trades_outqueue = normalizer.trades_stream_queue
    ws_handler = WebsocketHandler(exchange_id="binanceusdm")
    pair = "BTCUSDT"
    bus.on(f"{pair}@{StreamType.TRADES}", display_trades)
    trades_stream = await ws_handler.subscribe(
        pair, stream_type=StreamType.TRADES, out_queue=trades_outqueue
    )
    asyncio.create_task(coro=normalizer.process_trades())
    try:
        await asyncio.sleep(1200)
    finally:
        await ws_handler.close()


if __name__ == "__main__":
    asyncio.run(main())
