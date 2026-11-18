from typing import Any
from backend.app.schemas.plan import SchedulePlan, TimelineItem

def evaluate_schedule(facts: dict[str, Any]) -> SchedulePlan:
    total = round(facts.get("total_duration_hours", 0) * 60)
    prayer = facts.get("prayer_break_mins", 0)
    judging = facts.get("judging_duration_minutes", 0)
    # These are generated allocations, not claimed source facts; required durations override them.
    opening, closing = min(15, total // 12), min(15, total // 12)
    activities = list(facts.get("required_activities", []))
    filtered = []
    for activity in activities:
        if activity["name"].lower() == "opening":
            opening = activity["duration_mins"]
        elif activity["name"].lower() == "closing":
            closing = activity["duration_mins"]
        else:
            filtered.append(activity)
    activities = filtered
    additional = sum(item.get("duration_mins", 0) for item in activities)
    build = total - opening - closing - prayer - judging - additional
    conflicts = []
    if build <= 0:
        conflicts.append("Required activities and judging do not fit within the available event duration.")
    slots = [("Opening and briefing", opening), ("Build sprint", max(0, build))]
    if prayer:
        slots.append(("Prayer break", prayer))
    slots.extend((item["name"], item.get("duration_mins", 0)) for item in activities)
    slots.extend([("Judging", judging), ("Results and closing", closing)])
    start = 0
    clock_start = 0
    if facts.get("start_time"):
        hour, minute = map(int, facts["start_time"].split(":"))
        clock_start = hour * 60 + minute
    def clock(minute):
        minute = (minute + clock_start) % (24 * 60)
        return f"{minute // 60:02d}:{minute % 60:02d}"
    timeline = []
    for activity, duration in slots:
        if duration:
            timeline.append(TimelineItem(activity=activity, duration_mins=duration,
                                         start_minute=start, end_minute=start + duration,
                                         time_slot=f"{clock(start)} - {clock(start + duration)}"))
            start += duration
    judging_start = next((item.start_minute for item in timeline if item.activity == "Judging"), 0)
    unavailable = 0
    for notice in facts.get("judge_availability", []):
        delay = notice.get("delay_minutes")
        if not isinstance(delay, (int, float)) or delay < 0:
            conflicts.append("Judge availability contains an unsupported arrival restriction.")
            continue
        if delay > judging_start:
            count = notice.get("count", 1)
            note = notice.get("note", "")
            import re
            if notice.get("all_judges") or re.search(r"all\s+(?:the\s+)?(?:\d+\s+)?(?:confirmed\s+)?judges", note, re.I):
                count = facts.get("judges_confirmed", 0)
            if not isinstance(count, int) or count < 1:
                conflicts.append("Judge availability has an unsupported judge count.")
            else:
                unavailable += count
    selected = facts.get("judges_attending", 0)
    if facts.get("judges_confirmed", 0) - unavailable < selected:
        conflicts.append("Too few confirmed judges are available by the judging start time.")
    return SchedulePlan(total_duration_hours=facts.get("total_duration_hours", 0), prayer_break_minutes=prayer,
                        timeline=timeline, conflicts=conflicts, valid=bool(total and build > 0 and start == total and not conflicts))

