<script>
  import Topbar from "$lib/components/ui/custom/topbar/Topbar.svelte";
  import {
    websocketStore,
    connect,
    subscribe,
  } from "$lib/components/api/websocket.svelte";
  import Button from "$lib/components/ui/button/button.svelte";
  connect();
</script>

<div class="min-h-screen">
  <Topbar />
  <h1>{websocketStore.isConnected}</h1>
  <Button
    variant="default"
    onclick={() => subscribe(["trade_stream.btcusdt"], "binanceusdm")}
    >SUB</Button
  >
</div>
