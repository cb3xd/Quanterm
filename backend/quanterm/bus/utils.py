from quanterm.exchange.constants import ExchangeID
from quanterm.types import KlineIntervals, StreamTypes


def generate_event_id(
    exchange_id: ExchangeID,
    symbol: str,
    event_type: StreamTypes,
    extra: str | None = None,
) -> str:

    event_id = f"{exchange_id}.{event_type}.{symbol}".lower()

    if extra:
        event_id += f".{extra}"
    return event_id


def validate_event_id(event_id: str):
    parts = event_id.split(".")

    if parts.__len__() < 2:
        return
    if parts[0] not in StreamTypes._value2member_map_:
        print(f"[{event_id}] Invalid stream type: {parts[1]}")
        return
    if parts[2] and parts[2] not in KlineIntervals._value2member_map_:
        print(f"[{event_id}] Invalid interval: {parts[2]}")
        return

    return event_id
