<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { Chart } from "./Chart.ts";
  import * as PIXI from "pixi.js";
  import { chartsStore } from "./chartsDataStore.svelte.js";
  let app: PIXI.Application;
  let chart: Chart;
  let container: HTMLDivElement;
  let text: PIXI.Text;

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

    text = new PIXI.Text({
      text: "Press '+' to add a chart",
      style: {
        fontFamily: "Arial",
        fontSize: 48,
        fill: "#101010",
      },
    });

    text.anchor.set(0.5);
    text.position.set(container.clientWidth / 2, container.clientHeight / 2);
    app.ticker.add(() => {
      text.text =
        chartsStore.currentChart !== undefined
          ? chartsStore.currentChart.ticker.toUpperCase()
          : "Press '+' to add a chart";
    });
    app.stage.addChild(text);
  });
</script>

<div
  bind:this={container}
  style="cursor: crosshair"
  class="relative w-full flex-1 min-h-0 overflow-hidden"
></div>
