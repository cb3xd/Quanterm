from schemas import MiniTicker, AggregateTickers
from typing import Any


class MiniTickerStreamHandler:
    def __init__(self) -> None:
        self.previous_state: dict[str, MiniTicker] = {}

    async def process(self, raw_data: Any) -> None: # Change return type to None
        raw_list = raw_data.get("data", raw_data)
        tickers = [MiniTicker.model_validate(t) for t in raw_list]
        self.previous_state.update({ticker.symbol: ticker for ticker in tickers})

    def get_ticker(self, symbol: str) -> MiniTicker | None:
        return self.previous_state.get(symbol)

    def get_aggregate_tickers(self) -> AggregateTickers:
        """Returns an AggregateTickers object with the current state."""
        return AggregateTickers(tickers=self.previous_state.copy())
