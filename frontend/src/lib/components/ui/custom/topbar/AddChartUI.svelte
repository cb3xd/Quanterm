<script>
  import { setContext } from "svelte";
  import Button from "$lib/components/ui/button/button.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import AddChartPopup from "./AddChartPopup.svelte";
  import {
    fetchSymbols,
    symbolStore,
    exchangesStore,
  } from "$lib/components/api/apiDataStore.svelte";
  import {
    chartsStore,
    setCurrentChart,
  } from "../chart/chartsDataStore.svelte";

  // On startup
  $effect(() => {
    fetchSymbols();
  });
  let charts = $derived(chartsStore.charts);
  let exchanges = $derived(exchangesStore.current);
  let symbols = $derived(symbolStore.flattened);
  let exchangeFilter = $state("");
  let ticker = $state("");
  let loadHist = $state(false);
  let disableAdd = $derived(
    exchangeFilter == "" || ticker == "" ? true : false,
  );
</script>

<div class="flex flex-row min-w-screen items-start border-b-1">
  {#each charts.entries() as [key, chart]}<Button
      class="border-0"
      onclick={() => setCurrentChart(chart.ticker, chart.exchange)}
      variant="outline">{chart.ticker.toUpperCase()}</Button
    >{/each}
  <Dialog.Root class="w-fit">
    <Dialog.Trigger
      ><Button
        onclick={() => {
          exchangeFilter = "";
          ticker = "";
          loadHist = false;
        }}
        variant="outline"
        class="border-t-0 border-b-0">+</Button
      ></Dialog.Trigger
    >
    <Dialog.Content showCloseButton={false} class="flex flex-col gap-1.5">
      <AddChartPopup
        bind:exchanges
        bind:exchangeFilter
        bind:symbols
        bind:ticker
        bind:loadHist
      />
      <Dialog.Footer>
        <Dialog.Close asChild>
          <Button
            onclick={() => {
              setCurrentChart(ticker, exchangeFilter, loadHist);
            }}
            variant="outline"
            disabled={disableAdd}>Add</Button
          >
          <Button variant="outline">Cancel</Button>
        </Dialog.Close>
      </Dialog.Footer>
    </Dialog.Content>
  </Dialog.Root>
</div>
