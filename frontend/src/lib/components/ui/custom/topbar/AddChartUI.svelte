<script>
  import Button from "$lib/components/ui/button/button.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import AddChartPopup from "./AddChartPopup.svelte";
  import {
    fetchSymbols,
    symbolStore,
    exchangesStore,
    useKline,
  } from "$lib/components/api/apiDataStore.svelte";
  import {
    websocketStore,
    subscribe,
    streamsStore,
  } from "$lib/components/api/websocket.svelte";
  // On startup
  $effect(() => {
    fetchSymbols();
  });

  let exchanges = $derived(exchangesStore.current);
  let symbols = $derived(symbolStore.flattened);
  let exchangeFilter = $state("");
  let ticker = $state("");
  let loadHist = $state(false);
  let disableAdd = $derived(
    exchangeFilter == "" || ticker == "" ? true : false,
  );
</script>

<div class="flex flex-col min-w-screen items-start border-b-1">
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
              subscribe([`kline_stream.${ticker}.1m`], exchangeFilter);
              if (loadHist) useKline(exchangeFilter, ticker, "1m");
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
