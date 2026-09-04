<script>
  import { onMount } from "svelte";
  import Topbar from "$lib/components/ui/custom/topbar/Topbar.svelte";
  import {
    websocketStore,
    connect,
    subscribe,
    streamsStore,
  } from "$lib/components/api/websocket.svelte";
  import Button from "$lib/components/ui/button/button.svelte";
  import Monitor from "$lib/components/ui/custom/monitor-panel/Monitor.svelte";
  import AddChartUI from "$lib/components/ui/custom/topbar/AddChartUI.svelte";
  import Chart from "$lib/components/ui/custom/chart/Chart.svelte";
  import YAxisScrubber from "$lib/components/ui/custom/chart/YAxisScrubber.svelte";
  connect();
</script>

<div class="h-screen flex flex-col">
  <Topbar />
  <AddChartUI />
  <Chart />
</div>
