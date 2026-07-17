<script>
  import {
    fetchKline,
    fetchSymbols,
    symbolStore,
  } from "$lib/components/api/apiDataStore.svelte";
  import { buttonVariants } from "$lib/components/ui/button/button.svelte";
  import Button from "$lib/components/ui/button/button.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  import Skeleton from "$lib/components/ui/skeleton/skeleton.svelte";
  import Input from "$lib/components/ui/input/input.svelte";
  $effect(() => {
    fetchSymbols();
  });
  let searchInput = $state("");
  let filteredSymbols = $derived(
    searchInput === ""
      ? []
      : symbolStore.flattened.filter(({ symbol }) =>
          symbol.toLowerCase().startsWith(searchInput.toLowerCase()),
        ),
  );
  let topFilteredSymbols = $derived(filteredSymbols.slice(0, 5));
</script>

<Dialog.Root>
  <Dialog.Trigger
    class={`${buttonVariants({ variant: "outline" })} w-full items-center justify-start cursor-pointer`}
  >
    CEX Symbols
  </Dialog.Trigger>
  <Dialog.Content class="sm:max-w-md">
    <Dialog.Header>
      <Dialog.Title>CEX Symbol Search</Dialog.Title>
    </Dialog.Header>
    <Input type="symbolSearch" placeholder="BTCUSDT" bind:value={searchInput}
    ></Input>
    {#if searchInput == ""}
      <p></p>
    {:else}
      <p>Results for: {searchInput}</p>
      <ScrollArea class="h-fit border">
        {#if symbolStore.isLoading}
          <Skeleton class="h-72" />
        {:else}
          {#each topFilteredSymbols as { symbol, exchange }}
            <Button
              variant="outline"
              class="flex w-full justify-between cursor-pointer"
              onclick={() => fetchKline(exchange, symbol, "1m")}
              ><span>{symbol.toUpperCase()}</span>
              <span class="text-xs text-muted-foreground">{exchange}</span
              ></Button
            >
          {/each}
        {/if}
      </ScrollArea>
    {/if}
  </Dialog.Content>
</Dialog.Root>
