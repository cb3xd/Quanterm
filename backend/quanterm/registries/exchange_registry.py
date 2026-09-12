from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from quanterm.exchange.constants import ExchangeID

if TYPE_CHECKING:
    from quanterm.exchange.base import Exchange

_exchange_registry: dict[ExchangeID, Exchange] = {}


def get_registry():
    return _exchange_registry.copy()


def register_exchange(exchange_id: ExchangeID):
    def decorator(cls: Callable[..., Exchange]) -> Callable[..., Exchange]:
        _exchange_registry[exchange_id] = cls()
        return cls

    return decorator
