<script>
  import { onMount, onDestroy } from "svelte";
  import * as PIXI from "pixi.js";
  import { Text } from "pixi.js";

  // Scale math
  // PixiJS
  let container;
  let app;

  onMount(async () => {
    app = new PIXI.Application();

    await app.init({
      background: "#000000",
      resizeTo: document.getElementById("chart-container"),
    });

    container.appendChild(app.canvas);
    const yAxisBar = new PIXI.Graphics()
      .rect(
        app.screen.width -
          document.getElementById("chart-container")?.clientWidth / 24,
        0,
        document.getElementById("chart-container")?.clientWidth / 24,
        document.getElementById("chart-container")?.clientHeight,
      )
      .fill("#101010");
    yAxisBar.eventMode = "static";
    yAxisBar.cursor = "ns-resize";

    const temp = new Text({
      text: "Empty Chart",
      style: {
        fontFamily: "Arial",
        fontSize: 48,
        fill: "#101010",
        align: "center",
      },
    });
    app.stage.addChild(temp);

    app.stage.addChild(yAxisBar);
  });

  onDestroy(() => {
    app?.destroy(true, { children: true });
  });
</script>

<div
  bind:this={container}
  style="cursor: crosshair;"
  class="flex flex-1 flex-col"
  id="chart-container"
></div>
