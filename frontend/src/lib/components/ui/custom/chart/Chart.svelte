<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { Chart } from "./Chart.ts";
  import * as PIXI from "pixi.js";
  import { chartsStore, setCurrentChart } from "./chartsDataStore.svelte.js";

  let app: PIXI.Application;
  let chart: Chart;
  let container: HTMLDivElement;
  let text: PIXI.Text;
  let coordinateText: PIXI.Text;
  let currentPriceLine: PIXI.Graphics;
  let xLine: PIXI.Graphics;
  let yLine: PIXI.Graphics;
  let priceLabel: PIXI.Text;
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

    currentPriceLine = new PIXI.Graphics()
      .moveTo(-app.canvas.clientWidth * 2, 0)
      .lineTo(app.canvas.clientWidth * 2, 0);

    priceLabel = new PIXI.Text({
      style: {
        fontFamily: "Arial",
        fontSize: 12,
        fill: "#404040",
      },
    });

    xLine = new PIXI.Graphics()
      .moveTo(0, -app.canvas.clientHeight * 2)
      .lineTo(0, app.canvas.clientHeight * 2)
      .stroke({ color: "#202020", pixelLine: true });

    yLine = new PIXI.Graphics()
      .moveTo(-app.canvas.clientWidth * 2, 0)
      .lineTo(app.canvas.clientWidth * 2, 0)
      .stroke({ color: "#202020", pixelLine: true });

    text.anchor.set(0.5);
    text.position.set(container.clientWidth / 2, container.clientHeight / 2);
    coordinateText.position.set(10, 10);
    priceLabel.position.set(
      chart.right - priceLabel.width,
      container.clientTop,
    );

    app.stage.addChild(text);
    app.stage.addChild(coordinateText);
    app.stage.addChild(priceLabel);
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
          ? chartsStore.currentChart.ticker.toUpperCase()
          : "Press '+' to add a chart";
      const currPrice = chartsStore.currentChart.stream.close_price;
      currentPriceLine.stroke({
        color: "#303030",
        pixelLine: true,
      });
      currentPriceLine.position.y = chart.toGlobal(
        new PIXI.Point(0, -1 * currPrice),
      ).y;
      priceLabel.position.y = chart.toGlobal(
        new PIXI.Point(0, -1 * currPrice),
      ).y;
      priceLabel.text = `${currPrice}`;
      priceLabel.position.x = container.clientWidth - priceLabel.width;
    });

    app.stage.addChild(chart);
    app.stage.addChild(xLine, yLine, currentPriceLine);
    chart.drag().wheel();
  });

  onDestroy(() => {
    app.destroy();
  });
</script>

<div
  bind:this={container}
  style="cursor: crosshair"
  class="relative w-full flex-1 min-h-0 overflow-hidden"
></div>
