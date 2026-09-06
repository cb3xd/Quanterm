import { useKline } from "$lib/components/api/apiDataStore.svelte";
import { streamsStore, subscribe } from "$lib/components/api/websocket.svelte";
import { SvelteMap } from "svelte/reactivity";

const charts = new SvelteMap();
let currentKey = $state(null);
function addChart(ticker, exchange, loadHist) {
  const streamId = `kline_stream.${ticker}.1m`;
  subscribe([streamId], exchange);
  const entry = {
    ticker: ticker,
    exchange: exchange,
    get stream() {
      return streamsStore.streams[streamId];
    },
    histData: loadHist ? useKline(exchange, ticker, "1m") : null
  };
  console.log(entry);
  console.log(charts)
  charts.set(`${ticker}.${exchange}`, entry);
}

export function setCurrentChart(ticker, exchange, loadHist) {
  const key = `${ticker}.${exchange}`;
  if (!charts.has(key)) addChart(ticker, exchange, loadHist);
  currentKey = key;
}

export const chartsStore = {
  get charts() { return charts },
  get currentKey() { return currentKey },
  get currentChart() { return charts.get(currentKey) }
};
