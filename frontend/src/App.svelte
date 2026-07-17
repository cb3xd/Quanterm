<script>
  import Topbar from "$lib/components/ui/custom/topbar/Topbar.svelte";
  import {
    websocketStore,
    connect,
    subscribe,
    streamsStore,
  } from "$lib/components/api/websocket.svelte";
  import Button from "$lib/components/ui/button/button.svelte";
  import Monitor from "$lib/components/ui/custom/monitor-panel/Monitor.svelte";
  connect();
</script>

<div class="min-h-screen">
  <Topbar />
  <Monitor />
  <Button
    variant="Ghost"
    onclick={() => subscribe(["trade_stream.btc-usdt"], "binanceusdm")}
    >Sub</Button
  >
</div>
