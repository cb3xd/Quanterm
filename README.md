
# Quanterm
Charting and analysis app for crypto/defi

## Overview
I found that Tradingview is way too slow in updating price and its backtesting engine inefficient and inaccurate. Quanterm aims to solve all of that.

## Architecture
**Backend (Python) - backend/quanterm/**

**Framework:** FastAPI + WebSockets, using msgspec for fast serialization and asyncio for concurrency.

| Layer                      | What it does                                                                                                       | Key files                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| **API Layer**              | WebSocket + REST endpoints, parses client subscribe requests                                                       | *api/main.py, api/routes/websocket.py, api/routes/symbols.py*                                   |
| **EventBus**               | In-memory pub/sub that decouples data ingestion from distribution. Uses asyncio.TaskGroup for fan-out.             | *bus/base.py, bus/utils.py*                                                                     |
| **Exchange abstractions**  | Pluggable exchange system. Base classes for exchange connections, bridges, and WebSocket clients                   | *exchange/base.py, exchange/base_bridge.py, exchange/exchange_manager.py, exchange/registry.py* |
| **Binance USDM**           | Concrete Binance Futures implementation. WebSocket client, REST symbol fetcher, stream mappers for trades & klines | *exchamge/binanceusdm/ws.py, client.py, bridge.py, schemas.py, external_api.py*                 |
| **Shared types & schemas** | Core enums (StreamTypes, KlineIntervals), packet structs (TradePacket, KlinePacket, FastApiSubscribePacket)        | *types.py, schemas.py*                                                                          |

**Data flow:** Client sends sub packet -> FastAPI route -> EventBus -> Binance bridge translates to exchagne stream ID -> Binance WebSocket -> decoded data published back to EventBus -> (future) pushed to subscribed clients.

Features:
- Lazy subscription model (WebSocket only connects and adds a stream when a client asks)
- Single WebSocket connection per exchange
- Exchange registration via decorator pattern for easy extension
- LifeSpan context manager for clean startup and shutdown

**Frontend (Svelte) - frontend/**

**Stack**: Svelte 5 + Vite + Tailwind CSS + shadcn-svelte (Lyra style)

| Part                | What it does                                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------------------------- |
| App.svelte          | Root component (Temporary MVP) - Fetches symbols from backend on mount, renders a searchable, scrollable symbol list. |
| dataStore.svelte.js | Reactive store that fetches GET /api/all_exchange_symbols and exposes data/loading/error states.                      |
| UI components       | shadcn stuffs                                                                                                         |
| Styling             | Dark/light CSS variables, JetBrains Mono, shadcn-svelte + tw-animate-css                                              |

The frontend is still in its early stage.
## Tech Stack

|                   | Backend              | Frontend                                  |
| ----------------- | -------------------- | ----------------------------------------- |
| Language          | Python 3.12+         | JavaScript (ES Modules) (Typescript soon) |
| Framework         | FastAPI              | Svelte 5                                  |
| Build             | Hachling / pip       | Vite 8                                    |
| Styling           | -                    | Tailwind CSS + shadcn-svelte              |
| Data Validation   | msgspec              | -                                         |
| Exchange Protocol | aiohttp + websockets | -                                         |
| Package Manager   | pip                  | Bun                                       |

## Getting Started
```bash
git clone https://github.com/cb3xd/quanterm.git
cd Quanterm
```

backend:
```bash
cd backend && python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn quanterm.api.main:app
```
Runs at `localhost:8000`

frontend:
```bash
cd frontend
bun install
bun run dev
```
Runs at `localhost:5173` (Vite default)

**Performance**

To make our beloved silicon chips dont explode, test with this script and monitor with task manager or btop/htop filtering for uvicorn.

The script subscribes to all pairs available 
```bash
python test/perf_test.py
```

**Usage Options**

Run with a custom duration, default is 30 seconds:
```bash
python test/perf_test.py --duration 60
```

Enable system resource monitoring (CPU/Memory tracking):
```bash
python test/perf_test.py --monitor
```

You can also combine options:
```bash
python test/perf_test.py --duration 120 --monitor --verbose
```

**What to Expect**

The script will
1. Fetch all available trading pairs from the backend
2. Subscribe to each pair's trade stream sequentially (0.15s delay between each to avoid getting rate limited by the exchange)
3. Measure throughput, latency, and error rates during the test window
4. Output results to console and save metrics to perf_results.json

**Test Results**

System specs: Intel i5 10th gen with 16 GB RAM

```bash
python test/perf_test.py --monitor --duration 60
```

| Metric                    | Value         |
| ------------------------- | ------------- |
| Active Streams Subscribed | 747           |
| Messages Received         | 76,999        |
| Throughput                | 1,283.3 msg/s |
| Data received             | 14,162.7 KiB  |
| Errors                    | 0             |
| CPU Avg                   | 40.3%         |
| CPU Max                   | 44.8%         |
| CPU Min                   | 36.3%         |
| Mem Avg                   | 77.7 MB       |
| Mem Max                   | 77.7 MB       |
| Mem Min                   | 77.7 MB       |
*CPU Usage is in single core, 100% would mean 1 whole core is being used up.*

**Monitoring in Real-Time**
While the test runs, monitor system usage in a separate terminal:
**Linux/Mac:**
```bash
btop
# or
htop -p $(pgrep -f uvicorn | paste -sd, -)
```

**Windows**
```bash
tasklist /FI "IMAGENAME eq python.exe" /V
```

The test is non-invasive and representative of production trade stream loads (Hopefully anyways)

## Roadmap

### Core Infrastructure
- [x] Base EventBus architecture (`asyncio.TaskGroup` fan-out)
- [x] Basic Binance USDM WebSocket & REST integration
- [x] Lazy subscription model (on-demand stream allocation)
- [ ] **Multi-Connection Auto-Scaling**
  - [ ] Implement connection pool manager per exchange
  - [ ] Track max stream limits dynamically per exchange connection
  - [ ] Auto-spawn new WebSocket clients when limits are breached

### Data & Caching Layer
- [ ] **TimescaleDB (PostgreSQL) Integration**
  - [ ] Schema design for hyper-efficient raw trade/klines storage
  - [ ] Real-time data persistence pipeline from EventBus
- [ ] **Redis Cache Layer**
  - [ ] Cache active tickers and order book snapshots for the frontend
  - [ ] Implement pub/sub or state cache to reduce DB load

### Analytics & Quant Engine
- [ ] **Statistical Analysis**
  - [ ] Basic asset correlation finders
- [ ] **Advanced Signal Processing & ML** (Ideas)
  - [ ] Spectral graph analysis for market structure
  - [ ] Hybrid LSTM + CNN architectures for time-series forecasting
  - [ ] Mixture Density Networks (MDNs) for predicting price distributions

