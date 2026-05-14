from quanterm.exchange.base import ExchangeID, StreamTypes


def generate_event_id(
    exchange_id: ExchangeID, symbol: str, event_type: StreamTypes
) -> int:

    symbol_hash = hash(symbol) & 0xFFFFFF
    event_id = (exchange_id << 32) | (event_type << 24) | symbol_hash
    print(event_id)
    return event_id
