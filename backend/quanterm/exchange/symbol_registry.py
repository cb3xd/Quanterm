from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.registry import exchange_registry


class SymbolRegistry:
    def __init__(self) -> None:
        self.supported_symbols: dict[str, set[ExchangeID]] = {}
        self.formatted_symbols: dict[str, str] = {}
        self.active_exchanges = exchange_registry

    async def _get_all_symbols(self):
        for exchange_id, exchange_instance in self.active_exchanges.items():
            try:
                symbols = await exchange_instance.api.fetch_symbols()
                for symbol in symbols:
                    self.supported_symbols.setdefault(symbol, set()).add(exchange_id)
                    self.formatted_symbols.setdefault(symbol.replace("-", ""), symbol)

            except Exception as e:
                print(f"Error fetching from {exchange_id}: {e}")

        return self.supported_symbols

    async def get_all_symbols(self):
        if self.supported_symbols:
            return self.supported_symbols.copy()
        else:
            symbols = await self._get_all_symbols()
            return symbols

    def get_dash_format(self, symbol):
        return self.formatted_symbols.get(symbol)


symbol_registry = SymbolRegistry()
