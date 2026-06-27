#!/usr/bin/env python3
"""
Quanterm Performance Testing Suite
Modified to use URL stream query composition for market data.
"""

import argparse
import asyncio
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx
import msgspec
import websockets

# Configuration Defaults
DEFAULT_WS_URL = "ws://127.0.0.1:8000/ws"
DEFAULT_HTTP_URL = "http://127.0.0.1:8000/api/all_exchange_symbols"
DEFAULT_DURATION = 30  # seconds


# ============================================================================
# SYSTEM MONITORING
# ============================================================================


def get_uvicorn_pids() -> list[str]:
    """Get all uvicorn process IDs."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "uvicorn"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            return [pid for pid in result.stdout.strip().split("\n") if pid]
        return []
    except FileNotFoundError:
        return []


def get_process_stats(pids: list[str]) -> Optional[dict]:
    """Get CPU and memory stats for given process IDs."""
    if not pids:
        return None

    try:
        pid_str = ",".join(pids)
        result = subprocess.run(
            ["ps", "-p", pid_str, "-o", "%cpu,rss", "--no-headers"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            cpu_total = 0.0
            mem_total = 0.0  # in KiB

            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        cpu_total += float(parts[0])
                        mem_total += float(parts[1])

            return {
                "cpu_percent": cpu_total,
                "mem_mb": mem_total / 1024,  # Convert KiB to MiB
            }
    except Exception:
        pass

    return None


class SystemMonitor:
    """Monitors CPU and memory usage of uvicorn process during test."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.stats = []
        self.running = False

    async def start(self):
        """Start background monitoring task."""
        if not self.enabled:
            return
        self.running = True
        asyncio.create_task(self._monitor_loop())

    async def stop(self):
        """Stop monitoring."""
        self.running = False

    async def _monitor_loop(self):
        """Background task that polls system stats every 0.1s."""
        while self.running:
            pids = get_uvicorn_pids()
            if pids:
                stats = get_process_stats(pids)
                if stats:
                    self.stats.append({"timestamp": time.monotonic(), **stats})
            await asyncio.sleep(0.1)

    def get_summary(self) -> dict:
        """Return aggregated statistics from monitoring period."""
        if not self.stats:
            return {}

        cpu_values = [s["cpu_percent"] for s in self.stats]
        mem_values = [s["mem_mb"] for s in self.stats]

        return {
            "cpu_avg": sum(cpu_values) / len(cpu_values),
            "cpu_max": max(cpu_values),
            "cpu_min": min(cpu_values),
            "mem_avg": sum(mem_values) / len(mem_values),
            "mem_max": max(mem_values),
            "mem_min": min(mem_values),
            "samples": len(self.stats),
        }


# ============================================================================
# WEBSOCKET TESTING
# ============================================================================


