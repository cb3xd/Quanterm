# Quanterm

A WebSocket gateway for cryptocurrency exchange data, built with FastAPI and an event-driven architecture.

## Overview

Quanterm provides a unified WebSocket interface to subscribe to market data streams from various exchanges (starting with Binance USDT-M futures). The system uses a three-layer abstraction:

1. **FastAPI route** – Thin I/O wrapper for WebSocket connections
2. **EventBus** – Pub/sub routing system that decouples exchange logic from API layer
3. **Exchange handlers** – Exchange-specific logic for mapping streams and managing connections

## Features

-  Single WebSocket connection per exchange multiplexing 600+ streams
-  Lazy subscription model (no pre-subscription overhead)
-  EventBus routing by `event_id` only (zero exchange knowledge in core)
-  Lifespan context manager for reliable startup/shutdown
-  Manual testing verified with wscat
-  Ready for extension to other exchanges (Bybit, MEXC, etc.)

## Architecture

```
Client (wscat)
  ↓
FastAPI route (/ws/{exchange}/streams)
  ↓
EventBus (publish/on pattern)
  ↓
Exchange handler (internal_api.py)
  ↓
Exchange WebSocket backend
```

### Key Components

- **FastAPI WebSocket Route** (`backend/quanterm/api/routes/websocket.py`)
  - Accepts WebSocket connections
  - Parses incoming SUBSCRIBE packets
  - Publishes to EventBus (no business logic)

- **EventBus** (`backend/quanterm/bus/base.py`)
  - Simple `on()` and `publish()` interface
  - Uses `asyncio.TaskGroup` for concurrent listener execution

- **Exchange Handler** (`backend/quanterm/exchange/binanceusdm/internal_api.py`)
  - Lazy subscription via listener
  - Maps internal stream types to exchange-specific formats
  - Singleton WebSocket instance injected via `set_ws(ws)`

- **WebSocket Backend** (`backend/quanterm/exchange/binanceusdm/ws.py`)
  - Inherits from abstract `BaseWS`
  - Handles connection, listening, and message parsing
  - Publishes decoded exchange data to EventBus

## Data Flow

1. Client sends SUBSCRIBE: `{"method": "SUBSCRIBE", "params": {"symbol": "btcusdt", "stream_type": "trade_stream"}}`
2. FastAPI route parses to `FastApiSubscribePacket`
3. `event_bus.publish("binanceusdm.subscribe", packet)`
4. Exchange handler maps to Binance stream: `"btcusdt@aggTrade"`
5. `_ws.subscribe("btcusdt@aggTrade")` sends to Binance
6. Binance pushes trade data
7. Backend decodes and publishes to EventBus with `event_id` = `"binanceusdm.btcusdt.trade_stream"`
8. (Future) EventBus forwards to subscribed clients

## Getting Started

### Prerequisites

- Python 3.12+
- `uvicorn` and `fastapi` (see `backend/requirements.txt` or `pyproject.toml`)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Quanterm

# Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or pip install -e .
```

### Running the Server

```bash
# From backend directory
uvicorn quanterm.api.main:app
```

### Testing with wscat

```bash
# Terminal 1: Start server (as above)

# Terminal 2: Connect and subscribe
wscat -c ws://localhost:8000/ws/binanceusdm/streams

# In wscat:
{"method": "SUBSCRIBE", "params": {"symbol": "btcusdt", "stream_type": "trade_stream"}}

# You should see trade data in the server logs
```

## Project Status

### Completed (MVP)

- FastAPI WebSocket route handler
- EventBus pub/sub integration
- Binance exchange handler
- Stream type mapping (StreamTypes → MarketStreams)
- Kline interval mapping (KlineIntervals → Binance klines)
- Lifespan startup/shutdown
- Lazy subscription
- Data decode & publish
- Manual testing via wscat

### Post-MVP (Planned)

- Send data back to WebSocket client (currently only publishes to EventBus)
- Multi-connection factory for exchanges with connection limits
- Max streams validation
- OKX integration (following same pattern)
- Enhanced error handling
- Backpressure management
- Heartbeat mechanism
- Authentication for private streams

## Adding a New Exchange

1. Create `exchange/<exchange>/ws.py` inheriting from `BaseWS`
2. Create `exchange/<exchange>/internal_api.py` registering listener for `"{exchange}.subscribe"`
3. Create `exchange/<exchange>/streams.py` defining exchange-specific stream enums
4. In `api/main.py` startup: import and call `set_ws()` for the new exchange
5. The FastAPI route automatically routes via the `exchange` path parameter

## Packet Formats

### Client → Server (SUBSCRIBE)

```json
{
  "method": "SUBSCRIBE",
  "params": {
    "symbol": "btcusdt",
    "stream_type": "trade_stream",
    "interval": null
  }
}
```

For kline streams:
```json
{
  "method": "SUBSCRIBE",
  "params": {
    "symbol": "btcusdt",
    "stream_type": "kline_stream",
    "interval": "1m"
  }
}
```

### Internal Packet (FastApiSubscribePacket)

Defined in `backend/quanterm/schemas.py`:
- `event_id`: e.g., `"binanceusdm.subscribe"`
- `symbol`: e.g., `"btcusdt"`
- `stream_type`: `StreamTypes.trade_stream` or `StreamTypes.kline_stream`
- `interval`: `None` or `KlineIntervals.minute` etc.

