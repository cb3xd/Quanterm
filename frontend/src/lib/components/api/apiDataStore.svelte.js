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

const MAX_KLINE_DATASETS = 20;
let klines = $state({
  data: {},
  loading: true,
  error: ""
})


export async function fetchApiData(dataEndpoint, params) {
  const response = await fetch(`http://localhost:8000/api/${dataEndpoint}?${params}`);
  if (!response.ok) throw new Error(`HTTP Error! status: ${response.status}`);
  return await response.json();
}

export async function fetchTickerPriceChange(symbol) {
  tickerPriceChange.loading = true;
  try {
    const params = new URLSearchParams({ symbol: symbol });
    const endpoint = `price-change/binanceusdm`;
    const result = await fetchApiData(endpoint, params);

    const index = tickerPriceChange.data.findIndex((item) => item.symbol === symbol);

    if (index !== -1) {
      tickerPriceChange.data[index] = { ...result, symbol };
    } else {
      tickerPriceChange.data.push({ ...result, symbol });
    }

    tickerPriceChange.error = "";
  } catch (err) {
    tickerPriceChange.error = err.message;
    console.error(err);
  } finally {
    tickerPriceChange.loading = false;
  }
}
export async function fetchSymbols() {
  symbols.loading = true;
  try {
    symbols.data = await fetchApiData("symbols")
    symbols.error = "";
  } catch (err) {
    symbols.error = "Failed to load symbols";
    console.error(err);
  } finally {
    symbols.loading = false;
  }
}

export async function fetchKline(exchangeId, symbol, interval,) {
  const key = `${exchangeId}:${symbol}:${interval}`
  klines.loading = true;
  try {
    const params = new URLSearchParams({ symbol: symbol, interval: interval })
    const endpoint = `kline/${exchangeId}`
    const result = await fetchApiData(endpoint, params);
    const keys = Object.keys(klines.data);
    if (keys.length >= MAX_KLINE_DATASETS && !klines.data[key]) {
      delete klines.data[keys[0]];
    }
    klines.data[key] = result;

    klines.error = "";
  } catch (err) {
    klines.error = `Failed to load klines for ${symbol}`;
  } finally {
    klines.loading = false;
  }
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

export const klineStore = {
  get current() { return klines.data },
  get isLoading() { return klines.loading },
  get error() { return klines.error },

}

export const tickerPriceChangeStore = {
  get current() { return tickerPriceChange.data },
  get isLoading() { return tickerPriceChange.loading },
  get error() { return tickerPriceChange.error },
}
