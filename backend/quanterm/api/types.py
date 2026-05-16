from enum import StrEnum
from msgspec import Struct


class FastApiMethods(StrEnum):
    SUBSCRIBE = "sub"
    UNSUBSCRIBE = "unsub"
    LIST_STREAMS = "list_streams"


class Packet(Struct):
    method: FastApiMethods
    params: dict
