from enum import StrEnum
from msgspec import Struct, field
from msgspec.json import Decoder
from quanterm.exchange.constants import ExchangeID


class FastApiMethods(StrEnum):
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"
    LIST_STREAMS = "list_streams"


class Packet(Struct, tag_field="method"):
    pass


class SubscribePacket(Packet, tag=str(FastApiMethods.SUBSCRIBE)):
    exchange_id: ExchangeID
    events: set[str] = field(name="events")


class UnsubscribePacket(Packet, tag=str(FastApiMethods.UNSUBSCRIBE)):
    exchange_id: ExchangeID
    events: set[str] = field(name="events")


PACKET_DECODER = Decoder(SubscribePacket | UnsubscribePacket)
