import { useKline } from "$lib/components/api/apiDataStore.svelte.ts";
import { streamsStore, subscribe } from "$lib/components/api/websocket.svelte.ts";
import { SvelteMap } from "svelte/reactivity";


interface TickerEntry {
  ticker: string,
  exchange: string,
  readonly stream: any,
  histData: unknown | null;
}
const tickers: SvelteMap<string, TickerEntry> = new SvelteMap();
let currentKey: string = $state("");
function addTicker(ticker: string, exchange: string, loadHist: boolean) {
  const streamId = `kline_stream.${ticker}.1m`;
  subscribe([streamId], exchange);
  const entry: TickerEntry = {
    ticker: ticker,
    exchange: exchange,
    get stream() {
      return streamsStore.streams[`${exchange}.${streamId}`];
    },
    histData: loadHist ? useKline(exchange, ticker, "1m") : null
  };
  tickers.set(`${ticker}.${exchange}`, entry);
}

export function setCurrentTicker(ticker: string, exchange: string, loadHist: boolean) {
  const key = `${ticker}.${exchange}`;
  if (!tickers.has(key)) addTicker(ticker, exchange, loadHist);
  currentKey = key;
}

export const tickersStore = {
  get tickers() { return tickers },
  get currentKey() { return currentKey },
  get currentTicker() { return tickers.get(currentKey) },
};


