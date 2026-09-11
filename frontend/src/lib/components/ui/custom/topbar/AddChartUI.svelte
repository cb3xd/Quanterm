<script lang="ts">
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
    tickersStore,
    setCurrentTicker,
  } from "../chart/tickerDataStore.svelte.ts";

  // On startup
  $effect(() => {
    fetchSymbols();
  });
  let charts = $derived(tickersStore.tickers);
  let exchanges = $derived(exchangesStore.current);
  let symbols = $derived(symbolStore.flattened);
  let exchangeFilter = $state("");
  let symbolStr = $state("");
  let loadHist = $state(false);
  let disableAdd = $derived(
    exchangeFilter == "" || symbolStr == "" ? true : false,
  );
</script>

<div class="flex flex-row min-w-screen items-start border-b-1">
  {#each charts.entries() as [key, chart]}<Button
      class="border-0"
      onclick={() =>
        setCurrentTicker(
          { symbol: chart.symbol, exchange: chart.exchange },
          false,
        )}
      variant="outline">{chart.symbol.toUpperCase()}</Button
    >{/each}
  <Dialog.Root class="w-fit">
    <Dialog.Trigger
      ><Button
        onclick={() => {
          exchangeFilter = "";
          symbolStr = "";
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
        bind:loadHist
        bind:symbolStr
      />
      <Dialog.Footer>
        <Dialog.Close asChild>
          <Button
            onclick={() => {
              setCurrentTicker(
                { symbol: symbolStr, exchange: exchangeFilter },
                loadHist,
              );
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
