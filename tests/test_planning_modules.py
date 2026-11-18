import pytest
from backend.app.engine.areas.venue import evaluate_venue, VENUE_OPTIONS
from backend.app.engine.areas.schedule import evaluate_schedule
from backend.app.engine.areas.food import evaluate_food
from backend.app.engine.areas.judging import evaluate_judging
from backend.app.engine.areas.budget import evaluate_budget

def test_venue_evaluation_capacity_and_generator():
    facts = {"headcount": 180, "backup_power_required": True}
    plan = evaluate_venue(facts)
    assert plan.selected_room == "Hall B"
    assert plan.capacity == 200
    assert plan.cost == 150000.0
    assert plan.generator_standby is True
    assert plan.capacity >= 180

def test_venue_evaluation_rejects_insufficient_capacity():
    # Room D has 80 seats, headcount is 180
    assert VENUE_OPTIONS["Room D"]["capacity"] < 180

def test_schedule_evaluation_duration_and_prayer_break():
    facts = {"total_duration_hours": 4.0, "prayer_break_mins": 15}
    plan = evaluate_schedule(facts)
    assert plan.total_duration_hours == 4.0
    assert plan.prayer_break_minutes == 15
    total_slot_mins = sum(t.duration_mins for t in plan.timeline)
    assert total_slot_mins == 240
    # Verify prayer break is included
    assert any("Prayer" in t.activity for t in plan.timeline)

def test_food_evaluation_correct_math():
    facts = {"headcount": 180, "caterer_rate": 1200.0, "caterer_tier": "Standard lunch box"}
    plan = evaluate_food(facts)
    assert plan.headcount == 180
    assert plan.unit_cost == 1200.0
    assert plan.total_cost == 180 * 1200.0
    assert plan.total_cost == 216000.0

def test_judging_evaluation_ratio_and_time():
    facts = {
        "judges_confirmed": 20,
        "honorarium_per_judge": 5000.0,
        "teams_count": 50,
        "minutes_per_team": 15
    }
    plan = evaluate_judging(facts)
    assert plan.confirmed_judges == 20
    assert plan.total_honoraria == 100000.0
    assert plan.teams_per_judge == 2.5
    assert plan.teams_per_judge <= 3.0  # Max constraint
    assert plan.duration_minutes <= 45

def test_budget_evaluation_cap_and_balance():
    facts = {
        "budget_cap": 650000.0,
        "committed_prizes": 100000.0,
        "committed_internet": 20000.0,
        "committed_printing": 10000.0
    }
    plan = evaluate_budget(facts, venue_cost=150000.0, food_cost=216000.0, judging_cost=100000.0)
    assert plan.cap == 650000.0
    assert plan.total_committed == 130000.0
    assert plan.total_variable == 466000.0
    assert plan.total_projected == 596000.0
    assert plan.surplus_deficit == 54000.0
    assert plan.total_projected <= plan.cap
