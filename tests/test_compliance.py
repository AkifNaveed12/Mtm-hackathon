"""Official competition journeys with real deterministic planners and isolated state."""
import copy
import time

from backend.app.engine.pipeline import PlanningEngine
from backend.app.engine.tracer import ExecutionTracer


def test_full_pipeline_sample_pack_compliance(engine, sample_pack):
    started = time.monotonic()
    plan, checks = engine.run_full_pipeline(sample_pack, mode="offline")
    assert checks.all_passed, checks.model_dump()
    assert all(getattr(checks, name) for name in (
        "figures_valid", "budget_valid", "venue_fits", "schedule_valid",
        "enough_judges", "all_areas_covered",
    ))
    assert time.monotonic() - started < 120
    assert plan.judging.teams_count == 50
    assert plan.judging.confirmed_judges == 20
    assert plan.judging.selected_judges == 17
    assert plan.food.headcount == 177
    assert plan.judging.total_honoraria == 85000
    assert plan.raw_messages_count == 8
    assert plan.budget.cap == 650000
    assert sum(item.duration_mins for item in plan.schedule.timeline) == 240
    assert plan.schedule.prayer_break_minutes == 15
    assert plan.venue.capacity >= plan.food.headcount


def test_incremental_printing_expense_update_preserves_other_domains(engine, sample_pack):
    before, _ = engine.run_full_pipeline(sample_pack, mode="offline")
    before = copy.deepcopy(before)
    started = time.monotonic()
    accepted, reason, after, checks = engine.process_incremental_message(
        "Finance here. The printing bill came in at Rs 15,000, not Rs 10,000.",
        sender="Finance", mode="offline",
    )
    assert accepted, reason
    assert reason is None
    assert after.budget.total_projected == before.budget.total_projected + 5000
    printing = [item for item in after.budget.line_items if "printing" in item.item.lower()]
    assert len(printing) == 1
    assert printing[0].amount == 15000
    for area in ("venue", "schedule", "food", "judging"):
        assert getattr(after, area).model_dump() == getattr(before, area).model_dump()
    assert checks.all_passed
    assert time.monotonic() - started < 60


def test_incremental_catering_wrong_message_preserves_entire_valid_plan(engine, sample_pack):
    before, _ = engine.run_full_pipeline(sample_pack, mode="offline")
    snapshot = copy.deepcopy(before.model_dump())
    accepted, reason, after, checks = engine.process_incremental_message(
        "Caterer: I have rounded your order down to 100 boxes to keep the cost low.",
        sender="Caterer", mode="offline",
    )
    assert not accepted
    assert reason and "100" in reason
    assert after.model_dump() == snapshot
    assert checks.all_passed
    assert engine.rejected_records[-1].target_area == "food"
    assert "100" in engine.rejected_records[-1].raw_text


def test_unseen_pack_uses_changed_numbers_in_every_domain(engine, varied_pack):
    plan, checks = engine.run_full_pipeline(varied_pack, mode="offline")
    assert checks.all_passed, checks.model_dump()
    assert plan.judging.teams_count == 24
    assert plan.budget.cap == 400000
    assert plan.judging.minutes_per_team == 12
    assert plan.judging.honorarium_per_judge == 3000
    assert plan.schedule.total_duration_hours == 5
    assert plan.schedule.prayer_break_minutes == 20
    assert sum(item.duration_mins for item in plan.schedule.timeline) == 300
    assert plan.food.unit_cost in (600, 900)
    assert plan.venue.selected_room in ("Hall East", "Hall West")
    assert plan.food.headcount >= 96 + 8 + 8


def test_assignments_cover_every_team_once_within_judge_workload(engine, sample_pack):
    plan, _ = engine.run_full_pipeline(sample_pack, mode="offline")
    assignments = plan.judging.assignments
    assert len(assignments) == 50
    assert len({assignment["team_id"] for assignment in assignments}) == 50
    from collections import Counter
    workload = Counter(assignment["judge_id"] for assignment in assignments)
    assert len(workload) == 17
    assert max(workload.values()) <= 3
    assert not plan.judging.unassigned_teams
    for assignment in assignments:
        assert assignment["generated"] is True
        assert assignment["end_minute"] - assignment["start_minute"] == 15


