from quanterm.exchange.constants import ExchangeID
from quanterm.orderbook import Orderbook
from quanterm.registries.base import Registry

OrderbookRegistryModel = Registry[ExchangeID, Orderbook]
OrderbookRegistry: OrderbookRegistryModel = Registry[ExchangeID, Orderbook]()
