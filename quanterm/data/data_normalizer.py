import asyncio
from typing import Never
from quanterm.data.events import OrderbookSchema, TradesSchema, RawOrderbook, RawTradeList

class DataNormalizer:
    def __init__(self) -> None:
        self.orderbook_stream_queue: asyncio.Queue[RawOrderbook] = asyncio.Queue()
        self.trades_stream_queue : asyncio.Queue[RawTradeList]= asyncio.Queue()

    async def process_orderbook(self) -> Never:
        while True:
            orderbook : RawOrderbook= await self.orderbook_stream_queue.get()
            try:
                orderbook_validated: OrderbookSchema = OrderbookSchema(**orderbook)
                print(
                    f"Validated Orderbook: {orderbook_validated.bids[0]}:{orderbook_validated.asks[0]}"
                )
                # publish (orderbook_validated)
            except Exception as e:
                print(f"Validation failed: {e}")
    
    async def process_trades(self)-> Never:
        while True:
            trades : RawTradeList= await self.trades_stream_queue.get()
            try:
                for trade in trades:
                    trade_validated: TradesSchema = TradesSchema(**trade['info'])
                    print(
                        f"[{trade_validated.order_type}] {trade_validated.symbol} {trade_validated.quantity}@{trade_validated.price}"
                    )
            except Exception as e:
                print(f"")

