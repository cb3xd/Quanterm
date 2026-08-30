<script>
  import {
    fetchKline,
    fetchSymbols,
    symbolStore,
    exchangesStore,
  } from "$lib/components/api/apiDataStore.svelte";
  import * as Popover from "$lib/components/ui/popover/index";
  import { Label } from "$lib/components/ui/label/index";
  import Button from "$lib/components/ui/button/button.svelte";
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  import * as Select from "$lib/components/ui/select/index";
  import Input from "$lib/components/ui/input/input.svelte";

  // On startup
  $effect(() => {
    fetchSymbols();
  });

  let exchanges = $derived(exchangesStore.current);
  let exchangeFilter = $state("");
  let exchangeContent = $derived(
    exchangeFilter === "" ? "Platform" : exchangeFilter, // This is whats displayed on the button dropdown thing
  );

  let symbolDisabled = $derived(exchangeFilter === "" ? true : false);
  let searchInput = $state("");
  let filteredSymbols = $derived(
    searchInput === ""
      ? []
      : symbolStore.flattened
          .filter(
            ({ symbol, exchange }) =>
              exchange === exchangeFilter &&
              symbol.toLowerCase().startsWith(searchInput.toLowerCase()),
          )
          .slice(0, 5),
  );
  let showPopover = $derived(searchInput !== "" ? true : false);
  let ticker = $state("");
  let loadHist = $state(false);
</script>

<div class="flex flex-row justify-between">
  <Label for="platform">Platform</Label>
  <Select.Root id="platform" type="single" bind:value={exchangeFilter}>
    <Select.Trigger class="w-[200px]">{exchangeContent}</Select.Trigger>
    <Select.Content class="bg-black">
      {#each exchanges as exchange}
        <Select.Item value={exchange} class="bg-black" label={exchange}
          >{exchange}</Select.Item
        >
      {/each}
    </Select.Content>
  </Select.Root>
</div>
<div class="flex flex-row justify-between">
  <Label for="tickerSearch">Ticker</Label>
  <div class="flex flex-col w-[200px]">
    <Input
      id="tickerSearch"
      placeholder="BTC-USDT"
      bind:value={searchInput}
      class="w-[200px]"
      disabled={symbolDisabled}
    />
    <Popover.Root bind:open={showPopover}>
      <Popover.Trigger></Popover.Trigger>
      <Popover.Content
        class="flex gap-0 p-0 w-[200px]"
        onOpenAutoFocus={(e) => e.preventDefault()}
        onCloseAutoFocus={(e) => e.preventDefault()}
      >
        {#if searchInput !== ""}
          {#if symbolStore.isLoading}{:else}
            {#each filteredSymbols as { symbol, exchange }}
              <Popover.Close asChild>
                <Button
                  variant="outline"
                  class="cursor-pointer w-full"
                  onclick={() => {
                    ticker = symbol;
                    searchInput = symbol.toUpperCase();
                  }}
                  ><span>{symbol.toUpperCase()}</span>
                </Button></Popover.Close
              >
            {/each}
          {/if}
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
      <Select.Group>
        <Select.Item value={false} label="None" class="bg-black" />
        <Select.Item
          value={true}
          label="Past Hour"
          class="bg-black"
        /></Select.Group
      ></Select.Content
    >
  </Select.Root>
</div>
