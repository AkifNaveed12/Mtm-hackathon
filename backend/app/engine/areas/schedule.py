from typing import Dict, Any, List
from backend.app.schemas.plan import SchedulePlan, TimelineItem

def evaluate_schedule(facts: Dict[str, Any]) -> SchedulePlan:
    prayer_break = facts.get("prayer_break_mins", 15)
    total_hours = facts.get("total_duration_hours", 4.0)
    
    # 4-hour breakdown (240 minutes)
    timeline = [
        TimelineItem(time_slot="00:00 - 00:30", activity="Check-in, Welcome Address & Problem Briefing", duration_mins=30),
        TimelineItem(time_slot="00:30 - 02:45", activity="Hackathon Build Sprint", duration_mins=135),
        TimelineItem(time_slot="02:45 - 03:00", activity="Mandatory Prayer & Refreshment Break", duration_mins=prayer_break),
        TimelineItem(time_slot="03:00 - 03:45", activity="Judging Session (20 Judges evaluating 50 teams)", duration_mins=45),
        TimelineItem(time_slot="03:45 - 04:00", activity="Results Tabulation & Closing Ceremony", duration_mins=15),
    ]
    
    return SchedulePlan(
        total_duration_hours=total_hours,
        prayer_break_minutes=prayer_break,
        timeline=timeline
    )
