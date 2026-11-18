from typing import Any
from backend.app.engine.money import money, decimal
from backend.app.schemas.plan import FoodPlan

def evaluate_food(facts: dict[str, Any]) -> FoodPlan:
    required = facts.get("headcount", 0)
    quantity = facts.get("meal_quantity")
    headcount = required if quantity is None else quantity
    options = facts.get("catering_options", [])
    if not options and facts.get("caterer_rate") is not None:
        options = [{"name": facts.get("caterer_tier", "Quoted meal"), "unit_cost": facts["caterer_rate"], "delivery_cost": 0}]
    if not options:
        return FoodPlan(headcount=headcount, issues=["No catering quote was supplied."])
    selected = min(options, key=lambda option: decimal(option["unit_cost"]) * headcount + decimal(option.get("delivery_cost", 0)))
    delivery = selected.get("delivery_cost", 0)
    issues = []
    if headcount < required:
        issues.append(f"Proposed {headcount} meals is insufficient for {required} required attendees.")
    return FoodPlan(caterer_tier=selected["name"], unit_cost=selected["unit_cost"], headcount=headcount,
                    delivery_cost=delivery, total_cost=money(decimal(selected["unit_cost"]) * headcount + decimal(delivery)),
                    delivery_terms="Free delivery" if not delivery else f"Delivery Rs {delivery:,.2f}",
                    attendee_categories={"students": facts.get("students", 0), "staff": facts.get("staff", 0),
                                         "judges": facts.get("judges_attending", facts.get("judges_confirmed", 0))},
                    options=options, valid=required > 0 and headcount >= required, issues=issues)

