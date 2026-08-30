<script>
  import * as NavigationMenu from "$lib/components/ui/navigation-menu/index.js";
</script>

<NavigationMenu.Root class="flex flex-col border-b-1 min-w-screen items-start">
  <NavigationMenu.List>
    <NavigationMenu.Item>
      <NavigationMenu.Trigger>File</NavigationMenu.Trigger>
      <NavigationMenu.Content>
        <NavigationMenu.Link>wip</NavigationMenu.Link>
      </NavigationMenu.Content>
    </NavigationMenu.Item>
    <NavigationMenu.Item>
      <NavigationMenu.Trigger>Connection</NavigationMenu.Trigger>
    </NavigationMenu.Item>
    <NavigationMenu.Item>
      <NavigationMenu.Trigger>Settings</NavigationMenu.Trigger>
    </NavigationMenu.Item>
  </NavigationMenu.List>
</NavigationMenu.Root>
