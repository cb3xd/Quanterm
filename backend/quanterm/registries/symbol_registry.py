from quanterm.exchange.constants import ExchangeID
from quanterm.registries.base import Registry


class SymbolRegistry:
    def __init__(self) -> None:
        self._supported_symbols = Registry[str, set[ExchangeID]]()
        self._formatted_symbols = Registry[str, str]()

    async def _get_all_symbols(self):
        from quanterm.registries import EXCHANGE_REGISTRY

        _active_exchanges = EXCHANGE_REGISTRY.list()

        for exchange_id, exchange_instance in _active_exchanges.items():
            symbols = await exchange_instance.api.fetch_symbols()
            for symbol in symbols:
                self._supported_symbols.setdefault(symbol, set()).add(exchange_id)
                self._formatted_symbols.setdefault(symbol.replace("-", ""), symbol)

        return self._supported_symbols.list()

    async def get_all_symbols(self):
        if self._supported_symbols.list():
            return self._supported_symbols.list()
        else:
            symbols = await self._get_all_symbols()
            return symbols

    def get_dash_format(self, symbol):
        return self._formatted_symbols.get(symbol)
