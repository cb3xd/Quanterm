<script>
  import * as Popover from "$lib/components/ui/popover/index";
  import { Label } from "$lib/components/ui/label/index";
  import Button from "$lib/components/ui/button/button.svelte";
  import * as Select from "$lib/components/ui/select/index";
  import Input from "$lib/components/ui/input/input.svelte";
  let {
    exchanges = $bindable(),
    exchangeFilter = $bindable(),
    symbols = $bindable(),
    ticker = $bindable(),
    loadHist = $bindable(),
  } = $props();
  let exchangeContent = $derived(
    exchangeFilter === "" ? "Platform" : exchangeFilter, // This is whats displayed on the button dropdown thing
  );

  let symbolDisabled = $derived(exchangeFilter === "" ? true : false);
  let searchInput = $state("");
  let filteredSymbols = $derived(
    searchInput === ""
      ? []
      : symbols
          .filter(
            ({ symbol, exchange }) =>
              exchange === exchangeFilter &&
              symbol.toLowerCase().startsWith(searchInput.toLowerCase()),
          )
          .slice(0, 5),
  );
  let showPopover = $derived(searchInput !== "" ? true : false);
</script>

<div class="flex justify-between">
  <Label for="platform">Platform</Label>
  <Select.Root id="platform" type="single" bind:value={exchangeFilter}>
    <Select.Trigger class="w-[200px]">{exchangeContent}</Select.Trigger>
    <Select.Content>
      {#each exchanges as exchange}
        <Select.Item value={exchange} class="bg-black" label={exchange}>
          {#snippet child({ props })}
            <Button
              {...props}
              variant="ghost"
              class="bg-black w-full justify-start">{exchange}</Button
            >
          {/snippet}
        </Select.Item>
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
      </Popover.Content>
    </Popover.Root>
  </div>
</div>
<div class="flex justify-between">
  <Label for="histdata">Add Historical Data</Label>
  <Select.Root id="histdata" type="single" bind:value={loadHist}>
    <Select.Trigger class="w-[200px]">{loadHist ? "Yes" : "No"}</Select.Trigger>
    <Select.Content>
      <Select.Group>
        <Select.Item value={false} label="No" class="bg-black">
          {#snippet child({ props })}
            <Button
              {...props}
              variant="ghost"
              class="bg-black w-full justify-start">No</Button
            >
          {/snippet}
        </Select.Item>
        <Select.Item value={true} label="Yes" class="bg-black">
          {#snippet child({ props })}
            <Button
              {...props}
              variant="ghost"
              class="bg-black w-full justify-start">Yes</Button
            >
          {/snippet}
        </Select.Item>
      </Select.Group>
    </Select.Content>
  </Select.Root>
</div>
