# Quanterm Frontend Todo

## Homepage — Market Overview Dashboard

**Layout description (for illustration):**
A single-page dashboard with a top navigation bar containing the app name "QUANTERM" and nav links: Chart, Screeners, Backtest, Portfolio. Below the nav, a horizontal row of 4 ticker cards (BTCUSDT, ETHUSDT, SOLUSDT, +More) showing symbol name, 24h percentage change (green/red), and current price. Below that, a two-column section: left column lists Top Gainers and Top Losers with symbol name and percentage; right column shows a market heatmap grid (4x4 blocks of squares, each labeled with a ticker symbol, colored green/red by performance). At the bottom, a "Recent Activity" row with three mini sparkline charts for watched symbols.

**Data needed from backend:**
- `GET /api/all_exchange_symbols` (already exists) — list of all pairs
- New endpoint idea: `GET /api/ticker/24h` — aggregate 24h price change per symbol (or compute from kline data)

**Components to build:**
- `Home.svelte` — main dashboard shell + layout grid
- `TickerCard.svelte` — symbol name, price, 24h %, optional sparkline
- `MarketHeatmap.svelte` — NxN grid of colored squares (card/row per symbol)
- `TopMovers.svelte` — sorted list of gainers/losers with color-coded %
- `MiniChart.svelte` — small inline sparkline (canvas or SVG)

---

## Chart Page — Classic Terminal Layout

**Layout description (for illustration):**
A three-panel trading terminal layout. Top toolbar row with a symbol search/dropdown on the left, interval selector buttons (1m, 5m, 15m, 1h, 4h, 1d) in the center, and indicator/settings buttons on the right. Below the toolbar, the main area splits into two columns: left column (~25% width) is a scrollable symbol list with filter/search input at top (this is the existing Dialog component refactored into a sidebar panel); right column (~75% width) is split vertically: top ~70% is the main candlestick chart area, bottom ~30% is a volume histogram panel. A thin divider separates the two right panels. Collapsible left sidebar toggle.

**Components to build:**
- `ChartPage.svelte` — full page shell, toolbar + 2-column split
- `SymbolSidebar.svelte` — refactor existing Dialog content into a persistent sidebar panel with search + scrollable list
- `ChartToolbar.svelte` — symbol dropdown, interval selector, indicator buttons
- `KlineChart.svelte` — candlestick chart canvas (needs a charting library — consider lightweight-charts by TradingView or uPlot)
- `VolumePanel.svelte` — volume bar chart below main chart

---

## Shared / Infrastructure

- [ ] Decide routing approach (no SvelteKit — use conditional rendering or a simple hash router like `svelte-spa-router`)
- [ ] Evaluate charting library: `lightweight-charts` (TradingView, free) vs `uPlot` (lighter) vs custom canvas
- [ ] Build WebSocket connection layer for live trade/kline stream (mirrors the existing backend WS)
- [ ] Add skeleton/loading states for all async components (already have shadcn Skeleton)
- [ ] Dark mode is already set up — verify all new components use CSS variables from `app.css`

---

## Notes

- Stack: Svelte 5 + Vite + Tailwind + shadcn-svelte
- Backend at `localhost:8000`, frontend at `localhost:5173`
- Existing code: `src/App.svelte` (symbol dialog), `src/lib/components/dataStore.svelte.js` (symbol + kline fetch)
- Replace the default starter template structure in `app.css` (remove `#next-steps`, `#center`, `#spacer` rules)
