<script>
  import Button from "$lib/components/ui/button/button.svelte";
  import * as Dialog from "$lib/components/ui/dialog/index.js";
  import AddChartPopup from "./AddChartPopup.svelte";
</script>

<div class="flex flex-col min-w-screen items-start border-b-1">
  <Dialog.Root class="w-fit">
    <Dialog.Trigger
      ><Button variant="outline" class="border-t-0 border-b-0">+</Button
      ></Dialog.Trigger
    >
    <Dialog.Content showCloseButton={false} class="flex flex-col gap-1.5">
      <AddChartPopup />
      <Dialog.Footer>
        <Dialog.Close asChild
          ><Button variant="outline">Add</Button>
          <Button variant="outline">Cancel</Button></Dialog.Close
        >
      </Dialog.Footer>
    </Dialog.Content>
  </Dialog.Root>
</div>
