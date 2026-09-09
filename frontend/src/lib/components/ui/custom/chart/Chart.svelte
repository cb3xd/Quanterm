<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { Chart } from "./Chart.ts";
  import * as PIXI from "pixi.js";
  import { chartsStore } from "./chartsDataStore.svelte.js";

  let app: PIXI.Application;
  let chart: Chart;
  let container: HTMLDivElement;
  let text: PIXI.Text;
  let coordinateText: PIXI.Text;
  let xLine: PIXI.Graphics;
  let yLine: PIXI.Graphics;
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
        fill: "#202020",
      },
    });

    coordinateText = new PIXI.Text({
      text: "0, 0",
      style: {
        fontFamily: "Arial",
        fontSize: 12,
        fill: "#606060",
      },
    });

    xLine = new PIXI.Graphics()
      .moveTo(0, -app.canvas.clientHeight)
      .lineTo(0, app.canvas.clientHeight)
      .stroke({ color: "#202020", pixelLine: true });

    yLine = new PIXI.Graphics()
      .moveTo(-app.canvas.clientWidth, 0)
      .lineTo(app.canvas.clientWidth, 0)
      .stroke({ color: "#202020", pixelLine: true });
    text.anchor.set(0.5);
    text.position.set(container.clientWidth / 2, container.clientHeight / 2);
    coordinateText.position.set(10, 10);
    app.stage.addChild(text);
    app.stage.addChild(coordinateText);
    app.ticker.add(() => {
      const screenPoint = chart.input.lastGlobalPointer;
      const graphPoint = chart.toGraph(screenPoint);
      coordinateText.text = `(${Math.round(graphPoint.x)},${Math.round(graphPoint.y * -1)})`;
      xLine.position.set(
        chart.toGlobal(new PIXI.Point(Math.round(graphPoint.x), graphPoint.y))
          .x,
        screenPoint.y,
      );
      yLine.position.set(0, screenPoint.y);
      if (!chartsStore.currentChart) return;
      if (!chartsStore.currentChart.stream) return;
      text.text =
        chartsStore.currentChart !== undefined
          ? chartsStore.currentChart.stream.close_price
          : "Press '+' to add a chart";
    });

    const graphics = new PIXI.Graphics()
      .rect(50, 50, 100, 100)
      .fill(0xff0000)
      .circle(200, 200, 50)
      .stroke(0x00ff00)
      .lineStyle(5)
      .moveTo(300, 300)
      .lineTo(400, 400);
    app.stage.addChild(chart);
    app.stage.addChild(xLine, yLine);
    chart.addChild(graphics);
    chart.drag().wheel();
  });
</script>

<div
  bind:this={container}
  style="cursor: crosshair"
  class="relative w-full flex-1 min-h-0 overflow-hidden"
></div>
