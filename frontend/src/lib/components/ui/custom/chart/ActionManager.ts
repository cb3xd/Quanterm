import { FederatedEvent } from "pixi.js";
import { Chart } from "./Chart";
import type { Action, Drag, Wheel } from "./chart-actions/index.ts";

const ACTION_ORDER = [
  "drag",
  "pinch",
  "wheel",
]
export class ActionManager {
  public actions: Partial<Record<string, Action>>;
  public list: Array<Action>;
  public readonly chart: Chart;

  constructor(chart: Chart) {
    this.chart = chart;
    this.list = [];
    this.actions = {};
  }

  public add(name: string, action: Action, index: number = ACTION_ORDER.length) {
    const oldAction = this.actions[name];
    if (oldAction) oldAction.destroy();
    this.actions[name] = action;

    const current = ACTION_ORDER.indexOf(name);
    if (current !== -1) ACTION_ORDER.splice(current, 1);
    ACTION_ORDER.splice(index, 0, name);
    this.sort();
  }
  public moveChart(event: FederatedEvent): boolean {
    let stop = false;
    for (const action of this.chart.actions.list) if (action.moveChart(event)) stop = true;
    return stop;
  }

  public handlePointerUp(event: FederatedEvent): boolean {
    let stop = false;
    for (const action of this.list) {
      if (action.handlePointerUp(event)) stop = true;
    }
    return stop;
  }

  public handlePointerDown(event: FederatedEvent): boolean {
    let stop = false;
    for (const action of this.list) {
      if (action.handlePointerDown(event)) stop = true;
    }
    return stop;
  }
  public get(name: 'drag'): Drag | undefined | null;
  public get(name: 'wheel'): Wheel | undefined | null;
  public get<T extends Action = Action>(name: string): T | undefined | null;
  public get<T extends Action = Action>(name: string): T | undefined | null {
    return this.actions[name] as T;
  }
  public reset(): void {
    this.list.forEach((action) => { action.destroy(); })
  }
  public sort() {
    this.list = [];
    for (const action of ACTION_ORDER) {
      if (this.actions[action]) this.list.push(this.actions[action] as Action);
    }
  }
  public wheel(e: WheelEvent): boolean {
    let result = false;
    for (const action of this.list) {
      if (action.wheel(e)) result = true;
    }
    return result;
  }
}
