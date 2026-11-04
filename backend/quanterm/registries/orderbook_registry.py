from quanterm.exchange import ExchangeID
from quanterm.orderbook import Orderbook
from quanterm.registries.base import Registry

OrderbookRegistryModel = Registry[ExchangeID, Orderbook]
ORDERBOOK_REGISTRY: OrderbookRegistryModel = Registry[ExchangeID, Orderbook]()
