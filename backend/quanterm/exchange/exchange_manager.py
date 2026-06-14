import asyncio
from quanterm.bus.base import get_event_bus
from quanterm.exchange.base import Exchange
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.registry import exchange_registry
from quanterm.websocket.base import BaseWS


class ExchangeManager:
    def __init__(self) -> None:
        self._active_exchanges: dict[ExchangeID, Exchange] = exchange_registry
        self._websocket_instances: dict[ExchangeID, BaseWS] = {}
        self._event_bus = get_event_bus()

    @property
    def active_exchanges(self):
        return self._active_exchanges.copy()

    @property
    def websocket_instances(self):
        return self._websocket_instances.copy()

    def get_exchange(self, exchange_id: ExchangeID) -> Exchange:
        if exchange_id not in self.active_exchanges:
            exchange_class = exchange_registry[exchange_id]
            if not exchange_class:
                raise ValueError(f"Exchange {exchange_id} was never registered!")

            self._active_exchanges[exchange_id] = exchange_class
        return self._active_exchanges[exchange_id]

    async def connect_all_websockets(self):
        if not self.active_exchanges:
            print("No active exchanges to connect.")
            return
        print(f"Connecting websockets for {len(self.active_exchanges)} exchanges.")
        tasks = [
            exchange.connect_websocket() for exchange in self.active_exchanges.values()
        ]
        await asyncio.gather(*tasks)


manager = ExchangeManager()
