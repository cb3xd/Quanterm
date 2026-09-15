<script lang="ts">
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
    removeTicker,
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
  let currentTicker = $derived(tickersStore.currentTicker);
</script>

<div class="flex flex-row min-w-screen items-start border-b-1">
  {#each charts.entries() as [key, chart]}
    <Button
      class={currentTicker?.symbol === chart.symbol &&
      currentTicker?.exchange === chart.exchange
        ? "border-0 border-l border-b-2 gap-2"
        : "border-0 gap-2"}
      onclick={() =>
        setCurrentTicker(
          { symbol: chart.symbol, exchange: chart.exchange },
          false,
        )}
      variant="outline"
    >
      {chart.symbol.toUpperCase()}
      <button
        class="aspect-square p-1 hover:text-red-500 transition-colors"
        onclick={(e) => {
          e.stopPropagation();
          removeTicker({ symbol: chart.symbol, exchange: chart.exchange });
        }}
      >
        x
      </button>
    </Button>
  {/each}
  <Dialog.Root class="w-fit">
    <Dialog.Trigger
      ><Button
        onclick={() => {
          exchangeFilter = "";
          symbolStr = "";
          loadHist = false;
        }}
        variant="outline"
        class="border-t-0 border-b-0 aspect-square">+</Button
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
