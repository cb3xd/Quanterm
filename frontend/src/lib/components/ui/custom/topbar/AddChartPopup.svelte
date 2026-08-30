<script>
  import {
    fetchKline,
    fetchSymbols,
    symbolStore,
  } from "$lib/components/api/apiDataStore.svelte";
  import * as Popover from "$lib/components/ui/popover/index";
  import { Label } from "$lib/components/ui/label/index";
  import Button from "$lib/components/ui/button/button.svelte";
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  import * as Select from "$lib/components/ui/select/index";
  import Input from "$lib/components/ui/input/input.svelte";
  $effect(() => {
    fetchSymbols();
  });
  let exchanges = $derived([
    ...new Set(symbolStore.flattened.map((item) => item.exchange)),
  ]);
  let exchangeFilter = $state("");
  let exchangeContent = $derived(
    exchangeFilter === "" ? "Platform" : exchangeFilter,
  );
  let symbolDisabled = $derived(exchangeFilter === "" ? true : false);
  let searchInput = $state("");
  let filteredSymbols = $derived(
    searchInput === ""
      ? []
      : symbolStore.flattened.filter(
          ({ symbol, exchange }) =>
            exchange === exchangeFilter &&
            symbol.toLowerCase().startsWith(searchInput.toLowerCase()),
        ),
  );
  let topFilteredSymbols = $derived(filteredSymbols.slice(0, 5));
  let showPopover = $derived(searchInput !== "" ? true : false);
  let ticker = $state("");
  let loadHist = $state(false);
</script>

<div class="flex flex-row justify-between">
  <Label for="platform">Platform</Label>
  <Select.Root id="platform" type="single" bind:value={exchangeFilter}>
    <Select.Trigger class="w-[200px]">{exchangeContent}</Select.Trigger>
    <Select.Content>
      {#each exchanges as exchange}
        <Select.Item value={exchange} label={exchange}>{exchange}</Select.Item>
      {/each}
    </Select.Content>
  </Select.Root>
</div>
<div class="flex flex-row justify-between">
  <Label for="tickerSearch">Ticker</Label>
  <div class="flex flex-col w-[200px]">
    <Input
      id="tickerSearch"
      placeholder="BTCUSDT"
      bind:value={searchInput}
      class="w-[200px]"
      disabled={symbolDisabled}
    />
    <Popover.Root bind:open={showPopover}>
      <Popover.Trigger></Popover.Trigger>
      <Popover.Content
        class="w-fit align-middle"
        onOpenAutoFocus={(e) => e.preventDefault()}
        onCloseAutoFocus={(e) => e.preventDefault()}
      >
        {#if searchInput == ""}
          <p></p>
        {:else}
          <p>Results for: {searchInput}</p>
          <ScrollArea class="w-[180px] h-fit border">
            {#if symbolStore.isLoading}{:else}
              {#each topFilteredSymbols as { symbol, exchange }}
                <Button
                  variant="outline"
                  class="flex  w-full justify-between cursor-pointer"
                  onclick={() => {
                    ticker = symbol;
                    searchInput = symbol;
                  }}
                  ><span>{symbol.toUpperCase()}</span>
                </Button>
              {/each}
            {/if}
          </ScrollArea>
        {/if}
      </Popover.Content>
    </Popover.Root>
  </div>
</div>
<div class="flex flex-row justify-between">
  <Label for="histdata">Add Historical Data</Label>
  <Select.Root id="histdata" type="single" bind:value={loadHist}>
    <Select.Trigger class="w-[200px]"
      >{loadHist ? "Past Hour" : "None"}</Select.Trigger
    >
    <Select.Content>
      <Select.Group
        ><Select.Item value={false} label="None" /><Select.Item
          value={true}
          label="Past Hour"
        /></Select.Group
      ></Select.Content
    >
  </Select.Root>
</div>
