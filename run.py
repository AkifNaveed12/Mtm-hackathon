"""One command for a full message pack or one incremental message file."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    from backend.app.engine.ingestor import parse_raw_message_pack
    from backend.app.engine.pipeline import global_engine

    started = time.perf_counter()
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sample_pack.txt"
    try:
        if source.stat().st_size > 256_000:
            raise ValueError("Message file exceeds the 256 KB local limit.")
        raw_text = source.read_bytes().decode("utf-8")
    except (OSError, UnicodeError, ValueError):
        print("Cannot read the message file. Supply an existing UTF-8 TXT file under 256 KB.")
        return 1
    if not raw_text.strip():
        print("Message file is empty.")
        return 1
    print("HackPlan AI | Mind to Machine | local planning harness")
    print(f"Input: {source.name}")
    try:
        messages = parse_raw_message_pack(raw_text)
        is_full = len(messages) > 1 or not global_engine.active_facts
        before_calls = global_engine.tracer.get_log().total_calls
        if is_full:
            plan, checks = global_engine.run_full_pipeline(raw_text)
            accepted, rejection = checks.all_passed, None
        else:
            sender = messages[0].get("sender", "External") if messages else "External"
            accepted, rejection, plan, checks = global_engine.process_incremental_message(raw_text, sender)
        print(f"Operation: {'full plan' if is_full else 'incremental update'}")
        if rejection:
            print(f"REJECTED: {rejection}")
            print("The previous plan was preserved.")
        global_engine.tracer.print_trace()
        print("\nQuality checks")
        for field, label in [
            ("figures_valid", "Figures"), ("budget_valid", "Budget"),
            ("venue_fits", "Venue"), ("schedule_valid", "Schedule"),
            ("enough_judges", "Judging"), ("all_areas_covered", "Coverage"),
        ]:
            print(f"  {label}: {'PASS' if getattr(checks, field) else 'FAIL'}")
        print("\nOperational plan")
        print(f"Venue: {plan.venue.selected_room or 'Unresolved'}; {plan.venue.capacity} seats; Rs {plan.venue.cost:,.2f}")
        print(f"Schedule: {plan.schedule.total_duration_hours:g} hours; prayer break {plan.schedule.prayer_break_minutes} minutes")
        for item in plan.schedule.timeline:
            print(f"  {item.time_slot}: {item.activity} ({item.duration_mins} min)")
        print(f"Food: {plan.food.headcount} meals; {plan.food.caterer_tier}; total Rs {plan.food.total_cost:,.2f}")
        print(f"Judging: {plan.judging.confirmed_judges} confirmed judges; {plan.judging.selected_judges} assigned; {plan.judging.teams_count} teams")
        print(f"Budget: Rs {plan.budget.total_projected:,.2f} of Rs {plan.budget.cap:,.2f}; remaining Rs {plan.budget.surplus_deficit:,.2f}")
        for issue in plan.unresolved_constraints:
            print(f"UNRESOLVED: {issue}")
        elapsed = time.perf_counter() - started
        log = global_engine.tracer.get_log()
        artifact = {
            "competition": "Mind to Machine Hackathon 2026",
            "operation": "full" if is_full else "update", "accepted": accepted,
            "rejection_reason": rejection, "duration_seconds": round(elapsed, 3),
            "plan": plan.model_dump(), "checks": checks.model_dump(),
            "trace": log.model_dump(),
            "rejected_messages": [r.model_dump() for r in global_engine.rejected_records],
        }
        output_dir = ROOT / "data"
        output_dir.mkdir(exist_ok=True)
        (output_dir / "submission.json").write_text(json.dumps(artifact, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nElapsed: {elapsed:.3f}s; limit: {120 if is_full else 60}s")
        calls = log.total_calls - before_calls if not is_full else log.total_calls
        print(f"Model calls for operation: {calls}; provider-reported trace tokens: {log.overall_total_tokens}")
        if not log.usage_complete:
            print("Some provider token usage was unavailable; totals include reported usage only.")
        print("Saved plan and full trace: data/submission.json")
        return 0 if checks.all_passed else 1
    except Exception as exc:
        # Provider exceptions may embed request headers. Never print exception text.
        print(f"Planning failed ({type(exc).__name__}). Inspect the dashboard's safe execution diagnostics.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
