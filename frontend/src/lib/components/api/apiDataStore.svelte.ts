let tickerPriceChange = $state({
  data: [],
  loading: true,
  error: ""
})

let symbols = $state({
  data: {},
  loading: true,
  error: ""
})

export async function fetchApiData(dataEndpoint: string, params: URLSearchParams | null) {
  const response = await fetch(`http://localhost:8000/api/${dataEndpoint}?${params}`);
  if (!response.ok) throw new Error(`HTTP Error! status: ${response.status}`);
  return await response.json();
}

export async function fetchSymbols() {
  symbols.loading = true;
  try {
    symbols.data = await fetchApiData("symbols", null)
    symbols.error = "";
  } catch (err: unknown) {
    symbols.error = "Failed to load symbols";
    console.error(err);
  } finally {
    symbols.loading = false;
  }
}

function klineCacheKeygen(exchangeId: string, symbol: string, interval: string) {
  return `${exchangeId}:${symbol}:${interval}`
}

const klineCache = new Map();

interface KlineEntry {
  data: Object,
  loading: boolean,
  error: string,
  promise: Promise<unknown> | null
}

async function fetchKline(exchangeId: string, symbol: string, interval: string,) {
  const key = klineCacheKeygen(exchangeId, symbol, interval);
  const entry: KlineEntry = { data: {}, loading: true, error: "", promise: null };
  klineCache.set(key, entry);
  const params = new URLSearchParams({ symbol: symbol, interval: interval })
  const endpoint = `kline/${exchangeId}`
  entry.promise = fetchApiData(endpoint, params)
    .then(result => { entry.data = result; entry.loading = false; })
    .catch(err => { entry.error = err; entry.loading = false; });
}

export function useKline(exchangeId: string, symbol: string, interval: string) {
  const key = klineCacheKeygen(exchangeId, symbol, interval);
  if (!klineCache.has(key)) fetchKline(exchangeId, symbol, interval);
  return klineCache.get(key);
}

export const symbolStore = {
  get current() { return symbols.data },
  get isLoading() { return symbols.loading },
  get error() { return symbols.error },
  get flattened() {
    const result = [];
    for (const [symbol, exchanges] of Object.entries(symbols.data)) {
      const list = Array.isArray(exchanges) ? exchanges : [exchanges];
      for (const exchange of list) {
        result.push({ symbol, exchange });
      }
    }
    return result;
  }
};

export const exchangesStore = {
  get current() { return [...new Set(symbolStore.flattened.map((item) => item.exchange)),] },
  get isLoading() { return symbols.loading },
  get error() { return symbols.error },

};


export const tickerPriceChangeStore = {
  get current() { return tickerPriceChange.data },
  get isLoading() { return tickerPriceChange.loading },
  get error() { return tickerPriceChange.error },
}
