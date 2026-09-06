import { FederatedPointerEvent, Point, PointData, Rectangle } from "pixi.js";
import type { Chart } from "./Chart";

export interface IChartTouch {
  id: number;
  last: PointData | null;
}

export class InputManager {
  public readonly chart: Chart;
  public clickedAvailable?: boolean;
  public isMouseDown?: boolean;
  public last?: Point | null;
  public wheelFunction?: (e: WheelEvent) => void;
  public touches: IChartTouch[];

  constructor(chart: Chart) {
    this.chart = chart;
    this.touches = [];
    this.addListeners();
  }

  public destroy(): void {
    this.chart.options.events.domElement?.removeEventListener('wheel', this.wheelFunction as any);
  }

  private addListeners() {
    this.chart.eventMode = 'static';
    this.chart.hitArea = new Rectangle(0, 0, this.chart.graphWidth, this.chart.graphHeight);
    this.chart.on('pointerdown', this.handlePointerDown, this);
    this.chart.on('pointermove', this.moveChart, this);
    this.chart.on('pointerup', this.handlePointerUp, this);
    this.wheelFunction = (e) => this.handleWheel(e);
    this.chart.options.events.domElement.addEventListener(
      'wheel',
      this.wheelFunction as any,
      { passive: false }
    )
    this.isMouseDown = false;
  }

  public handlePointerDown(event: FederatedPointerEvent): void {
    if (!this.chart.visible) return;
    if (event.pointerType === 'mouse') this.isMouseDown = true;
    else if (!this.get(event.pointerId)) this.touches.push({ id: event.pointerId, last: null });
    if (!(this.count() === 1)) this.clickedAvailable = false;
    this.last = event.global.clone();
    this.clickedAvailable = false;
    this.chart.actions.handlePointerDown(event);
  }

  public clear(): void {
    this.isMouseDown = false;
    this.touches = [];
    this.last = null;
  }

  public moveChart(event: FederatedPointerEvent): void {
    if (!this.chart.visible) return;
    this.chart.actions.moveChart(event);
    if (this.clickedAvailable && this.last) {
      const distX = event.global.x - this.last.x;
      const distY = event.global.y - this.last.y;
      if (Math.abs(distX) >= this.chart.threshold || Math.abs(distY) >= this.chart.threshold) this.clickedAvailable = false;
    }
  }

  public breaksThreshold(change: number): boolean {
    return Math.abs(change) >= this.chart.threshold;
  }

  public handlePointerUp(event: FederatedPointerEvent): void {
    if (!this.chart.visible) return;
    if (event.pointerType === 'mouse') { this.isMouseDown = false; }
    if (event.pointerType !== 'mouse') { this.remove(event.pointerId); }
    this.chart.actions.handlePointerUp(event);
    if (this.clickedAvailable && (this.isMouseDown ? 1 : 0) + this.touches.length === 0 && this.last) {
      this.chart.emit('clicked', {
        event,
        graph: this.chart.toGraph(this.last),
        chart: this.chart,

      });
      this.clickedAvailable = false;
    }
  }

  public getPointerPosition(event: WheelEvent): Point {
    const point = new Point();
    this.chart.options.events.mapPositionToPoint(point, event.clientX, event.clientY);
    return point
  }

  public handleWheel(event: WheelEvent): void {
    if (!this.chart.visible) return;
    const point = this.chart.toLocal(this.getPointerPosition(event));
    this.chart
    const pointerInChart = this.chart.left <= point.x && point.x <= this.chart.right && this.chart.top <= point.y && point.y <= this.chart.bottom;
    if (pointerInChart) this.chart.actions.wheel(event);
  }

  public get(id: number): IChartTouch | null {
    for (const touch of this.touches) {
      if (touch.id === id) return touch;
    }
    return null;
  }

  public count(): number { return (this.isMouseDown ? 1 : 0) + this.touches.length; }
  remove(id: number): void {
    for (let i = 0; i < this.touches.length; i++) {
      if (this.touches[i].id === id) { this.touches.splice(i, 1); return; }
    }
  }

}
