let symbols = $state({
  data: {},
  loading: true,
  error: ""
})

let klines = $state({
  data: [],
  loading: true,
  error: ""
})


export async function fetchApiData(stateVar, dataEndpoint, params) {
  try {
    stateVar.loading = true;

    const response = await fetch(`http://localhost:8000/api/${dataEndpoint}?${params}`);

    console.log(response);
    const result = await response.json();
    console.log(result);

    stateVar.data = result;
    stateVar.loading = false;
  }
  catch (err) {
    stateVar.error = "Failed to load symbols";
    stateVar.loading = false;
    console.error(err)
  }
}

export async function fetchSymbols() {
  fetchApiData(symbols, 'all_exchange_symbols');
}

export async function fetchKline(exchangeId, symbol, interval,) {
  const params = new URLSearchParams({ symbol: symbol, interval: interval })
  const endpoint = `kline/${exchangeId}`
  fetchApiData(klines, endpoint, params);
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
