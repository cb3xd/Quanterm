import threading
from typing import Any, overload

from quanterm.registries.exchange_registry import ExchangeRegistry
from quanterm.registries.stream_registry import StreamRegistry
from quanterm.registries.symbol_registry import SymbolRegistry

SYMBOL_REGISTRY = SymbolRegistry()
STREAM_REGISTRY = StreamRegistry()
EXCHANGE_REGISTRY = ExchangeRegistry()
