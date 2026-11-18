from typing import Dict, Any, List
from backend.app.schemas.plan import BudgetPlan, BudgetLineItem

def evaluate_budget(facts: Dict[str, Any], venue_cost: float, food_cost: float, judging_cost: float) -> BudgetPlan:
    budget_cap = facts.get("budget_cap", 650000.0)
    prizes = facts.get("committed_prizes", 100000.0)
    internet = facts.get("committed_internet", 20000.0)
    printing = facts.get("committed_printing", 10000.0)
    
    total_committed = prizes + internet + printing
    total_variable = venue_cost + food_cost + judging_cost
    total_projected = total_committed + total_variable
    surplus_deficit = budget_cap - total_projected
    
    line_items = [
        BudgetLineItem(category="Prizes", item="Winner & Runner-up awards", amount=prizes, status="COMMITTED"),
        BudgetLineItem(category="Infrastructure", item="Dedicated backup internet link", amount=internet, status="COMMITTED"),
        BudgetLineItem(category="Materials", item="Badges, certificates, directional signs", amount=printing, status="COMMITTED"),
        BudgetLineItem(category="Venue", item="Hall B rental with standby generator", amount=venue_cost, status="VARIABLE"),
        BudgetLineItem(category="Catering", item="Standard lunch box x 180 headcount", amount=food_cost, status="VARIABLE"),
        BudgetLineItem(category="Judging", item="Judge honoraria (20 judges x Rs 5,000)", amount=judging_cost, status="VARIABLE"),
    ]
    
    return BudgetPlan(
        cap=budget_cap,
        total_committed=total_committed,
        total_variable=total_variable,
        total_projected=total_projected,
        surplus_deficit=surplus_deficit,
        line_items=line_items
    )
