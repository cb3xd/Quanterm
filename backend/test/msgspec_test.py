import msgspec
from typing import Callable, Union


class TradePacket(msgspec.Struct):
    symbol: str
    price: str
    quantity: str
    time: int


class OrderbookPacket(msgspec.Struct):
    symbol: str
    bids: list
    asks: list


# 2. Subclasses define the expected routing value (tag) and map the divergent JSON keys
class ABCTradeEvent(TradePacket, tag_field="e", tag="aggTrade"):
    symbol: str = msgspec.field(name="s")
    price: str = msgspec.field(name="p")
    quantity: str = msgspec.field(name="q")
    time: int = msgspec.field(name="t")


class ABCDepthEvent(OrderbookPacket, tag_field="e", tag="depthUpdate"):
    symbol: str = msgspec.field(name="s")
    bids: list = msgspec.field(name="b")
    asks: list = msgspec.field(name="a")


# 3. Use standard Python Union (or AggTradeEvent | DepthEvent in 3.10+)
StreamRouterType = Union[ABCTradeEvent, ABCDepthEvent]

# 4. Pass the union directly to the Decoder
decoder = msgspec.json.Decoder(StreamRouterType)

# Execution
payload_trade = b'{"e": "aggTrade", "s": "BTCUSDT", "p": "60000", "q": "10", "t": 100}'
payload_depth = b'{"e":"depthUpdate","s":"ETHUSDT","b":[["3000","1"]], "a":[]}'


def map_trade(packet: ABCTradeEvent):
    return TradePacket(
        symbol=packet.symbol,
        price=packet.price,
        quantity=packet.quantity,
        time=packet.time,
    )


def map_depth(packet: ABCDepthEvent):
    return OrderbookPacket(symbol=packet.symbol, bids=packet.bids, asks=packet.asks)


hash_map: dict[type[msgspec.Struct], Callable] = {
    ABCTradeEvent: map_trade,
    ABCDepthEvent: map_depth,
}

abc_trade_packet = decoder.decode(payload_trade)
trade_packet: Callable = hash_map.get(type(abc_trade_packet))(abc_trade_packet)
print(trade_packet)
print(msgspec.json.encode(trade_packet))
