from typing import Dict, Any
from backend.app.schemas.plan import FoodPlan

def evaluate_food(facts: Dict[str, Any]) -> FoodPlan:
    headcount = facts.get("headcount", 180)
    # The 12 Nov caterer message updated standard lunch box to Rs 1,200 per head with free delivery
    unit_cost = facts.get("caterer_rate", 1200.0)
    tier = facts.get("caterer_tier", "Standard lunch box")
    delivery = facts.get("caterer_delivery", "Free delivery confirmed on 12 Nov")
    
    total = headcount * unit_cost
    
    return FoodPlan(
        caterer_tier=tier,
        unit_cost=unit_cost,
        headcount=headcount,
        total_cost=total,
        delivery_terms=delivery
    )
