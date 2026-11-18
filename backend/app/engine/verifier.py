from backend.app.schemas.plan import OperationalPlan
from backend.app.schemas.checks import CoreChecks, CheckDetails
from backend.app.engine.money import decimal, total

def verify_plan(plan: OperationalPlan) -> CoreChecks:
    required = plan.event.get("required_headcount", plan.food.headcount)
    food_math = decimal(plan.food.unit_cost) * plan.food.headcount + decimal(plan.food.delivery_cost) == decimal(plan.food.total_cost)
    paid_judges = plan.event.get("paid_judges", plan.judging.selected_judges)
    judging_math = decimal(paid_judges * decimal(plan.judging.honorarium_per_judge)) == decimal(plan.judging.total_honoraria)
    budget_math = decimal(total([plan.budget.total_committed, plan.budget.total_variable])) == decimal(plan.budget.total_projected)
    lines_math = decimal(total(line.amount for line in plan.budget.line_items)) == decimal(plan.budget.total_projected)
    surplus_math = decimal(plan.budget.cap) - decimal(plan.budget.total_projected) == decimal(plan.budget.surplus_deficit)
    figures = bool(food_math and judging_math and budget_math and lines_math and surplus_math and plan.event.get("students", 0) > 0
                   and plan.food.headcount >= required and not plan.unresolved_constraints)
    schedule_mins = sum(item.duration_mins for item in plan.schedule.timeline)
    areas = [area for area in ("venue", "schedule", "food", "judging", "budget") if getattr(plan, area).valid]
    coverage = len(areas) == 5 and not plan.unresolved_constraints
    values = dict(figures_valid=figures, budget_valid=plan.budget.valid,
                  venue_fits=plan.venue.valid and plan.venue.capacity >= required,
                  schedule_valid=plan.schedule.valid and schedule_mins == round(plan.schedule.total_duration_hours * 60),
                  enough_judges=plan.judging.valid, all_areas_covered=coverage)
    note = "Currency arithmetic uses Decimal; counts and constraints verified."
    if plan.unresolved_constraints:
        note = "Unresolved: " + "; ".join(plan.unresolved_constraints)
    details = CheckDetails(figures_note=note, budget_spend=plan.budget.total_projected,
                           budget_cap=plan.budget.cap, venue_capacity=plan.venue.capacity,
                           venue_generator=plan.venue.generator_standby, headcount_required=required,
                           schedule_duration_mins=schedule_mins, prayer_break_mins=plan.schedule.prayer_break_minutes,
                           judges_confirmed=plan.judging.confirmed_judges,
                           teams_per_judge=plan.judging.teams_per_judge, areas_present=areas)
    return CoreChecks(**values, all_passed=all(values.values()), details=details)
