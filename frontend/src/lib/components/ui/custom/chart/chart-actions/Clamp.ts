import { Point } from "pixi.js";
import { Chart } from "../Chart.ts";
import { Action } from "./Action.ts";

export interface IClampOptions {
  left?: number | boolean | null;
  top?: number | boolean | null;
  bottom?: number | boolean | null;
  right?: number | boolean | null;

  direction?: 'all' | 'x' | 'y' | null;
}

const DEFAULT_CLAMP_OPTIONS: Required<IClampOptions> = {
  left: 0,
  right: true,
  top: 0,
  bottom: null,
  direction: null,
};

export class Clamp extends Action {
  public readonly options: Required<IClampOptions>;

  protected last: {
    x: number | null;
    y: number | null;
    scaleX: number | null;
    scaleY: number | null;
  };

  constructor(chart: Chart, options: IClampOptions = {}) {
    super(chart);
    this.options = Object.assign({}, DEFAULT_CLAMP_OPTIONS, options);
    if (this.options.direction) {
      this.options.left
        = this.options.direction === 'x' || this.options.direction === 'all'
          ? true
          : null;
      this.options.right
        = this.options.direction === 'x' || this.options.direction === 'all'
          ? true
          : null;
      this.options.top
        = this.options.direction === 'y' || this.options.direction === 'all'
          ? true
          : null;
      this.options.bottom
        = this.options.direction === 'y' || this.options.direction === 'all'
          ? true
          : null;
    }
  }

  public move(): boolean {
    this.update();
    return false;
  }

  public update(): void {
    if (this.hasNoChange()) {
      return;
    }

    const original = new Point(this.chart.x, this.chart.y);

    this.clampHorizontal(original);
    this.clampVertical(original);

    this.updateLastState();
  }

  private hasNoChange(): boolean {
    return (
      this.chart.x === this.last.x &&
      this.chart.y === this.last.y &&
      this.chart.scale.x === this.last.scaleX &&
      this.chart.scale.y === this.last.scaleY
    );
  }

  private clampHorizontal(original: Point): void {
    if (this.options.left === null && this.options.right === null) {
      return;
    }

    let moved = false;

    if (this.options.left !== null) {
      moved = this.clampLeftBound() || moved;
    }

    if (this.options.right !== null) {
      moved = this.clampRightBound() || moved;
    }

    if (moved) {
      this.emitMoved(original, 'clamp-x');
    }
  }

  private clampVertical(original: Point): void {
    if (this.options.top === null && this.options.bottom === null) {
      return;
    }

    let moved = false;

    if (this.options.top !== null) {
      moved = this.clampTopBound() || moved;
    }

    if (this.options.bottom !== null) {
      moved = this.clampBottomBound() || moved;
    }

    if (moved) {
      this.emitMoved(original, 'clamp-y');
    }
  }

  private clampLeftBound(): boolean {
    const leftBound = this.options.left === true ? 0 : (this.options.left as number);

    if (this.chart.left < leftBound) {
      this.chart.x = -leftBound * this.chart.scale.x;
      return true;
    }

    return false;
  }

  private clampRightBound(): boolean {
    const rightBound = this.options.right === true
      ? this.chart.graphWidth
      : (this.options.right as number);

    if (this.chart.right > rightBound) {
      this.chart.x = -rightBound * this.chart.scale.x + this.chart.screenWidth;
      return true;
    }

    return false;
  }

  private clampTopBound(): boolean {
    const topBound = this.options.top === true ? 0 : (this.options.top as number);

    if (this.chart.top < topBound) {
      this.chart.y = -topBound * this.chart.scale.y;
      return true;
    }

    return false;
  }

  private clampBottomBound(): boolean {
    const bottomBound = this.options.bottom === true
      ? this.chart.graphHeight
      : (this.options.bottom as number);

    if (this.chart.bottom > bottomBound) {
      this.chart.y = -bottomBound * this.chart.scale.y + this.chart.screenHeight;
      return true;
    }

    return false;
  }

  private emitMoved(original: Point, type: string): void {
    this.chart.emit('moved', {
      chart: this.chart,
      original,
      type,
    });
  }

  private updateLastState(): void {
    this.last.x = this.chart.x;
    this.last.y = this.chart.y;
    this.last.scaleX = this.chart.scale.x;
    this.last.scaleY = this.chart.scale.y;
  }

  public reset(): void { this.update(); }
}
