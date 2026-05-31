from typing import Any, Callable
from quanterm.exchange.base import Exchange
from quanterm.exchange.constants import ExchangeID

exchange_registry: dict[ExchangeID, Callable[[Any], Exchange]] = {}


def register_exchange(exchange_id: ExchangeID):
    def decorator(cls: Callable[[Any], Exchange]) -> Callable[[Any], Exchange]:
        exchange_registry[exchange_id] = cls
        return cls

    return decorator
