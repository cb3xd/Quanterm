import asyncio
from typing import Any
from quanterm.data.events import StreamType, OrderbookSchema, TradesSchema
from quanterm.websocket_handlers.websocket_handler import WebsocketHandler


class DataNormalizer:
    def __init__(self) -> None:
        self.orderbook_stream_queue = asyncio.Queue()
        self.trades_stream_queue = asyncio.Queue()

    async def process_orderbook(self):
        while True:
            orderbook = await self.orderbook_stream_queue.get()
            try:
                orderbook_validated = OrderbookSchema(**orderbook)
                print(
                    f"Validated Orderbook: {orderbook_validated.bids[0]}:{orderbook_validated.asks[0]}"
                )
                # publish (orderbook_validated)
            except Exception as e:
                print(f"Validation failed: {e}")


async def main():
    normalizer = DataNormalizer()
    out_queue = normalizer.orderbook_stream_queue
    ws_handler = WebsocketHandler("binanceusdm", out_queue=out_queue)
    pair = "BTC/USDT:USDT"
    stream_type = StreamType.ORDERBOOK
    ticker_stream = await ws_handler.subscribe(pair, stream_type)
    asyncio.create_task(normalizer.process_orderbook())
    await asyncio.sleep(2)
    await ws_handler.unsubscribe(ticker_stream)
    await ws_handler.close()


if __name__ == "__main__":
    asyncio.run(main())
