from typing import Optional, List
from pydantic import BaseModel, Field

class CheckDetails(BaseModel):
    figures_note: Optional[str] = None
    budget_spend: float = 0.0
    budget_cap: float = 0.0
    venue_capacity: int = 0
    venue_generator: bool = False
    headcount_required: int = 0
    schedule_duration_mins: int = 0
    prayer_break_mins: int = 0
    judges_confirmed: int = 0
    teams_per_judge: float = 0
    areas_present: List[str] = Field(default_factory=list)

class CoreChecks(BaseModel):
    figures_valid: bool = Field(False, description="All arithmetic, rates, and quotes internally sound")
    budget_valid: bool = Field(False, description="Total spend <= budget cap")
    venue_fits: bool = Field(False, description="Venue capacity >= total headcount and power resilient")
    schedule_valid: bool = Field(False, description="Schedule equals 4 hours with required breaks")
    enough_judges: bool = Field(False, description="Judge capacity meets judging ratio constraints")
    all_areas_covered: bool = Field(False, description="All 5 required planning areas covered")
    all_passed: bool = Field(False, description="All six criteria satisfy rules")
    details: CheckDetails = Field(default_factory=CheckDetails)
