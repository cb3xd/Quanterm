<script>
  import Separator from "../../separator/separator.svelte";
  import { Button } from "$lib/components/ui/button/index.js";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index";
</script>

<div>
  <div
    class="flex flex-row min-w-screen gap-2 justify-between items-center mb-1"
  >
    <div class="flex flex-row w-max gap-2">
      <Button variant="outline">File</Button>
      <Button variant="outline">Connection</Button>
      <Button variant="outline">Settings</Button>
    </div>
  </div>
</div>
