import pytest
from backend.app.engine.pipeline import PlanningEngine
from backend.app.engine.tracer import ExecutionTracer

def test_full_pipeline_sample_pack_compliance():
    with open("sample_pack.txt", "r", encoding="utf-8") as f:
        sample_text = f.read()

    engine = PlanningEngine()
    plan, checks = engine.run_full_pipeline(sample_text)

    # 6 checks verification
    assert checks.figures_valid is True
    assert checks.budget_valid is True
    assert checks.venue_fits is True
    assert checks.schedule_valid is True
    assert checks.enough_judges is True
    assert checks.all_areas_covered is True
    assert checks.all_passed is True

def test_incremental_printing_expense_update():
    """Practice message 1: Printing expense increases from Rs 10,000 to Rs 15,000"""
    with open("sample_pack.txt", "r", encoding="utf-8") as f:
        sample_text = f.read()

    engine = PlanningEngine()
    plan, checks = engine.run_full_pipeline(sample_text)
    initial_spend = plan.budget.total_projected

    # Submit incremental message
    printing_msg = "Printing invoice update: Printing expense is now Rs 15,000 instead of Rs 10,000."
    accepted, reason, updated_plan, updated_checks = engine.process_incremental_message(printing_msg, sender="Finance")

    assert accepted is True
    assert reason is None
    # Spend should increase by exactly Rs 5,000
    assert updated_plan.budget.total_projected == initial_spend + 5000.0
    assert updated_plan.budget.total_projected == 601000.0
    assert updated_plan.budget.total_projected <= 650000.0
    assert updated_checks.all_passed is True

def test_incremental_catering_sabotage_rejection():
    """Practice message 2: Catering proposes reducing 177 required meals to 100"""
    with open("sample_pack.txt", "r", encoding="utf-8") as f:
        sample_text = f.read()

    engine = PlanningEngine()
    plan, checks = engine.run_full_pipeline(sample_text)
    initial_headcount = plan.food.headcount
    initial_spend = plan.budget.total_projected

    # Submit sabotage message
    sabotage_msg = "Caterer WhatsApp: Can we supply only 100 lunch boxes instead of 180? Shortage of supplies."
    accepted, reason, preserved_plan, preserved_checks = engine.process_incremental_message(sabotage_msg, sender="Caterer")

    assert accepted is False
    assert reason is not None
    assert "insufficient" in reason.lower() or "180" in reason or "100" in reason
    # Active plan must remain preserved and valid
    assert preserved_plan.food.headcount == initial_headcount
    assert preserved_plan.budget.total_projected == initial_spend
    assert preserved_checks.all_passed is True
    assert len(engine.rejected_records) == 1
    assert engine.rejected_records[0].target_area == "food"

def test_trace_tag_and_token_constraints():
    tracer = ExecutionTracer()
    entry = tracer.record_call(
        model_name="qwen/qwen3.8-27b",
        area_tag="venue",
        input_text="Evaluate room options",
        output_text="Selected Hall B",
        prompt_tokens=25,
        completion_tokens=15
    )
    assert entry.call_number == 1
    assert entry.area_tag in ["reading", "venue", "schedule", "food", "judging", "budget"]
    assert entry.total_tokens == 40
    log = tracer.get_log()
    assert log.total_calls == 1
    assert log.overall_total_tokens == 40
