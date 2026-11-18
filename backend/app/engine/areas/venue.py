from typing import Any
from backend.app.schemas.plan import VenuePlan

def evaluate_venue(facts: dict[str, Any]) -> VenuePlan:
    required = facts.get("headcount", 0)
    options, eligible = [], []
    for original in facts.get("venues", []):
        option = dict(original)
        issues = []
        if option["capacity"] < required:
            issues.append(f"Capacity {option['capacity']} below required {required}.")
        if facts.get("backup_power_required") and not option.get("generator"):
            issues.append("A required standby generator is unavailable.")
        missing = set(facts.get("required_facilities", [])) - set(option.get("facilities", []))
        if missing:
            issues.append("Missing facilities: " + ", ".join(sorted(missing)))
        if facts.get("selected_venue") and option["name"].lower() != facts["selected_venue"].lower():
            issues.append("Does not match the requested venue.")
        option.update(eligible=not issues, validation_errors=issues)
        options.append(option)
        if not issues:
            eligible.append(option)
    if not eligible:
        return VenuePlan(required_seating=required, options=options, issues=["No source venue satisfies seating and facility constraints."])
    selected = min(eligible, key=lambda item: (item["cost"], item["capacity"]))
    return VenuePlan(selected_room=selected["name"], capacity=selected["capacity"], cost=selected["cost"],
                     generator_standby=selected.get("generator", False), facilities=selected.get("facilities", []),
                     required_seating=required, options=options, valid=required > 0,
                     rationale=f"Lowest quoted cost among feasible venues: {selected['capacity']} seats for {required} attendees. Generator availability is enforced only when a source requires it.")