async def fetch_exchange_symbols(http_url: str) -> dict:
    """Fetches symbols from an endpoint returning dict[str, list[Exchange_ID]]."""
    print(f"Fetching target streams from {http_url}...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(http_url)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                print(f"Successfully parsed {len(data)} symbols from market map.")
                return data
            print("Endpoint did not return a dictionary structure.")
            return {}
    except Exception as e:
        print(f"Failed to fetch symbols from API: {e}")
        sys.exit(1)


async def reader_loop(ws, stop_event, stats):
    """Drains incoming frames continuously for the lifetime of the connection."""
    while not stop_event.is_set():
        try:
            msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
            stats["messages_received"] += 1
            stats["bytes_received"] += len(msg)

            if stats.get("verbose"):
                try:
                    parsed = json.loads(msg)
                    sys.stdout.write("\r\033[K")
                    print(f"[STREAM] {json.dumps(parsed, indent=2)}\n")
                except json.JSONDecodeError:
                    sys.stdout.write("\r\033[K")
                    print(f"[STREAM] non-JSON frame: {msg[:200]}")

        except asyncio.TimeoutError:
            continue
        except websockets.ConnectionClosed:
            print("\nWebSocket connection closed prematurely by server.")
            break


async def single_client_streamer(ws_url, symbol_map, stop_event, subs_done, stats):
    """Maintains a single connection using query-based stream inclusion."""
    connected = False

    # Compose streams parameter using the upgraded URL format logic
    streams = [f"trade_stream.{symbol.lower()}" for symbol in symbol_map.keys()]

    encoder = msgspec.json.Encoder()
    params = encoder.encode(
        {"method": "sub", "events": streams, "exchange": "binanceusdm"}
    )

    try:
        async with websockets.connect(DEFAULT_WS_URL) as ws:
            connected = True
            stats["connected"] = True
            stats["subs_sent"] = len(streams)
            subs_done.set()

            print(f"Connected to combined stream with {len(streams)} targets.")
            await ws.send(params)
            await reader_loop(ws, stop_event, stats)

    except Exception as e:
        stats["errors"] += 1
        key = type(e).__name__
        stats["error_types"][key] = stats["error_types"].get(key, 0) + 1
        print(f"\nConnection Error: {e}")
    finally:
        if connected:
            stats["connected"] = False
        subs_done.set()


async def progress_loop(stop_event, subs_done, stats, duration, streams_count, silent):
    """Prints live status during the live execution phase."""
    if silent:
        await stop_event.wait()
        return

    start = time.monotonic()
    while not stop_event.is_set():
        await asyncio.sleep(0.1)
        elapsed = time.monotonic() - start
        status = "ONLINE" if stats["connected"] else "OFFLINE"
        rate = stats["messages_received"] / max(elapsed, 0.01)

        if not subs_done.is_set():
            sys.stdout.write(
                f"\rConnecting and initializing streams... | Status: {status}"
            )
        else:
            live_elapsed = time.monotonic() - stats.get("subs_done_time", start)
            sys.stdout.write(
                f"\r[PROGRESS] {live_elapsed:.0f}/{duration}s | "
                f"Status: {status} | "
                f"Streams: {streams_count} | "
                f"Total Msgs: {stats['messages_received']} ({rate:.0f}/s) | "
                f"Errors: {stats['errors']}"
            )
        sys.stdout.flush()

    sys.stdout.write("\n")


# ============================================================================
# REPORTING
# ============================================================================


def print_results(ws_url, symbol_map, stats, duration, system_monitor):
    """Print formatted test results and optionally save to file."""
    wall_time = duration
    total_msgs = stats["messages_received"]
    total_bytes = stats["bytes_received"]
    throughput = total_msgs / wall_time if wall_time > 0 else 0

    print()
    print("=" * 70)
    print(f"  AGGREGATED STREAM RESULTS — {ws_url}")
    print("=" * 70)
    print(f"  Active Streams Subscribed: {len(symbol_map)}")
    print(f"  Messages received        : {total_msgs:,}")
    print(f"  Throughput               : {throughput:,.1f} msg/s")
    print(f"  Data received            : {total_bytes / 1024:,.1f} KiB")
    print(f"  Errors                   : {stats['errors']}")
    if stats.get("error_types"):
        for err_type, count in stats["error_types"].items():
            print(f"    {err_type}: {count}")

    if system_monitor.enabled:
        sys_stats = system_monitor.get_summary()
        if sys_stats:
            print()
            print("  SYSTEM RESOURCE USAGE")
            print(f"    CPU Avg  : {sys_stats['cpu_avg']:.1f}%")
            print(f"    CPU Max  : {sys_stats['cpu_max']:.1f}%")
            print(f"    CPU Min  : {sys_stats['cpu_min']:.1f}%")
            print(f"    Mem Avg  : {sys_stats['mem_avg']:.1f} MB")
            print(f"    Mem Max  : {sys_stats['mem_max']:.1f} MB")
            print(f"    Mem Min  : {sys_stats['mem_min']:.1f} MB")
            print(f"    Samples  : {sys_stats['samples']}")

    print("=" * 70)

    results = {
        "timestamp": datetime.now().isoformat(),
        "ws_url": ws_url,
        "duration_seconds": wall_time,
        "streams_subscribed": len(symbol_map),
        "messages_received": total_msgs,
        "throughput_msg_per_sec": throughput,
        "data_received_kib": total_bytes / 1024,
        "errors": stats["errors"],
    }

    if system_monitor.enabled:
        results["system"] = system_monitor.get_summary()

    results_file = Path("perf_results.json")
    try:
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {results_file.absolute()}")
    except Exception as e:
        print(f"\nCould not save results: {e}")


# ============================================================================
# MAIN
# ============================================================================


async def main():
    parser = argparse.ArgumentParser(
        description="Quanterm Performance Testing Suite",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--ws-url", default=DEFAULT_WS_URL, help="WebSocket target endpoint"
    )
    parser.add_argument(
        "--http-url", default=DEFAULT_HTTP_URL, help="HTTP API to fetch symbols from"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=DEFAULT_DURATION,
        help="Test run duration in seconds",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Pretty-print every incoming stream message",
    )
    parser.add_argument(
        "--silent", action="store_true", help="Suppress progress bar metrics"
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Enable live CPU/memory monitoring (requires pgrep)",
    )
    args = parser.parse_args()

    symbol_map = await fetch_exchange_symbols(args.http_url)
    if not symbol_map:
        print("No symbols returned from the API endpoint. Exiting.")
        return

    stats = {
        "connected": False,
        "messages_received": 0,
        "bytes_received": 0,
        "errors": 0,
        "error_types": {},
        "subs_sent": 0,
        "verbose": args.verbose,
    }

    if not args.silent:
        print(
            f"Preparing query parameter connection for {len(symbol_map)} streams, running for {args.duration}s"
        )
        if args.monitor:
            print("System monitoring enabled\n")

    stop_event = asyncio.Event()
    subs_done = asyncio.Event()

    system_monitor = SystemMonitor(enabled=args.monitor)
    await system_monitor.start()

    client_task = asyncio.create_task(
        single_client_streamer(args.ws_url, symbol_map, stop_event, subs_done, stats)
    )
    progress_task = asyncio.create_task(
        progress_loop(
            stop_event, subs_done, stats, args.duration, len(symbol_map), args.silent
        )
    )

    await subs_done.wait()
    stats["subs_done_time"] = time.monotonic()
    print(
        f"\nAll streams established via URL execution. Running for {args.duration}s..."
    )
    await asyncio.sleep(args.duration)
    stop_event.set()

    await asyncio.gather(client_task, progress_task, return_exceptions=True)
    await system_monitor.stop()

    print_results(args.ws_url, symbol_map, stats, args.duration, system_monitor)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
