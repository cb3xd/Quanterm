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
Runs at `localhost:5171` (Vite default)

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
