from backend.app.schemas.plan import OperationalPlan
from backend.app.schemas.checks import CoreChecks, CheckDetails

def verify_plan(plan: OperationalPlan) -> CoreChecks:
    # 1. Figures Valid Check
    food_math = abs(plan.food.unit_cost * plan.food.headcount - plan.food.total_cost) < 0.01
    judging_math = abs(plan.judging.confirmed_judges * plan.judging.honorarium_per_judge - plan.judging.total_honoraria) < 0.01
    budget_math = abs((plan.budget.total_committed + plan.budget.total_variable) - plan.budget.total_projected) < 0.01
    surplus_math = abs((plan.budget.cap - plan.budget.total_projected) - plan.budget.surplus_deficit) < 0.01
    figures_valid = food_math and judging_math and budget_math and surplus_math
    
    # 2. Budget Valid Check
    budget_valid = plan.budget.total_projected <= plan.budget.cap
    
    # 3. Venue Fits Check
    required_headcount = 180  # 150 students + 10 staff + 20 judges
    venue_fits = plan.venue.capacity >= required_headcount
    
    # 4. Schedule Valid Check
    schedule_duration_mins = int(plan.schedule.total_duration_hours * 60)
    schedule_valid = (schedule_duration_mins == 240) and (plan.schedule.prayer_break_minutes >= 15)
    
    # 5. Enough Judges Check
    # 50 teams / max 3 teams per judge = 16.67 => need at least 17 judges
    min_judges_needed = int(plan.judging.teams_count / 3.0) + (1 if plan.judging.teams_count % 3 != 0 else 0)
    enough_judges = plan.judging.confirmed_judges >= min_judges_needed and plan.judging.teams_per_judge <= 3.0
    
    # 6. All Areas Covered Check
    areas_present = ["venue", "schedule", "food", "judging", "budget"]
    all_areas_covered = (
        bool(plan.venue.selected_room) and
        bool(plan.schedule.timeline) and
        bool(plan.food.caterer_tier) and
        (plan.judging.confirmed_judges > 0) and
        (plan.budget.total_projected > 0)
    )
    
    all_passed = (
        figures_valid and
        budget_valid and
        venue_fits and
        schedule_valid and
        enough_judges and
        all_areas_covered
    )
    
    figures_note = "All arithmetic equations and rate totals verified." if figures_valid else "Arithmetic discrepancy detected."
    
    details = CheckDetails(
        figures_note=figures_note,
        budget_spend=plan.budget.total_projected,
        budget_cap=plan.budget.cap,
        venue_capacity=plan.venue.capacity,
        venue_generator=plan.venue.generator_standby,
        headcount_required=required_headcount,
        schedule_duration_mins=schedule_duration_mins,
        prayer_break_mins=plan.schedule.prayer_break_minutes,
        judges_confirmed=plan.judging.confirmed_judges,
        teams_per_judge=plan.judging.teams_per_judge,
        areas_present=areas_present
    )
    
    return CoreChecks(
        figures_valid=figures_valid,
        budget_valid=budget_valid,
        venue_fits=venue_fits,
        schedule_valid=schedule_valid,
        enough_judges=enough_judges,
        all_areas_covered=all_areas_covered,
        all_passed=all_passed,
        details=details
    )
