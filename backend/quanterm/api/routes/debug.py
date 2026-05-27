import os
import tracemalloc
from fastapi import APIRouter, Query

router = APIRouter(prefix="/debug", tags=["debug"])

# Global variable to store our baseline snapshot
_old_snapshot: tracemalloc.Snapshot | None = None


@router.get("/memory")
async def profile_memory(
    action: str = Query("stats", description="Options: 'snapshot', 'diff', 'stats'"),
):
    global _old_snapshot

    if action == "snapshot":
        # Capture the current memory footprint as our baseline
        _old_snapshot = tracemalloc.take_snapshot()
        return {"status": "Baseline snapshot stored successfully!"}

    if action == "diff":
        if not _old_snapshot:
            return {"error": "No baseline snapshot found. Call ?action=snapshot first."}

        current_snapshot = tracemalloc.take_snapshot()

        # Compare current memory against the old baseline, grouped by filename and line number
        stats = current_snapshot.compare_to(_old_snapshot, "lineno")

        # Filter out external library noise and focus on your source code or high-growth zones
        report = []
        for stat in stats[:15]:  # Top 15 memory hoarders
            # Format file path to be readable
            frame = stat.traceback[0]
            filename = frame.filename

            # Clean up long virtual environment paths for readability
            if ".venv" in filename:
                filename = filename.split(".venv")[-1]
            elif "site-packages" in filename:
                filename = filename.split("site-packages")[-1]

            report.append(
                {
                    "file": f"{filename}:{frame.lineno}",
                    "memory_growth_mb": round(stat.size_diff / (1024 * 1024), 3),
                    "total_allocated_mb": round(stat.size / (1024 * 1024), 3),
                    "allocation_count": stat.count,
                }
            )

        return {
            "message": "Memory growth since baseline snapshot",
            "top_allocations": report,
        }

    # Default action: Just show current top memory consumers overall
    current_snapshot = tracemalloc.take_snapshot()
    top_stats = current_snapshot.statistics("filename")

    return {
        "current_top_files": [
            {"file": str(stat.key), "size_mb": round(stat.size / (1024 * 1024), 2)}
            for stat in top_stats[:10]
        ]
    }
