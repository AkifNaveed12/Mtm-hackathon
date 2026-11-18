from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class VenuePlan(BaseModel):
    selected_room: str = "Hall B"
    capacity: int = 200
    cost: float = 150000.0
    generator_standby: bool = True
    rationale: str = "Seats 200 (fits 180 required headcount: 150 students + 10 staff + 20 judges) with standby generator."

class TimelineItem(BaseModel):
    time_slot: str
    activity: str
    duration_mins: int

class SchedulePlan(BaseModel):
    total_duration_hours: float = 4.0
    prayer_break_minutes: int = 15
    timeline: List[TimelineItem] = Field(default_factory=list)

class FoodPlan(BaseModel):
    caterer_tier: str = "Standard lunch box"
    unit_cost: float = 1200.0
    headcount: int = 180
    total_cost: float = 216000.0
    delivery_terms: str = "Free delivery confirmed on 12 Nov"

class JudgingPlan(BaseModel):
    confirmed_judges: int = 20
    honorarium_per_judge: float = 5000.0
    total_honoraria: float = 100000.0
    teams_count: int = 50
    teams_per_judge: float = 2.5
    minutes_per_team: int = 15
    duration_minutes: int = 45

class BudgetLineItem(BaseModel):
    category: str
    item: str
    amount: float
    status: Literal["COMMITTED", "VARIABLE", "REJECTED"]

class BudgetPlan(BaseModel):
    cap: float = 650000.0
    total_committed: float = 130000.0
    total_variable: float = 466000.0
    total_projected: float = 596000.0
    surplus_deficit: float = 54000.0
    line_items: List[BudgetLineItem] = Field(default_factory=list)

class RejectedMessageRecord(BaseModel):
    message_index: Optional[int] = None
    sender: str
    raw_text: str
    target_area: str
    attempted_action: str
    rejection_reason: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class OperationalPlan(BaseModel):
    status: Literal["VALID", "MUTATED", "REJECTED_ROLLBACK"] = "VALID"
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    venue: VenuePlan = Field(default_factory=VenuePlan)
    schedule: SchedulePlan = Field(default_factory=SchedulePlan)
    food: FoodPlan = Field(default_factory=FoodPlan)
    judging: JudgingPlan = Field(default_factory=JudgingPlan)
    budget: BudgetPlan = Field(default_factory=BudgetPlan)
    raw_messages_count: int = 0
