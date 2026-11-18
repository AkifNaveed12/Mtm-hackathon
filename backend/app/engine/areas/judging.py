from typing import Dict, Any
from backend.app.schemas.plan import JudgingPlan

def evaluate_judging(facts: Dict[str, Any]) -> JudgingPlan:
    judges_confirmed = facts.get("judges_confirmed", 20)
    honorarium = facts.get("honorarium_per_judge", 5000.0)
    teams_count = facts.get("teams_count", 50)
    mins_per_team = facts.get("minutes_per_team", 15)
    
    # Each judge handles no more than 3 teams
    teams_per_judge = teams_count / judges_confirmed if judges_confirmed > 0 else 0
    total_honoraria = judges_confirmed * honorarium
    
    # With 20 judges and 50 teams, 10 judges evaluate 3 teams (45m) and 10 judges evaluate 2 teams (30m).
    # The judging window fits inside a 45-minute block.
    duration_minutes = int(min(3, teams_per_judge + 0.99)) * mins_per_team
    
    return JudgingPlan(
        confirmed_judges=judges_confirmed,
        honorarium_per_judge=honorarium,
        total_honoraria=total_honoraria,
        teams_count=teams_count,
        teams_per_judge=round(teams_per_judge, 2),
        minutes_per_team=mins_per_team,
        duration_minutes=duration_minutes
    )
