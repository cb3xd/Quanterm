import msgspec
from typing import Union

from msgspec.json import Encoder


class UniversalTradePacket(msgspec.Struct):
    symbol: str
    price: str


# 1. Base struct defines the shared attributes and the JSON routing key (tag_field)
class UniversalStreamEvent(msgspec.Struct, tag_field="e"):
    symbol: str


# 2. Subclasses define the expected routing value (tag) and map the divergent JSON keys
class AggTradeEvent(UniversalStreamEvent, tag="aggTrade"):
    symbol: str = msgspec.field(name="s")
    price: str = msgspec.field(name="p")


class DepthEvent(UniversalStreamEvent, tag="depthUpdate"):
    symbol: str = msgspec.field(name="s")
    bids: list = msgspec.field(name="b")


# 3. Use standard Python Union (or AggTradeEvent | DepthEvent in 3.10+)
StreamRouterType = Union[AggTradeEvent, DepthEvent]

# 4. Pass the union directly to the Decoder
decoder = msgspec.json.Decoder(StreamRouterType)

# Execution
payload_trade = b'{"e":"aggTrade","s":"BTCUSDT","p":"60000"}'
payload_depth = b'{"e":"depthUpdate","s":"ETHUSDT","b":[["3000","1"]]}'

trade = decoder.decode(payload_trade)
depth = decoder.decode(payload_depth)
print(trade)
print(depth)

encoder = Encoder()

print(encoder.encode(trade))
universal_trade = UniversalTradePacket(symbol=trade.symbol, price=trade.price)
print(universal_trade)
print(encoder.encode(universal_trade))
