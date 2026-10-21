Price = str
Quantity = str
LocalOrderbook = dict[Price, Quantity]


class Orderbook:
    def __init__(self) -> None:
        self.local_orderbook: LocalOrderbook = {}
