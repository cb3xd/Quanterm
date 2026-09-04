<script>
  let curr = 50; // Initialize above 0 to prevent initial division by zero
  let startY = 0;
  let startValue = 50;

  function handleMouseDown(e) {
    startY = e.clientY;
    startValue = curr;
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  }

  function onMouseMove(e) {
    const delta = startY - e.clientY;
    // Clamp curr so it stays above 0 while dragging
    curr = Math.max(1, startValue + delta * 0.5);
  }

  function onMouseUp() {
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
  }

  $: step = Math.max(0.01, curr / 100);
  $: testInterval = Array.from(
    { length: Math.floor(100 / step) + 1 },
    (_, i) => (i * step).toFixed(1), // Formatted to 1 decimal place
  ).reverse();
</script>

<div
  id="yaxis-scrubber"
  class="flex flex-col min-h-full w-12"
  style:gap="{curr}px"
  style:cursor="row-resize"
  on:mousedown={handleMouseDown}
  role="slider"
  aria-label="Y-axis value"
  aria-valuenow={curr / 100}
  aria-valuemin={1}
  aria-valuemax={200}
  tabindex="0"
></div>
