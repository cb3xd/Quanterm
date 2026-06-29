import asyncio
from collections import deque
import time

import msgspec
import websockets

import httpx

encoder = msgspec.json.Encoder()
FAPI_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"
BATCH_SIZE = 100


def fetch_symbols() -> dict[str, list[str]]:
    """Fetch {symbol: [exchange_ids]} from the API."""
    resp = httpx.get(f"{FAPI_URL}/api/all_exchange_symbols")
    resp.raise_for_status()
    return resp.json()


def build_subscribe_packets(
    symbols_by_exchange: dict[str, list[str]],
    batch_size: int = BATCH_SIZE,
) -> list[bytes]:
    """
    Build subscribe packets per exchange, chunked into batches.
    Binance limits ~200 params per SUBSCRIBE message, so we default to 100.
    """
    exchange_symbols: dict[str, list[str]] = {}
    for symbol, exchanges in symbols_by_exchange.items():
        for exchange in exchanges:
            exchange_symbols.setdefault(exchange, []).append(symbol)

    packets = []
    for exchange, symbols in exchange_symbols.items():
        events = [f"kline_stream.{s}.1m" for s in symbols]
        # Chunk into batches
        for i in range(0, len(events), batch_size):
            chunk = events[i : i + batch_size]
            packet = encoder.encode(
                {
                    "method": "sub",
                    "events": chunk,
                    "exchange": exchange,
                }
            )
            packets.append(packet)
    return packets


decoder = msgspec.json.Decoder()


async def test():
    symbols = fetch_symbols()
    symbols = dict(list(symbols.items())[: len(symbols)])
    total = sum(len(v) for v in symbols.values())
    print(f"Fetched {len(symbols)} unique symbols ({total} symbol-exchange pairs)")

    packets = build_subscribe_packets(symbols)[:10]
    print(f"Built {len(packets)} subscribe packet(s) (batch size: {BATCH_SIZE})")
    for i, pkt in enumerate(packets):
        decoded = msgspec.json.decode(pkt)
        print(
            f"  Packet {i}: exchange={decoded['exchange']}, "
            f"events={len(decoded['events'])}"
        )

    async with websockets.connect(
        WS_URL,
        ping_interval=20,
        ping_timeout=10,
        close_timeout=5,
    ) as ws:
        for pkt in packets:
            await ws.send(pkt)
        print("\nSubscribed. Listening for events...\n")
        try:
            samples = deque(maxlen=5000)
            while True:
                msg = await ws.recv()
                decoded = decoder.decode(msg)
                samples.append(
                    round((time.time() * 1000) - decoded.get("event_time"), 2)
                )
                print(
                    f" \rLatency: {round(sum(samples) / len(samples))}ms",
                    end="",
                    flush=True,
                )

        except websockets.ConnectionClosed:
            print("Connection closed by server.")
        except KeyboardInterrupt:
            print("\nUser interrupted. Closing...")
            await ws.close()


asyncio.run(test())
