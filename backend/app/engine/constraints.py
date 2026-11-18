import math
import operator
from backend.app.schemas.facts import EventFacts, Constraint

SUPPORTED = {"headcount", "budget_cap", "capacity", "generator", "facility", "prayer_break",
             "event_duration", "max_teams_per_judge", "judging_minutes", "meal_quantity", "required_activity"}
OPS = {">=": operator.ge, "<=": operator.le, "==": operator.eq, "=": operator.eq,
       ">": operator.gt, "<": operator.lt, "!=": operator.ne}

def normalize_facts(facts: dict) -> dict:
    raw, raw_text = facts.get("raw_messages", []), facts.get("raw_text", "")
    filtered = {key: value for key, value in facts.items() if key in EventFacts.model_fields}
    validated = EventFacts.model_validate(filtered)
    result = validated.model_dump()
    result["raw_messages"], result["raw_text"] = raw, raw_text
    derived_teams = facts.get("_teams_derived", not bool(result["teams_count"]))
    if derived_teams and result["team_size"]:
        result["teams_count"] = math.ceil(result["students"] / result["team_size"])
    result["_teams_derived"] = derived_teams
    limit = result["max_teams_per_judge"]
    selected = min(result["judges_confirmed"], math.ceil(result["teams_count"] / limit)) if limit else 0
    result["judges_attending"] = selected if result["attending_judges"] is None else result["attending_judges"]
    result["headcount"] = result["students"] + result["staff"] + result["judges_attending"]
    unresolved = list(result["unresolved_constraints"])
    if result["team_size"] and result["students"] % result["team_size"]:
        unresolved.append("Student count does not divide exactly into the required team size; permission for a partial team is unresolved.")
    if not derived_teams and result["team_size"] and result["teams_count"] * result["team_size"] != result["students"]:
        unresolved.append("Explicit team count and team size do not match the source student count.")
    for key in ("students", "team_size", "budget_cap", "total_duration_hours", "judges_confirmed", "max_teams_per_judge", "minutes_per_team"):
        if not result.get(key):
            unresolved.append("Missing required source fact: " + key)
    if not result["venues"]:
        unresolved.append("Missing source venue options.")
    if not result["catering_options"]:
        unresolved.append("Missing source catering quotes.")
    for rule in result["constraints"]:
        if rule["effective_status"] == "inactive":
            continue
        if rule["effective_status"] != "active":
            unresolved.append("Unknown constraint status for " + rule["identifier"] + ": " + rule["effective_status"])
            continue
        if rule["constraint_type"] not in SUPPORTED or (rule["operator"] not in OPS and rule["operator"] not in ("includes", "requires")):
            unresolved.append("Unsupported constraint " + rule["identifier"])
    result["unresolved_constraints"] = list(dict.fromkeys(unresolved))
    derived = [
        ("derived-headcount", "food", "headcount", ">=", result["headcount"], "people"),
        ("budget-ceiling", "budget", "budget_cap", "<=", result["budget_cap"], "rupees"),
        ("event-window", "schedule", "event_duration", "==", round(result["total_duration_hours"] * 60), "minutes"),
        ("prayer-break", "schedule", "prayer_break", ">=", result["prayer_break_mins"], "minutes"),
        ("judge-workload", "judging", "max_teams_per_judge", "<=", result["max_teams_per_judge"], "teams"),
    ]
    derived_ids = {item[0] for item in derived}
    result["constraints"] = [rule for rule in result["constraints"] if rule["identifier"] not in derived_ids]
    known = {rule["identifier"] for rule in result["constraints"]}
    for identifier, area, kind, op, value, unit in derived:
        if identifier not in known:
            result["constraints"].append(Constraint(identifier=identifier, area=area, constraint_type=kind,
                                                    operator=op, value=value, unit=unit,
                                                    source_message="derived from referenced source facts").model_dump())
    return result

def check_constraints(plan, facts):
    errors = []
    values = {"headcount": plan.food.headcount, "meal_quantity": plan.food.headcount,
              "budget_cap": plan.budget.total_projected, "capacity": plan.venue.capacity,
              "generator": plan.venue.generator_standby,
              "prayer_break": plan.schedule.prayer_break_minutes,
              "event_duration": sum(item.duration_mins for item in plan.schedule.timeline),
              "max_teams_per_judge": max((sum(a["judge_id"] == judge for a in plan.judging.assignments)
                                            for judge in {a["judge_id"] for a in plan.judging.assignments}), default=0),
              "judging_minutes": plan.judging.minutes_per_team}
    for rule in facts.get("constraints", []):
        rule = Constraint.model_validate(rule).model_dump()
        if rule.get("effective_status", "active") == "inactive":
            continue
        if rule["effective_status"] != "active":
            errors.append("Unknown constraint status for " + rule["identifier"] + ": " + rule["effective_status"])
            continue
        kind = rule["constraint_type"]
        conditions = rule.get("conditions", {})
        if conditions:
            errors.append("Constraint conditions need review: " + rule["identifier"])
            continue
        if kind == "facility":
            valid = str(rule["value"]).lower() in [item.lower() for item in plan.venue.facilities]
        elif kind == "required_activity":
            valid = any(str(rule["value"]).lower() in item.activity.lower() for item in plan.schedule.timeline)
        elif kind in values and rule["operator"] in OPS:
            try:
                actual = values[kind]
                unit, scope = rule.get("unit", "").lower(), rule.get("scope", "").lower()
                expected = rule["value"]
                if kind == "headcount":
                    if unit in ("students", "student"):
                        actual = facts.get("students", 0)
                    elif unit in ("staff", "volunteers"):
                        actual = facts.get("staff", 0)
                    elif unit in ("students_per_team", "people_per_team") or scope == "team":
                        actual = facts.get("team_size", 0)
                    elif unit in ("judges", "judge"):
                        actual = facts.get("judges_attending", 0)
                if kind in ("event_duration", "prayer_break", "judging_minutes") and unit in ("hours", "hour", "hrs", "hr"):
                    expected *= 60
                valid = OPS[rule["operator"]](actual, expected)
            except TypeError:
                valid = False
        else:
            errors.append("Unsupported constraint: " + rule["identifier"])
            continue
        if not valid:
            errors.append(f"Constraint {rule['identifier']} violated ({kind} {rule['operator']} {rule['value']}).")
    return errors
