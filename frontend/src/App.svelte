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
  import Tabs from "$lib/components/ui/custom/tabs/tabs.svelte";
  connect();
</script>

<div class="min-h-screen">
  <Topbar />
  <Tabs></Tabs>
  <Monitor />
  <Button
    variant="Ghost"
    onclick={() => subscribe(["trade_stream.btc-usdt"], "binanceusdm")}
    >Sub</Button
  >
</div>
