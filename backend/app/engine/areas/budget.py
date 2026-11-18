from typing import Any
from backend.app.engine.money import total, decimal, money
from backend.app.schemas.plan import BudgetPlan, BudgetLineItem

def evaluate_budget(facts: dict[str, Any], venue_cost: float, food_cost: float, judging_cost: float) -> BudgetPlan:
    expenses = facts.get("expenses", {})
    if not expenses:
        expenses = {key.removeprefix("committed_"): value for key, value in facts.items() if key.startswith("committed_")}
    lines = [BudgetLineItem(category="Committed", item=label.replace("_", " ").title(), amount=amount,
                            status="COMMITTED") for label, amount in expenses.items()]
    lines.extend(BudgetLineItem(category=label, item=label, amount=amount, status="VARIABLE") for label, amount in
                 (("Venue", venue_cost), ("Catering", food_cost), ("Judge honoraria", judging_cost)))
    committed, variable = total(expenses.values()), total([venue_cost, food_cost, judging_cost])
    projected = total([committed, variable])
    cap = facts.get("budget_cap", 0)
    remaining = money(decimal(cap) - decimal(projected))
    warnings = []
    if remaining < 0:
        warnings.append(f"Planned expenses exceed the approved budget by Rs {-remaining:,.2f}.")
    if facts.get("proposals"):
        warnings.append(f"{len(facts['proposals'])} unapproved proposal(s) excluded from expenditure.")
    return BudgetPlan(cap=cap, total_committed=committed, total_variable=variable,
                      total_projected=projected, surplus_deficit=remaining, line_items=lines,
                      warnings=warnings, valid=cap > 0 and remaining >= 0)

