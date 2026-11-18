"""Validated public planning records. Defaults describe an empty workspace."""
from datetime import datetime, timezone
from typing import Any, Literal
from pydantic import BaseModel, Field

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

class VenuePlan(BaseModel):
    selected_room: str = ""
    capacity: int = 0
    cost: float = 0
    generator_standby: bool = False
    rationale: str = "No message pack processed."
    required_seating: int = 0
    facilities: list[str] = Field(default_factory=list)
    options: list[dict[str, Any]] = Field(default_factory=list)
    valid: bool = False
    issues: list[str] = Field(default_factory=list)

class TimelineItem(BaseModel):
    time_slot: str
    activity: str
    duration_mins: int
    start_minute: int = 0
    end_minute: int = 0
    source: str = "Generated allocation"

class SchedulePlan(BaseModel):
    total_duration_hours: float = 0
    prayer_break_minutes: int = 0
    timeline: list[TimelineItem] = Field(default_factory=list)
    valid: bool = False
    conflicts: list[str] = Field(default_factory=list)

class FoodPlan(BaseModel):
    caterer_tier: str = ""
    unit_cost: float = 0
    headcount: int = 0
    total_cost: float = 0
    delivery_terms: str = "Unspecified"
    delivery_cost: float = 0
    attendee_categories: dict[str, int] = Field(default_factory=dict)
    options: list[dict[str, Any]] = Field(default_factory=list)
    valid: bool = False
    issues: list[str] = Field(default_factory=list)

class JudgingPlan(BaseModel):
    confirmed_judges: int = 0
    selected_judges: int = 0
    honorarium_per_judge: float = 0
    total_honoraria: float = 0
    teams_count: int = 0
    teams_per_judge: float = 0
    minutes_per_team: int = 0
    max_teams_per_judge: int = 0
    duration_minutes: int = 0
    assignments: list[dict[str, Any]] = Field(default_factory=list)
    unassigned_teams: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    availability: list[dict[str, Any]] = Field(default_factory=list)
    identifiers_generated: bool = True
    valid: bool = False

class BudgetLineItem(BaseModel):
    category: str
    item: str
    amount: float
    status: Literal["COMMITTED", "VARIABLE", "REJECTED"]

class BudgetPlan(BaseModel):
    cap: float = 0
    total_committed: float = 0
    total_variable: float = 0
    total_projected: float = 0
    surplus_deficit: float = 0
    line_items: list[BudgetLineItem] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    valid: bool = False

class RejectedMessageRecord(BaseModel):
    message_index: int | None = None
    sender: str
    raw_text: str
    target_area: str
    attempted_action: str
    rejection_reason: str
    violated_constraints: list[str] = Field(default_factory=list)
    source_reference: str | None = None
    timestamp: str = Field(default_factory=now)

class OperationalPlan(BaseModel):
    status: Literal["EMPTY", "VALID", "INVALID", "MUTATED", "REJECTED_ROLLBACK"] = "EMPTY"
    last_updated: str = Field(default_factory=now)
    event: dict[str, Any] = Field(default_factory=dict)
    venue: VenuePlan = Field(default_factory=VenuePlan)
    schedule: SchedulePlan = Field(default_factory=SchedulePlan)
    food: FoodPlan = Field(default_factory=FoodPlan)
    judging: JudgingPlan = Field(default_factory=JudgingPlan)
    budget: BudgetPlan = Field(default_factory=BudgetPlan)
    raw_messages_count: int = 0
    version: int = 0
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    unresolved_constraints: list[str] = Field(default_factory=list)
    affected_areas: list[str] = Field(default_factory=list)
    extraction_mode: str = "not_run"

