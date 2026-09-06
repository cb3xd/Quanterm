import { FederatedEvent } from "pixi.js";
import { Chart } from "../Chart";

export class Action {
  public readonly chart: Chart;

  constructor(chart: Chart) { this.chart = chart };

  public destroy() { }
  public handlePointerDown(_e: FederatedEvent): boolean { return false };
  public moveChart(_e: FederatedEvent): boolean { return false };
  public handlePointerUp(_e: FederatedEvent): boolean { return false };
  public wheel(_e: WheelEvent): boolean | undefined { return false };
  public update(_delta: number): void { }
  public resize() { }
  public reset(): void { }
}
