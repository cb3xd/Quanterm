<script>
  import { fetchApiData } from "$lib/components/dataStore.svelte";

  let { children } = $props();
  $effect(() => {
    fetchApiData();
  });
</script>

{@render children()}
