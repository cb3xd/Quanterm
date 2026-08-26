<script>
  import Button from "$lib/components/ui/button/button.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
</script>

<Dialog.Root>
  <Dialog.Trigger>+</Dialog.Trigger>
  <div
    class="flex flex-row min-w-screen gap-2 justify-between items-center mb-1"
  >
    <Dialog.Content class="flex flex-row w-max gap-2">
      <Button>Test</Button>
      <Button>Test</Button>
      <Button>Test</Button>
    </Dialog.Content>
  </div></Dialog.Root
>
