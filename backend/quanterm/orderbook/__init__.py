from quanterm.orderbook.types import LocalOrderbook


class Orderbook:
    def __init__(self) -> None:
        self.local_orderbook: LocalOrderbook = {}
