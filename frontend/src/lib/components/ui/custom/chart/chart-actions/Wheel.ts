import { Point, PointData } from "pixi.js";
import { Action } from ".";
import { Chart } from "../Chart";

export interface IWheelOptions {
  percent?: number;
  smooth?: false | number;
  interrupt?: boolean;
  lineHeight?: number;
  axis?: 'all' | 'x' | 'y';
  wheelZoom?: boolean;
}

const DEFAULT_WHEEL_OPTIONS: Required<IWheelOptions> = {
  percent: 0.1,
  smooth: false,
  interrupt: true,
  lineHeight: 20,
  axis: 'all',
  wheelZoom: true,
}

export class Wheel extends Action {
  public readonly options: Required<IWheelOptions>;

  protected smoothing?: PointData | null;
  protected smoothingCenter?: Point | null;
  protected smoothingCount?: number;
  protected axis: string;
  constructor(chart: Chart, options: IWheelOptions = {}) {
    super(chart);
    this.options = Object.assign({}, DEFAULT_WHEEL_OPTIONS, options);
    this.axis = this.options.axis;
  }

  protected adjustChartForZoom(oldPoint: PointData | undefined, point: PointData): void {
    const targetParent = this.chart.parent || this.chart;
    targetParent.toLocal(oldPoint as PointData, this.chart, oldPoint);
    const comparePoint = targetParent.toLocal(point as PointData);
    this.chart.y += comparePoint.y - (oldPoint as PointData).y;
    this.chart.emit('moved', { chart: this.chart, type: 'wheel' });
  }
  public update(): void {
    if (!this.smoothing) return;
    const point = this.smoothingCenter;
    const change = this.smoothing;
    const oldPoint = this.chart.toLocal(point as PointData);;

    if (this.axis === 'all') { this.chart.scale.x += change.x; this.chart.scale.y += change.y; }
    else if (this.axis === 'x') this.chart.scale.x += change.x;
    else this.chart.scale.y += change.y;

    this.chart.emit('zoomed', { chart: this.chart, type: 'wheel' });
    (this.smoothingCount as number)++;
    if (typeof this.options.smooth === 'number' && (this.smoothingCount as number) >= this.options.smooth) this.smoothing = null;

    this.adjustChartForZoom(oldPoint, point as PointData);
  }

  public handlePointerDown(): boolean {
    if (this.options.interrupt) this.smoothing = null;
    return false;
  }
  private pinch(e: WheelEvent) {
    const point = this.chart.input.getPointerPosition(e);
    const step = (-e.deltaY * (e.deltaMode ? this.options.lineHeight : 1)) / 200;
    const change = Math.pow(2, (1 + this.options.percent) * step);
    const oldPoint = this.chart.toLocal(point);;


    if (this.axis === 'all') { this.chart.scale.x *= change; this.chart.scale.y *= change; }
    else if (this.axis === 'x') this.chart.scale.x *= change;
    else this.chart.scale.y += change;

    this.chart.emit('zoomed', { chart: this.chart, type: 'wheel' });
    this.chart.emit('moved', { chart: this.chart, type: 'wheel' });
    this.chart.emit('wheel-start', { event: e, chart: this.chart });

    this.adjustChartForZoom(oldPoint, point as PointData);
  }

  public wheel(e: WheelEvent): boolean {
    if (!this.options.wheelZoom) return true;
    const point = this.chart.input.getPointerPosition(e);
    const step = (-e.deltaY * (e.deltaMode ? this.options.lineHeight : 1)) / 500;
    const change = Math.pow(2, (1 + this.options.percent) * step);

    if (this.options.smooth) {
      const x = this.smoothing ? this.smoothing.x * (this.options.smooth - (this.smoothingCount as number)) : 0
      const y = this.smoothing ? this.smoothing.y * (this.options.smooth - (this.smoothingCount as number)) : 0
      const original = { x: x, y: y };
      const smoothingX = ((this.chart.scale.x + original.x) * change - this.chart.scale.x) / this.options.smooth;
      const smoothingY = ((this.chart.scale.y + original.y) * change - this.chart.scale.y) / this.options.smooth;
      this.smoothing = { x: smoothingX, y: smoothingY };
    }
    else {
      const oldPoint = this.chart.toLocal(point);

      if (this.axis === 'all') { this.chart.scale.x *= change; this.chart.scale.y *= change; }
      else if (this.axis === 'x') this.chart.scale.x *= change;
      else this.chart.scale.y += change;

      this.chart.emit('zoomed', { chart: this.chart, type: 'wheel' });

      this.adjustChartForZoom(oldPoint, point as PointData);

    }
    return true;

  }

}
