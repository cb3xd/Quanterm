import asyncio
from quanterm.data.events import OrderbookSchema, TradesSchema

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
    
    async def process_trades(self):
        while True:
            trades = await self.trades_stream_queue.get()
            try:
                for trade in trades:
                    trade_validated = TradesSchema(**trade['info'])
                    print(
                        f"[{trade_validated.order_type}] {trade_validated.symbol} {trade_validated.quantity}@{trade_validated.price}"
                    )
            except Exception as e:
                print(f"")

