<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { Chart } from "./Chart.ts";
  import * as PIXI from "pixi.js";

  let app: PIXI.Application;
  let chart: Chart;
  let container: HTMLDivElement;
  onMount(async () => {
    app = new PIXI.Application();
    await app.init({
      background: "#000000",
      resizeTo: container,
      sharedTicker: true,
    });
    container.appendChild(app.canvas);

    chart = new Chart({
      container: container,
      events: app.renderer.events,
      ticker: app.ticker,
    });

    app.stage.addChild(chart);
    chart.drag().wheel();
    const sprite = chart.addChild(new PIXI.Sprite(PIXI.Texture.WHITE));
    sprite.tint = 0xff0000;
    sprite.width = sprite.height = 100;
    sprite.position.set(100, 100);
  });
</script>

<div
  bind:this={container}
  style="cursor: crosshair"
  class="relative w-full flex-1 min-h-0 overflow-hidden"
></div>
