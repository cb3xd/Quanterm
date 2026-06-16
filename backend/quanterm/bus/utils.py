from quanterm.exchange.constants import ExchangeID
from quanterm.types import StreamTypes


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
