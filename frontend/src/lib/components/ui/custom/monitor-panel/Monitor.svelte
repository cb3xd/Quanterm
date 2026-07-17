<script>
  import {
    websocketStore,
    exchangesStore,
  } from "$lib/components/api/websocket.svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area/index";
  import * as Item from "$lib/components/ui/item/index";
  let exchanges = $derived(exchangesStore.exchanges);
</script>

<ScrollArea class="h-fit w-32 border ">
  <div class="h-full w-full flex flex-col items-center align-middle py-1">
    {#each exchanges as exchange}
      <Item.Root variant="outline" class="w-full py-0 border-0">
        <Item.Media>
          <div class="h-1 w-1 rounded-full bg-green-600" />
        </Item.Media>
        <Item.Content>{exchange}</Item.Content>
      </Item.Root>
    {/each}

    <Item.Root variant="outline" class="w-full  py-0 border-0">
      <Item.Media>
        <div class="h-1 w-1 rounded-full bg-gray-600" />
      </Item.Media>
      <Item.Content>mexc</Item.Content>
    </Item.Root>
    <Item.Root variant="outline" class="w-full  py-0 border-0">
      <Item.Media>
        <div class="h-1 w-1 rounded-full bg-gray-600" />
      </Item.Media>
      <Item.Content>deribit</Item.Content>
    </Item.Root>
    <Item.Root variant="outline" class="w-full  py-0 border-0">
      <Item.Media>
        <div class="h-1 w-1 rounded-full bg-gray-600" />
      </Item.Media>
      <Item.Content>Bybit</Item.Content>
    </Item.Root>
  </div>
</ScrollArea>
