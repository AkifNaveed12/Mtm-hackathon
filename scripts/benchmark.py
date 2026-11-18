"""Bounded full-pack plus two practice updates; no WhatsApp requests.

Usage: python scripts/benchmark.py offline|provider [workspace]
Workspace mode requires the API process stopped to avoid concurrent writers.
Partial failures are saved honestly, with their actual provider traces.
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    from backend.app.engine.pipeline import PlanningEngine, global_engine

    mode = sys.argv[1] if len(sys.argv) > 1 else os.getenv("PLANNER_MODE", "offline")
    if mode not in {"offline", "provider", "auto"}:
        raise ValueError("Mode must be offline, provider or auto.")
    output_dir = ROOT / "data"
    output_dir.mkdir(exist_ok=True)
    engine = global_engine if "workspace" in sys.argv[2:] else PlanningEngine(
        database_path=str(output_dir / f"benchmark-{mode}-{uuid.uuid4().hex[:8]}.sqlite3"))
    rows = []
    initial_calls = engine.tracer.get_log().total_calls
    before = initial_calls
    start = time.perf_counter()
    failed = False
    try:
        plan, checks = engine.run_full_pipeline((ROOT / "sample_pack.txt").read_bytes().decode("utf-8"), mode=mode)
        rows.append({"operation": "initial", "seconds": round(time.perf_counter()-start, 3),
                     "calls": engine.tracer.get_log().total_calls-before,
                     "all_checks_passed": checks.all_passed, "extraction_mode": plan.extraction_mode,
                     "meals": plan.food.headcount, "projected_budget": plan.budget.total_projected})
    except Exception as error:
        failed = True
        rows.append({"operation": "initial", "seconds": round(time.perf_counter()-start, 3),
                     "calls": engine.tracer.get_log().total_calls-before, "status": "error",
                     "error_type": type(error).__name__, "all_checks_passed": False})
    if not failed and checks.all_passed:
        for filename, sender, expected in [("printing_update.txt", "Finance", True),
                                            ("catering_invalid.txt", "Caterer", False)]:
            text = (ROOT / "tests" / "fixtures" / filename).read_bytes().decode("utf-8")
            before_plan = plan.model_dump()
            before = engine.tracer.get_log().total_calls
            start = time.perf_counter()
            try:
                accepted, reason, plan, checks = engine.process_incremental_message(text, sender, mode=mode)
                rows.append({"operation": filename, "seconds": round(time.perf_counter()-start, 3),
                             "calls": engine.tracer.get_log().total_calls-before,
                             "accepted": accepted, "expected_acceptance": expected,
                             "all_checks_passed": checks.all_passed, "rejection_reason": reason,
                             "previous_plan_preserved": before_plan == plan.model_dump() if not accepted else None,
                             "unaffected_venue_preserved": before_plan["venue"] == plan.venue.model_dump(),
                             "unaffected_schedule_preserved": before_plan["schedule"] == plan.schedule.model_dump(),
                             "printing_delta_correct": abs(plan.budget.total_projected - before_plan["budget"]["total_projected"] - 5000) < 0.001 if expected else None,
                             "projected_budget": plan.budget.total_projected})
            except Exception as error:
                failed = True
                rows.append({"operation": filename, "seconds": round(time.perf_counter()-start, 3),
                             "calls": engine.tracer.get_log().total_calls-before, "status": "error",
                             "error_type": type(error).__name__, "all_checks_passed": False,
                             "previous_plan_preserved": before_plan == engine.active_plan.model_dump()})
                break
    trace = engine.tracer.get_log().model_dump()
    attempt_entries = trace["entries"][initial_calls:]
    okay = not failed and len(rows) == 3 and all(row["all_checks_passed"] for row in rows)
    okay = okay and rows[0]["seconds"] < 120 and all(row["seconds"] < 60 and row["calls"] <= 5 for row in rows[1:])
    okay = okay and all(row.get("accepted") == row.get("expected_acceptance") for row in rows[1:])
    okay = okay and all(row.get("printing_delta_correct") is not False for row in rows)
    verified = bool(okay and mode == "provider" and attempt_entries and all(e["status"] == "success" for e in attempt_entries))
    result = {"mode": mode, "actual_provider_verified": verified, "results": rows,
              "attempt_entries": attempt_entries, "trace": trace,
              "plan": engine.active_plan.model_dump(), "checks": engine.checks.model_dump()}
    (output_dir / f"benchmark-{mode}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"mode": mode, "actual_provider_verified": verified, "results": rows,
                      "models": sorted({entry["model_name"] for entry in attempt_entries}),
                      "attempt_model_calls": len(attempt_entries),
                      "attempt_reported_tokens": sum(e["total_tokens"] or 0 for e in attempt_entries),
                      "attempt_usage_complete": all(e["total_tokens"] is not None for e in attempt_entries),
                      "historical_trace_calls": trace["total_calls"],
                      "historical_trace_reported_tokens": trace["overall_total_tokens"]}, indent=2))
    return 0 if okay else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Benchmark stopped ({type(error).__name__}); no successful provider result is claimed.")
        raise SystemExit(1)