def test_authorized_student_count_update_recomputes_derived_teams_and_meals(engine, sample_pack):
    engine.run_full_pipeline(sample_pack, mode="offline")
    accepted, reason, plan, checks = engine.process_incremental_message(
        "The approved student count is now 180 students in teams of 3.",
        sender="Dean's office", mode="offline",
    )
    assert accepted, reason
    assert checks.all_passed
    assert plan.judging.teams_count == 60
    assert plan.judging.selected_judges == 20
    assert plan.food.headcount == 210
    assert plan.venue.capacity >= 210


def test_explicit_full_judge_attendance_and_payment_override_generated_minimum(engine, sample_pack):
    text = sample_pack + """
# Message 9
From: Judging coordinator (email)
Date: 18 Nov
Message: All confirmed judges will attend the event. Pay all confirmed judges their honoraria.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert checks.all_passed, checks.model_dump()
    assert plan.judging.confirmed_judges == 20
    assert plan.food.headcount == 180
    assert plan.judging.total_honoraria == 100000


def test_latest_catering_quote_wins_even_when_old_quote_follows(engine, sample_pack):
    import re
    blocks = [b for b in re.split(r"(?=# Message \d+)", sample_pack) if b.strip()]
    assert len(blocks) == 8
    blocks[2], blocks[3] = blocks[3], blocks[2]
    plan, checks = engine.run_full_pipeline("\n".join(blocks), mode="offline")
    assert checks.all_passed
    assert plan.food.unit_cost in (800, 1200)
    assert plan.food.unit_cost != 1000


def test_infeasible_budget_cannot_overwrite_existing_valid_plan(engine, sample_pack):
    before, _ = engine.run_full_pipeline(sample_pack, mode="offline")
    snapshot = copy.deepcopy(before.model_dump())
    accepted, reason, after, checks = engine.process_incremental_message(
        "Finance here. The printing bill came in at Rs 900,000, not Rs 10,000.",
        sender="Finance", mode="offline",
    )
    assert not accepted
    assert reason
    assert after.model_dump() == snapshot
    assert checks.all_passed


def test_trace_tag_and_provider_reported_token_counts():
    tracer = ExecutionTracer()
    entry = tracer.record_call(
        model_name="test-provider-model", area_tag="venue",
        input_text="Exact input", output_text="Exact output",
        prompt_tokens=25, completion_tokens=15, total_tokens=40,
    )
    assert entry.call_number == 1
    assert entry.area_tag in {"reading", "venue", "schedule", "food", "judging", "budget"}
    assert entry.total_tokens == 40
    assert tracer.get_log().overall_total_tokens == 40


def test_trace_does_not_truncate_exact_inputs_or_outputs(capsys):
    tracer = ExecutionTracer()
    prompt = "input-start " + "x" * 500 + " input-END"
    output = "output-start " + "y" * 500 + " output-END"
    tracer.record_call(model_name="test-provider-model", area_tag="reading",
                       input_text=prompt, output_text=output,
                       prompt_tokens=200, completion_tokens=200)
    tracer.print_trace()
    printed = capsys.readouterr().out
    assert prompt in printed
    assert output in printed


def test_trace_unavailable_tokens_are_never_estimated():
    tracer = ExecutionTracer()
    entry = tracer.record_call(model_name="test-provider-model", area_tag="reading",
                              input_text="input", output_text="output",
                              prompt_tokens=None, completion_tokens=None)
    assert entry.prompt_tokens is None
    assert entry.completion_tokens is None
    assert entry.total_tokens is None


def test_database_persistence_survives_fresh_engine_instance(tmp_path, sample_pack):
    db = str(tmp_path / "plans.sqlite3")
    first = PlanningEngine(database_path=db)
    before, _ = first.run_full_pipeline(sample_pack, mode="offline")
    first.process_incremental_message(
        "Finance here. Printing is now Rs 15,000.", sender="Finance", mode="offline",
    )
    first.process_incremental_message(
        "Caterer: reduce to 100 boxes", sender="Caterer", mode="offline",
    )
    expected = copy.deepcopy(first.active_plan.model_dump())
    second = PlanningEngine(database_path=db)
    assert second.active_plan.model_dump() == expected
    assert second.active_plan.budget.total_projected == before.budget.total_projected + 5000
    assert second.rejected_records
    assert second.checks.all_passed
