# Quanterm Codebase

## Overview
Python async cryptocurrency trading terminal. Focuses on real-time market data streaming via Binance WebSocket API.

## Tech Stack
- Python 3.10+
- ccxt.pro (async WebSocket)
- pydantic (data validation)
- asyncio (concurrency)
- queue (thread-safe Queue for cross-task communication)

## Structure
- `quanterm/__main__.py` — Entry point. Connects, subscribes, processes orderbook.
- `quanterm/exchange/binance/` — Binance WebSocket client.
  - `binance_websocket.py` — `WebsocketHandler` (subscribe/unsubscribe/close, backoff).
  - `handlers/` — Protocol `DataStreamHandler`, `KlineStreamHandler`, `MiniTickerStreamHandler`.
- `quanterm/data/stream_types.py` — `StreamType` StrEnum (ORDERBOOK, TICKER, OHLCV, TRADES).
- `quanterm/data/schemas/` — Pydantic models (`KlineTick`, `MiniTicker`, `AggregateTickers`).
- `.gitignore` — Standard Python, cache, env, logs, IDE patterns.

## Key Files
- `quanterm/__main__.py` — Main async entry.
- `quanterm/exchange/binance/binance_websocket.py` — Core WebSocket handler.
- `quanterm/data/stream_types.py` — Stream type enum.
- `quanterm/data/schemas/kline.py` — KlineTick schema.
- `quanterm/data/schemas/mini_ticker.py` — MiniTicker & AggregateTickers schemas.
- `quanterm/exchange/binance/handlers/mini_ticker_handler.py` — MiniTicker processing.
- `quanterm/exchange/binance/handlers/kline_handler.py` — Kline processing.
- `quanterm/exchange/binance/handlers/base.py` — DataStreamHandler protocol.

## Run
```bash
python -m quanterm
```
Async main connects to Binance USDM orderbook stream, subscribes BTC/USDT:USDT, prints events, unsub after 2s.

## Notes
- Uses `asyncio.Queue` for inter-task communication; `queue.Queue` in main for thread safety.
- Backoff strategy: exponential up to 60s on stream errors.
- Models use `populate_by_name` for alias/field mapping.