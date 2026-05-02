import asyncio
from typing import List, Never

from pydantic import TypeAdapter, ValidationError
from quanterm.data.event_bus import EventBus
from quanterm.data.events import (
    OrderbookSchema,
    StreamType,
    TradeSchema,
    TradeWrapper,
    RawOrderbook,
    RawTradeList,
)


class DataNormalizer:
    def __init__(self, event_bus: EventBus) -> None:
        self.orderbook_stream_queue: asyncio.Queue[RawOrderbook] = asyncio.Queue()
        self.trades_stream_queue: asyncio.Queue[RawTradeList] = asyncio.Queue()
        self._bus = event_bus

    async def process_orderbook(self) -> Never:
        while True:
            orderbook: RawOrderbook = await self.orderbook_stream_queue.get()
            try:
                orderbook_validated: OrderbookSchema = OrderbookSchema(**orderbook)
                await self._bus.publish(
                    f"{orderbook_validated.symbol}@{StreamType.ORDERBOOK}",
                    orderbook_validated,
                )
            except Exception as e:
                print(f"Validation failed: {e}")

    async def process_trades(self) -> Never:
        trades_adapter = TypeAdapter(List[TradeWrapper])

        while True:
            trades: RawTradeList = await self.trades_stream_queue.get()
            try:
                validated_batch = trades_adapter.validate_python(trades)
                for wrapper in validated_batch:
                    trade: TradeSchema = wrapper.info
                    await self._bus.publish(
                        f"{trade.symbol}@{StreamType.TRADES}", trade
                    )
            except ValidationError as e:
                print(f"{e}")
