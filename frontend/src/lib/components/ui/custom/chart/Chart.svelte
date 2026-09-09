<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { Chart } from "./Chart.ts";
  import * as PIXI from "pixi.js";
  import { chartsStore } from "./chartsDataStore.svelte.js";

  let app: PIXI.Application;
  let chart: Chart;
  let container: HTMLDivElement;
  let text: PIXI.Text;
  let currentPriceLine = new PIXI.Graphics().stroke({
    color: 0xff0000,
    pixelLine: true,
  });

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

    text = new PIXI.Text({
      text: "Press '+' to add a chart",
      style: {
        fontFamily: "Arial",
        fontSize: 48,
        fill: "#FFFFFF",
      },
    });
    text.anchor.set(0.5);
    text.position.set(container.clientWidth / 2, container.clientHeight / 2);

    app.stage.addChild(text);
    app.ticker.add(() => {
      const graphPoint = chart.toGraph(chart.input.lastGlobalPointer);
      console.log(graphPoint.x, graphPoint.y * -1);
      if (!chartsStore.currentChart) return;
      if (!chartsStore.currentChart.stream) return;
      text.text =
        chartsStore.currentChart !== undefined
          ? chartsStore.currentChart.stream.close_price
          : "Press '+' to add a chart";
    });
    const sprite = chart.addChild(new PIXI.Sprite(PIXI.Texture.WHITE));
    sprite.tint = 0xff0000;
    sprite.width = sprite.height = 10;
    sprite.position.set(0, 0);

    const sprite2 = chart.addChild(new PIXI.Sprite(PIXI.Texture.WHITE));
    sprite2.tint = 0xff0000;
    sprite2.width = sprite2.height = 10;
    sprite2.position.set(200, 0);

    app.stage.addChild(chart);
    // chart.addChild(currentPriceLine);

    chart.drag().wheel();
  });
</script>

<div
  bind:this={container}
  style="cursor: crosshair"
  class="relative w-full flex-1 min-h-0 overflow-hidden"
></div>
