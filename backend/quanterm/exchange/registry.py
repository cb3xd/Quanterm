from typing import Callable

from quanterm.exchange.base import Exchange
from quanterm.exchange.constants import ExchangeID

exchange_registry: dict[ExchangeID, Callable[..., Exchange]] = {}


def register_exchange(exchange_id: ExchangeID):
    def decorator(cls: Callable[..., Exchange]) -> Callable[..., Exchange]:
        exchange_registry[exchange_id] = cls
        return cls

    return decorator
