<script lang="ts">
  import { fetchApiData, symbolStore } from "$lib/components/dataStore.svelte";
  import { buttonVariants } from "$lib/components/ui/button/button.svelte";
  import Button from "$lib/components/ui/button/button.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  import Skeleton from "$lib/components/ui/skeleton/skeleton.svelte";
  import Input from "$lib/components/ui/input/input.svelte";
  $effect(() => {
    fetchApiData();
  });

  let searchInput = $state("");
  let filteredSymbols = $derived(
    Object.fromEntries(
      Object.entries(symbolStore.current).filter(([key, value]) =>
        key.startsWith(searchInput.toLowerCase()),
      ),
    ),
  );
</script>

<Dialog.Root>
  <Dialog.Trigger class={buttonVariants({ variant: "outline" })}
    >Symbols</Dialog.Trigger
  >
  <Dialog.Content class="sm:max-w-md">
    <Dialog.Header>
      <Dialog.Title>Available Symbols</Dialog.Title>
      <Dialog.Description>
        Currently the only supported exchange is Binance USDM futures.
      </Dialog.Description>
    </Dialog.Header>
    <Input type="symbolSearch" placeholder="BTCUSDT" bind:value={searchInput}
    ></Input>
    {#if searchInput == ""}
      <p></p>
    {:else}
      <p>Results for: {searchInput}</p>
    {/if}
    <ScrollArea class="h-72 border">
      {#if symbolStore.isLoading}
        <Skeleton class="h-[125px]" />
      {:else}
        {#each Object.entries(filteredSymbols) as symbol}
          <Button variant="outline" class="flex w-full justify-between"
            ><span>{symbol[0].toUpperCase()}</span>
            <span> {symbol[1]}</span></Button
          >
        {/each}
      {/if}
    </ScrollArea>
  </Dialog.Content>
</Dialog.Root>
