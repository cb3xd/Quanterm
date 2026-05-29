from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager


class SymbolRegistry:
    def __init__(self) -> None:
        self.supported_symbols: dict[str, set[ExchangeID]] = {}
        self.active_exchanges = manager.active_exchanges

    async def get_all_symbols(self):
        for exchange_id, exchange_instance in self.active_exchanges.items():
            try:
                symbols = await exchange_instance.api.fetch_symbols()
                for symbol in symbols:
                    self.supported_symbols.setdefault(symbol, set()).add(exchange_id)

            except Exception as e:
                print(f"Error fetching from {exchange_id}: {e}")

        return self.supported_symbols


symbol_registry = SymbolRegistry()
