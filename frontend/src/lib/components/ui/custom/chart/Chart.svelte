<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import * as PIXI from "pixi.js";
  import { Text } from "pixi.js";
  import { chartsStore } from "./chartsDataStore.svelte";
  let container: HTMLDivElement;
  let app: PIXI.Application;

  let yAxisBar: PIXI.Graphics;
  let txt: PIXI.Text;
  onMount(async () => {
    app = new PIXI.Application();
    await app.init({
      background: "#000000",
      resizeTo: container,
    });
    container.appendChild(app.canvas);
    yAxisBar = new PIXI.Graphics()
      .rect(0, 0, container.clientWidth / 24, container.clientHeight)
      .fill("#101010");
    yAxisBar.position.set(
      container.clientWidth - container.clientWidth / 24,
      0,
    );
    yAxisBar.eventMode = "static";
    yAxisBar.cursor = "ns-resize";
    console.log(container.clientWidth - container.clientWidth / 24);

    txt = new Text({
      text: "Press '+' to add a chart",
      style: {
        fontFamily: "Arial",
        fontSize: 48,
        fill: "#101010",
      },
    });

    app.ticker.add(updateText);
    function updateText() {
      txt.text =
        chartsStore.currentChart !== undefined
          ? chartsStore.currentChart.ticker.toUpperCase()
          : "Press '+' to add a chart";
    }
    txt.anchor.set(0.5);
    txt.position.set(container.clientWidth / 2, container.clientHeight / 2);
    app.stage.addChild(txt);

    app.stage.addChild(yAxisBar);
  });
  window.addEventListener("resize", handleResize);
  function handleResize() {
    console.log(container.clientHeight, container.clientWidth);
    const newPos = container.clientWidth - container.clientWidth / 24;
    console.log(newPos);
    yAxisBar.position.set(newPos, 0);
    yAxisBar.setSize(yAxisBar.width, container.clientHeight);
  }

  onDestroy(() => {
    app?.destroy(true, { children: true });
  });
</script>

<div
  bind:this={container}
  style="cursor: crosshair;"
  class="relative w-full flex-1 min-h-0 overflow-hidden"
></div>
