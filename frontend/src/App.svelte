<script>
  import Topbar from "$lib/components/ui/custom/topbar/Topbar.svelte";
  import { connect } from "$lib/components/api/websocket.svelte";
  import AddChartUI from "$lib/components/ui/custom/topbar/AddChartUI.svelte";
  connect();
</script>

<div class="min-h-screen">
  <Topbar />
  <AddChartUI />
</div>
