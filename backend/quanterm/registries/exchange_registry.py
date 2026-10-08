from __future__ import annotations

import logging
from collections.abc import Callable

from quanterm.exchange.base import Exchange
from quanterm.exchange.constants import ExchangeID
from quanterm.registries.base import Registry


class ExchangeRegistry(Registry[ExchangeID, Exchange]):
    def __init__(self) -> None:
        super().__init__()

    def register_exchange(self, exchange_id: ExchangeID):

        def decorator(cls: Callable[..., Exchange]) -> Callable[..., Exchange]:
            self._entries[exchange_id] = cls()
            logging.getLogger("uvicorn").info(f"registering {exchange_id}")
            return cls

        return decorator
