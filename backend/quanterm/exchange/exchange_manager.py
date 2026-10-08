import asyncio
from quanterm.exchange.base import Exchange
from quanterm.exchange.constants import ExchangeID
from quanterm.registries import EXCHANGE_REGISTRY
from quanterm.websocket.base import BaseWS


class ExchangeManager:
    def __init__(self) -> None:
        self._active_exchanges: dict[ExchangeID, Exchange] = EXCHANGE_REGISTRY.list()
        self._websocket_instances: dict[ExchangeID, BaseWS] = {}

    @property
    def active_exchanges(self):
        return self._active_exchanges.copy()

    @property
    def websocket_instances(self):
        return self._websocket_instances.copy()

    def get_exchange(self, exchange_id: ExchangeID) -> Exchange:
        if exchange_id not in self.active_exchanges:
            exchange_class = self._active_exchanges[exchange_id]
            if not exchange_class:
                raise ValueError(f"Exchange {exchange_id} was never registered!")

            self._active_exchanges[exchange_id] = exchange_class
        return self._active_exchanges[exchange_id]

    async def connect_all_websockets(self):
        if not self.active_exchanges:
            return
        tasks = [
            exchange.connect_websocket() for exchange in self.active_exchanges.values()
        ]
        await asyncio.gather(*tasks)

    async def close_all(self):
        await asyncio.gather(
            *[exchange.close() for exchange in self.active_exchanges.values()]
        )
