"""Planner arithmetic and feasibility must respond to input, never sample constants."""
from backend.app.engine.areas.budget import evaluate_budget
from backend.app.engine.areas.venue import evaluate_venue


def test_venue_evaluation_uses_supplied_capacity_price_and_power():
    facts = {"headcount": 115, "backup_power_required": True, "venues": [
        {"name": "Small", "capacity": 90, "cost": 12000, "generator": True, "facilities": []},
        {"name": "Cheap", "capacity": 150, "cost": 25000, "generator": False, "facilities": []},
        {"name": "Resilient", "capacity": 130, "cost": 35000, "generator": True, "facilities": []},
    ]}
    plan = evaluate_venue(facts)
    assert plan.selected_room == "Resilient"
    assert plan.cost == 35000
    assert plan.capacity >= 115
    assert plan.generator_standby


def test_generator_is_not_an_invented_requirement():
    facts = {"headcount": 80, "backup_power_required": False, "venues": [
        {"name": "Ordinary", "capacity": 90, "cost": 10000, "generator": False, "facilities": []},
        {"name": "Powered", "capacity": 100, "cost": 20000, "generator": True, "facilities": []},
    ]}
    plan = evaluate_venue(facts)
    assert plan.selected_room == "Ordinary"


def test_budget_decimal_arithmetic_is_exact():
    facts = {"budget_cap": 1000, "expenses": {"printing": 12.35, "internet": 20.05}}
    plan = evaluate_budget(facts, venue_cost=100.10, food_cost=200.20, judging_cost=300.30)
    assert str(plan.total_projected) in ("633.0", "633", "633.00")
    assert str(plan.surplus_deficit) in ("367.0", "367", "367.00")


def test_judge_allocation_never_exceeds_team_cap(engine, varied_pack):
    plan, checks = engine.run_full_pipeline(varied_pack, mode="offline")
    assert checks.enough_judges
    assert plan.judging.teams_per_judge <= 3
    assert plan.judging.duration_minutes >= plan.judging.minutes_per_team


def test_food_and_budget_line_items_add_up(engine, varied_pack):
    plan, _ = engine.run_full_pipeline(varied_pack, mode="offline")
    assert plan.food.total_cost >= plan.food.headcount * plan.food.unit_cost
    included = [item.amount for item in plan.budget.line_items if item.status != "REJECTED"]
    assert sum(included) == plan.budget.total_projected
    assert plan.budget.cap - plan.budget.total_projected == plan.budget.surplus_deficit
