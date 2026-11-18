from typing import Dict, Any, List
from backend.app.schemas.plan import VenuePlan

# Standard venue rooms described in messages
VENUE_OPTIONS = {
    "Room D": {"capacity": 80, "cost": 40000.0, "generator": False},
    "Hall A": {"capacity": 200, "cost": 120000.0, "generator": False},
    "Hall B": {"capacity": 200, "cost": 150000.0, "generator": True},
    "Hall C": {"capacity": 300, "cost": 220000.0, "generator": True},
}

def evaluate_venue(facts: Dict[str, Any]) -> VenuePlan:
    headcount = facts.get("headcount", 180)
    prefer_generator = facts.get("backup_power_required", True)
    
    # Check eligible rooms that fit headcount
    eligible = []
    for name, opt in VENUE_OPTIONS.items():
        if opt["capacity"] >= headcount:
            if prefer_generator:
                if opt["generator"]:
                    eligible.append((name, opt))
            else:
                eligible.append((name, opt))
                
    if not eligible:
        # Fallback to largest room
        name, opt = "Hall C", VENUE_OPTIONS["Hall C"]
    else:
        # Pick lowest cost among eligible
        eligible.sort(key=lambda x: x[1]["cost"])
        name, opt = eligible[0]
        
    rationale = (
        f"Selected {name} (seats {opt['capacity']} vs {headcount} required) "
        f"at Rs {opt['cost']:,.0f}. Standby generator: {opt['generator']} "
        f"(protects against Islamabad power cuts)."
    )
    
    return VenuePlan(
        selected_room=name,
        capacity=opt["capacity"],
        cost=opt["cost"],
        generator_standby=opt["generator"],
        rationale=rationale
    )
