"""Structured extraction boundary: unknown rules remain explicit, never disappear."""
from typing import Any, Literal
import math
import re
from pydantic import BaseModel, Field, ConfigDict, field_validator

class VenueOption(BaseModel):
    name: str
    capacity: int = Field(ge=0, le=100000)
    cost: float = Field(ge=0, le=1e12)
    generator: bool = False
    facilities: list[str] = Field(default_factory=list)
    source_message: int | None = None

class CateringOption(BaseModel):
    name: str
    unit_cost: float = Field(ge=0, le=1e9)
    delivery_cost: float = Field(default=0, ge=0, le=1e9)
    source_message: int | None = None

class Constraint(BaseModel):
    identifier: str
    source_message: int | str | None = None
    area: Literal["venue", "schedule", "food", "judging", "budget", "reading"]
    constraint_type: str
    operator: str = ">="
    value: Any = None
    unit: str = ""
    scope: str = "event"
    conditions: dict[str, Any] = Field(default_factory=dict)
    authority: str = "source"
    effective_status: str = "active"

    @field_validator("conditions", mode="before")
    @classmethod
    def empty_conditions(cls, value):
        return {} if value is None or value == [] else value

    @field_validator("operator", mode="before")
    @classmethod
    def canonical_operator(cls, value):
        text = str(value).strip().lower()
        return {"eq": "==", "equals": "==", "equal": "==", "le": "<=", "lte": "<=",
                "less_than_or_equal": "<=", "ge": ">=", "gte": ">=", "greater_than_or_equal": ">=",
                "lt": "<", "gt": ">", "ne": "!=", "neq": "!="}.get(text, text)

    @field_validator("effective_status", mode="before")
    @classmethod
    def canonical_status(cls, value):
        text = str(value).strip().lower()
        if text in {"active", "approved", "effective", "current", "enforced", "mandatory", "accepted", "valid"}:
            return "active"
        if text in {"inactive", "superseded", "rejected", "request", "pending", "proposal", "proposed", "expired"}:
            return "inactive"
        return text

class EventFacts(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    event_name: str = "Physical hackathon"
    event_date: str | None = None
    location: str | None = None
    students: int = Field(default=0, ge=0, le=100000)
    staff: int = Field(default=0, ge=0, le=100000)
    team_size: int = Field(default=0, ge=0, le=10000)
    teams_count: int = Field(default=0, ge=0, le=10000)
    budget_cap: float = Field(default=0, ge=0, le=1e12)
    total_duration_hours: float = Field(default=0, ge=0, le=168)
    prayer_break_mins: int = Field(default=0, ge=0, le=1440)
    backup_power_required: bool = False
    required_facilities: list[str] = Field(default_factory=list)
    judges_confirmed: int = Field(default=0, ge=0, le=10000)
    attending_judges: int | None = Field(default=None, ge=0, le=10000)
    pay_all_confirmed_judges: bool = False
    max_teams_per_judge: int = Field(default=0, ge=0, le=10000)
    minutes_per_team: int = Field(default=0, ge=0, le=1440)
    honorarium_per_judge: float = Field(default=0, ge=0, le=1e9)
    venues: list[VenueOption] = Field(default_factory=list)
    catering_options: list[CateringOption] = Field(default_factory=list)
    expenses: dict[str, float] = Field(default_factory=dict)
    constraints: list[Constraint] = Field(default_factory=list)
    unresolved_constraints: list[str] = Field(default_factory=list)
    judge_availability: list[dict[str, Any]] = Field(default_factory=list)
    required_activities: list[dict[str, Any]] = Field(default_factory=list)
    source_facts: list[dict[str, Any]] = Field(default_factory=list)
    proposals: list[dict[str, Any]] = Field(default_factory=list)
    meal_quantity: int | None = Field(default=None, ge=0, le=100000)
    selected_venue: str | None = None
    start_time: str | None = None

    @field_validator("expenses")
    @classmethod
    def validate_expenses(cls, expenses):
        if any(not name.strip() or not math.isfinite(value) or value < 0 or value > 1e12 for name, value in expenses.items()):
            raise ValueError("Expenses require a name and finite nonnegative amount.")
        return expenses

    @field_validator("required_activities")
    @classmethod
    def validate_activities(cls, activities):
        for activity in activities:
            duration = activity.get("duration_mins")
            if not isinstance(activity.get("name"), str) or not activity["name"].strip() or not isinstance(duration, int) or duration < 0 or duration > 10080:
                raise ValueError("Activities require a name and nonnegative duration in minutes.")
        return activities

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value):
        if value is not None and not re.fullmatch(r"(?:[01]?\d|2[0-3]):[0-5]\d", value):
            raise ValueError("Start time must be a valid 24-hour HH:MM time.")
        return value

