from typing import Any, Callable
from quanterm.exchange.base import Exchange
from quanterm.exchange.constants import ExchangeID

EXCHANGE_REGISTRY: dict[ExchangeID, Callable[[Any], Exchange]] = {}


def register_exchange(exchange_id: ExchangeID):
    def decorator(cls: Callable[[Any], Exchange]) -> Callable[[Any], Exchange]:
        EXCHANGE_REGISTRY[exchange_id] = cls
        return cls

    return decorator
