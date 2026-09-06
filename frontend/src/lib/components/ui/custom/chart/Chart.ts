import { Container, DestroyOptions, EventSystem, Point, PointData, Rectangle, Ticker } from "pixi.js";
import { InputManager } from "./InputManager.ts";
import { ActionManager } from "./ActionManager.ts";
import { Drag, type IDragOptions } from "./chart-actions/Drag.ts";
import { Wheel, type IWheelOptions } from "./chart-actions/Wheel.ts";

export interface IChartTransformState {
  x: number;
  y: number;
  scaleX: number;
  scaleY: number;
}

export interface IChartOptions {
  maxWidth?: number | null;
  maxHeight?: number | null;
  threshold?: number;
  ticker: Ticker;
  container: HTMLDivElement;
  events: EventSystem;
}

export interface ICompleteChartOptions extends IChartOptions {
  threshold: number;
  ticker: Ticker
  container: HTMLDivElement
}


const DEFAULT_CHART_OPTIONS: Partial<ICompleteChartOptions> = {
  maxWidth: null,
  maxHeight: null,
  threshold: 1,
}


export class Chart extends Container {

  public moving?: boolean;
  public screenWidth: number;
  public screenHeight: number;
  public threshold: number;
  public readonly input: InputManager;
  public readonly actions: ActionManager;
  public zooming?: boolean;
  public lastChart?: IChartTransformState | null;
  public readonly options: ICompleteChartOptions;
  private _graphWidth?: number | null;
  private _graphHeight?: number | null;
  private _hitAreaDefault?: Rectangle;
  private _dirty?: boolean;

  private readonly tickerFunction?: () => void;
  constructor(options: IChartOptions) {
    super();
    this.options = { ...DEFAULT_CHART_OPTIONS, ...options, } as ICompleteChartOptions;
    this.screenWidth = this.options.container.clientWidth;
    this.screenHeight = this.options.container.clientHeight;
    this.threshold = this.options.threshold;
    this._graphWidth = this.screenWidth * 9;
    this._graphHeight = this.screenHeight * 16
    this.tickerFunction = () => this.update();
    this.input = new InputManager(this);
    this.actions = new ActionManager(this);
    this.tickerFunction = () => this.update();
    this.options.ticker.add(this.tickerFunction);
  }
  destroy(options?: DestroyOptions): void {
    if (this.tickerFunction) this.options.ticker.remove(this.tickerFunction);
    this.input.destroy();
    super.destroy(options);
  }
  update(): void {
    if (!this.lastChart) return;
    if (this.lastChart.x !== this.x || this.lastChart.y !== this.y) this.moving = true;
    else if (this.moving) {
      this.emit('move-end', this);
      this.moving = false;
    }
    if (this.lastChart.scaleX !== this.scale.x || this.lastChart.scaleY !== this.scale.y) this.zooming = true;
    else if (this.zooming) {
      this.emit('zoom-end', this);
      this.zooming = false;
    }

    this._hitAreaDefault = new Rectangle(this.left, this.top, this.graphScreenWidth, this.graphScreenHeight);
    this.hitArea = this._hitAreaDefault;

    this._dirty =
      this._dirty ||
      !this.lastChart ||
      this.lastChart.x !== this.x ||
      this.lastChart.y !== this.y ||
      this.lastChart.scaleX !== this.scale.x ||
      this.lastChart.scaleY !== this.scale.y;

    this.lastChart = {
      x: this.x,
      y: this.y,
      scaleX: this.scale.x,
      scaleY: this.scale.y
    };

    this.emit('frame-end', this);
  }

  public drag(options?: IDragOptions): Chart {
    this.actions.add('drag', new Drag(this, options));
    return this;
  }

  public wheel(options?: IWheelOptions): Chart {
    this.actions.add('wheel', new Wheel(this, options));
    return this;
  }

  resize(
    screenWidth: number = this.options.container.clientWidth,
    screenHeight: number = this.options.container.clientHeight,
    maxWidth?: number,
    maxHeight?: number

  ): void {
    this.screenWidth = screenWidth;
    this.screenHeight = screenHeight;


    if (typeof maxWidth !== 'undefined') this._graphWidth = maxWidth;
    if (typeof maxHeight !== 'undefined') this._graphHeight = maxHeight;
    this.dirty = true;
  }


  public moveCenter(x: number, y: number): Chart;
  public moveCenter(center: PointData): Chart;
  public moveCenter(...args: [number, number] | [PointData]): Chart {
    let x, y: number;

    if (typeof args[0] === 'number') {
      x = args[0];
      y = args[1] as number;
    } else {
      x = args[0].x;
      y = args[0].y;
    }

    const newX = ((this.graphScreenWidth / 2) - x) * this.scale.x;
    const newY = ((this.graphScreenWidth / 2) - y) * this.scale.y;

    if (!(this.x !== newX || this.y !== newY)) return this;

    this.position.set(newX, newY);
    this.actions.reset();
    this.dirty = true;
    return this;
  }

  get left(): number { return -this.x / this.scale.x; }
  set left(value: number) {
    this.x = -value * this.scale.x;
    this.actions.reset();
  }

  get right(): number { return (-this.x / this.scale.x) + this.graphScreenWidth; }
  set right(value: number) {
    this.x = (-value * this.scale.x) + this.screenWidth;
    this.actions.reset();
  }

  get top(): number { return -this.y / this.scale.y; }
  set top(value: number) {
    this.y = -value * this.scale.y;
    this.actions.reset();
  }

  get bottom(): number { return (-this.y / this.scale.y) + this.graphScreenHeight; }
  set bottom(value: number) {
    this.y = (-value * this.scale.y) + this.screenHeight;
    this.actions.reset();
  }

  get dirty(): boolean { return !!this._dirty; }
  set dirty(value: boolean) { this._dirty = value; }

  get graphWidth(): number {
    if (this._graphWidth) return this._graphWidth;
    return this.width / this.scale.x;
  }
  get graphHeight(): number {
    if (this._graphHeight) return this._graphHeight;
    return this.height / this.scale.y;
  }

  set graphWidth(value: number) { this._graphWidth = value; }
  set graphHeight(value: number) { this._graphHeight = value; }

  public getVisibleBounds(): Rectangle { return new Rectangle(this.left, this.top, this.graphScreenWidth, this.graphScreenHeight); }
  public toGraph<P extends PointData = Point>(x: number, y: number): P;
  public toGraph<P extends PointData = Point>(screenPoint: PointData): P;

  public toGraph<P extends PointData = Point>(x: number | PointData, y?: number): P {
    if (arguments.length === 2) return this.toGlobal<P>(new Point(x as number, y))
    return this.toGlobal<P>(x as PointData);
  }

  get graphScreenWidth(): number { return this.screenWidth / this.scale.x; }
  get graphScreenHeight(): number { return this.screenHeight / this.scale.y; }

  get screenGraphWidth(): number { return this.graphWidth * this.scale.x; }
  get screenGraphHeight(): number { return this.graphHeight * this.scale.y; }

  get center(): Point {
    return new Point((this.graphScreenWidth / 2) - (this.x / this.scale.x),
      (this.graphScreenHeight / 2) - (this.y / this.scale.y))
  }
  set center(value: Point) { this.moveCenter(value); }
}
