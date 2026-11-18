import math
from typing import Any
from backend.app.engine.money import money, decimal
from backend.app.schemas.plan import JudgingPlan

def evaluate_judging(facts: dict[str, Any]) -> JudgingPlan:
    confirmed = facts.get("judges_confirmed", 0)
    teams = facts.get("teams_count", 0)
    limit = facts.get("max_teams_per_judge", 0)
    judges = facts.get("judges_attending", min(confirmed, math.ceil(teams / limit)) if limit else 0)
    minutes = facts.get("minutes_per_team", 0)
    honorarium = facts.get("honorarium_per_judge", 0)
    assignments, unassigned = [], []
    for index in range(teams):
        identifier = f"T{index + 1:03d}"
        if not judges or not limit or index // judges >= limit:
            unassigned.append(identifier)
            continue
        slot = index // judges
        assignments.append({"team_id": identifier, "judge_id": f"J{index % judges + 1:03d}",
                            "slot": slot + 1, "start_minute": slot * minutes,
                            "end_minute": (slot + 1) * minutes, "generated": True})
    duration = math.ceil(teams / judges) * minutes if judges else 0
    conflicts = []
    if judges > confirmed:
        conflicts.append("Required attending judges exceed the confirmed pool.")
    if unassigned:
        conflicts.append(f"{len(unassigned)} teams exceed confirmed judging capacity.")
    if not minutes:
        conflicts.append("Per-team judging duration is missing.")
    return JudgingPlan(confirmed_judges=confirmed, selected_judges=judges,
                       honorarium_per_judge=honorarium, total_honoraria=money(decimal(honorarium) * (confirmed if facts.get("pay_all_confirmed_judges") else judges)),
                       teams_count=teams, teams_per_judge=teams / judges if judges else 0,
                       max_teams_per_judge=limit, minutes_per_team=minutes, duration_minutes=duration,
                       assignments=assignments, unassigned_teams=unassigned, conflicts=conflicts,
                       availability=facts.get("judge_availability", []),
                       valid=bool(teams and judges and minutes and limit and not unassigned and not conflicts))

