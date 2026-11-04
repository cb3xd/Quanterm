from msgspec import Struct

Price = str
Quantity = str

Bids = list[Price | Quantity]
Asks = Bids


class LocalOrderbook(Struct):
    symbol: str
    event_time: int
    transaction_time: int
    bids: Bids
    asks: Asks


class Orderbook:
    def __init__(self) -> None:
        self.local_orderbook: LocalOrderbook
