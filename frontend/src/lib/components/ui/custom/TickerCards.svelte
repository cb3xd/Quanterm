<script>
  import {
    fetchTickerPriceChange,
    tickerPriceChangeStore,
  } from "$lib/components/dataStore.svelte";
  import * as Card from "$lib/components/ui/card/index";
  import { Label } from "../label";
  import Skeleton from "../skeleton/skeleton.svelte";
  $effect(() => {
    fetchTickerPriceChange("btcusdt");
    fetchTickerPriceChange("solusdt");
    fetchTickerPriceChange("ethusdt");
  });
</script>

<div class="flex flex-wrap justify-center gap-22 py-4 h-fit">
  {#if tickerPriceChangeStore.isLoading}
    <Skeleton class="w-1/5 min-h-30" />
    <Skeleton class="w-1/5 min-h-30" />
    <Skeleton class="w-1/5 min-h-30" />
  {:else}
    {#each tickerPriceChangeStore.current as ticker}
      <Card.Root class="w-1/5  h-fit max-w-sm cursor-pointer">
        <Card.Header>
          <Card.Title>{ticker["symbol"].toUpperCase()}</Card.Title>
          <Card.Description>PERPETUAL</Card.Description>
          <Card.Action
            class={ticker["priceChangePercent"].startsWith("-")
              ? "text-destructive"
              : "text-emerald-400"}
          >
            {ticker["priceChangePercent"]}%
          </Card.Action>
        </Card.Header>
        <Card.Content>
          <div class="flex flex-col gap-2">
            <div class="flex flex-row justify-between gap-2w">
              <Label class="text-lg">{ticker["lastPrice"]}</Label>
            </div>
          </div>
        </Card.Content>
      </Card.Root>
    {/each}
  {/if}
</div>
