<script module>
  import { tv } from "tailwind-variants";
  import { cn } from "$lib/utils.js";

  export const navigationMenuTriggerStyle = tv({
    base: "rounded-none px-2.5 py-1.5 text-xs font-medium transition-all hover:bg-muted focus:bg-muted focus-visible:ring-1 focus-visible:ring-ring/50 focus-visible:outline-1 disabled:opacity-50 data-popup-open:bg-muted/50 data-popup-open:hover:bg-muted data-open:bg-muted/50 data-open:hover:bg-muted data-open:focus:bg-muted group/navigation-menu-trigger inline-flex h-9 w-max items-center justify-center outline-none disabled:pointer-events-none",
  });
</script>

<script>
  import { NavigationMenu as NavigationMenuPrimitive } from "bits-ui";
  let {
    ref = $bindable(null),
    class: className,
    children,
    ...restProps
  } = $props();
</script>

<NavigationMenuPrimitive.Trigger
  bind:ref
  data-slot="navigation-menu-trigger"
  class={cn(navigationMenuTriggerStyle(), "group", className)}
  {...restProps}
>
  {@render children?.()}
</NavigationMenuPrimitive.Trigger>

