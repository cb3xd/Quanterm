import { useKline } from "$lib/components/api/apiDataStore.svelte.ts";
import { streamsStore, subscribe } from "$lib/components/api/websocket.svelte.ts";
import { SvelteMap } from "svelte/reactivity";

export interface ITicker {
  symbol: string,
  exchange: string,
}

interface ITickerEntry {
  symbol: string,
  exchange: string,
  readonly stream: any,
  histData: unknown | null;
}

const tickers: SvelteMap<string, ITickerEntry> = new SvelteMap();
let currentKey: string = $state("");

function addTicker(ticker: ITicker, loadHist: boolean) {
  const streamId = `kline_stream.${ticker.symbol}.1m`;
  subscribe([streamId], ticker.exchange);
  const entry: ITickerEntry = {
    symbol: ticker.symbol,
    exchange: ticker.exchange,
    get stream() {
      return streamsStore.streams[`${ticker.exchange}.${streamId}`];
    },
    histData: loadHist ? useKline(ticker.exchange, ticker.symbol, "1m") : null
  };
  tickers.set(`${ticker.symbol}.${ticker.exchange}`, entry);
}

export function setCurrentTicker(ticker: ITicker, loadHist: boolean) {
  const key = `${ticker.symbol}.${ticker.exchange}`;
  if (!tickers.has(key)) addTicker(ticker, loadHist);
  currentKey = key;
}

export const tickersStore = {
  get tickers() { return tickers },
  get currentKey() { return currentKey },
  get currentTicker() { return tickers.get(currentKey) },
};


