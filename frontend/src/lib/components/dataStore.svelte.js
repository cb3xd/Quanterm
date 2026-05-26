let apiData = $state({
  data: {},
  loading: true,
  error: ""
})


export async function fetchApiData() {
  try {
    apiData.loading = true;

    const response = await fetch('http://localhost:8000/api/all_exchange_symbols');
    console.log(response);
    const result = await response.json();
    console.log(result);

    apiData.data = result;
    apiData.loading = false;
  }
  catch (err) {
    apiData.error = "Failed to load symbols";
    apiData.loading = false;
    console.error(err)
  }
}


export const symbolStore = {
  get current() { return apiData.data },
  get isLoading() { return apiData.loading },
  get error() { return apiData.error }
};
