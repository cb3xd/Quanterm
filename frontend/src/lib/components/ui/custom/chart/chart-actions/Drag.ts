import type { FederatedPointerEvent, PointData } from "pixi.js";
import { Point } from "pixi.js";
import { Chart } from "../Chart";
import { Action } from "./Action";

export interface IDragOptions {
  direction?: string;
  wheel?: boolean;
  wheelScroll?: number;
  factor?: number;
  lineHeight?: number;
}
const DEFAULT_DRAG_OPTIONS: Required<IDragOptions> = {
  direction: 'all',
  wheel: true,
  wheelScroll: 1,
  factor: 1,
  lineHeight: 20,
}


export class Drag extends Action {
  public readonly options: Readonly<Required<IDragOptions>>;
  protected moved: boolean;
  protected xDirection: boolean;
  protected yDirection: boolean;
  protected last?: PointData | null;
  protected current?: number;
  protected activeButton?: number;
  private windowEventHandlers: Array<{
    event: string;
    handler: (e: any) => void;
  }> = [];

  constructor(chart: Chart, options = {}) {
    super(chart);

    this.options = Object.assign({}, DEFAULT_DRAG_OPTIONS, options);
    this.moved = false;
    this.xDirection
      = !this.options.direction
      || this.options.direction === 'all'
      || this.options.direction === 'x';
    this.yDirection
      = !this.options.direction
      || this.options.direction === 'all'
      || this.options.direction === 'y';
  }

  public moveChart(event: FederatedPointerEvent): boolean {
    if (!(this.last && this.current === event.pointerId)) return false;

    if (event.pointerType === 'mouse' && !(event.buttons & 4)) {
      this.last = null;
      this.moved = false;
      return false
    }
    const x = event.global.x;
    const y = event.global.y;
    const count = this.chart.input.count();

    if (count !== 1) { this.moved = false; return false; }
    const newPoint = { x, y };
    (this.chart.parent || this.chart).toLocal(
      newPoint,
      undefined,
      newPoint
    );

    const dX = newPoint.x - this.last.x;
    const dY = newPoint.y - this.last.y;

    const hasMovedEnough = this.moved || (this.xDirection && this.chart.input.breaksThreshold(dX)) || (this.yDirection && this.chart.input.breaksThreshold(dY));
    if (!hasMovedEnough) return false;

    if (this.xDirection) this.chart.x += dX * this.options.factor;
    if (this.xDirection) this.chart.y += dY * this.options.factor;

    this.last = newPoint;

    if (!this.moved) this.chart.emit('drag-start', {
      event,
      screen: new Point(this.last.x, this.last.y),
      graph: this.chart.toGraph(new Point(this.last.x, this.last.y)),
      chart: this.chart
    });

    this.moved = true;
    this.chart.emit('moved', { chart: this.chart, type: 'drag' });
    return true;

  }
  public handlePointerUp(event: FederatedPointerEvent): boolean {
    if (!(this.last && this.moved)) return false;

    const screen = new Point(this.last.x, this.last.y);
    (this.chart.parent || this.chart).toGlobal(screen, screen, true);
    this.chart.emit('drag-end', { event, screen, graph: this.chart.toGraph(screen), chart: this.chart });

    this.last = null;
    this.moved = false;
    return true;
  }

  public handlePointerDown(event: FederatedPointerEvent): boolean {
    if (event.pointerType === 'mouse' && event.button !== 1) return false;
    this.activeButton = event.button;
    this.last = { x: event.global.x, y: event.global.y };
    (this.chart.parent || this.chart).toLocal(this.last, undefined, this.last);
    this.current = event.pointerId;
    return true;

  }

  public wheel(event: WheelEvent): boolean {
    if (!(this.options.wheel)) return false;

    const wheel = this.chart.actions.get('wheel');

    if (!(!wheel || (!wheel.options.wheelZoom && !event.ctrlKey))) return false;

    const step = event.deltaMode ? this.options.lineHeight : 1;

    if (this.xDirection) this.chart.x += event.deltaX * step * this.options.wheelScroll;
    if (this.yDirection) this.chart.y += event.deltaY * step * this.options.wheelScroll;
    this.chart.emit('wheel-scroll', this.chart);
    this.chart.emit('moved', { chart: this.chart, type: 'wheel' });
    return true;
  }

  public override destroy(): void {
    if (typeof window === 'undefined') return;
    this.windowEventHandlers.forEach(({ event, handler }) => { window.removeEventListener(event, handler) });
  }
}
