"""Malformed external facts must be rejected before planners see them."""
import pytest
from pydantic import ValidationError

from backend.app.schemas.facts import EventFacts


@pytest.mark.parametrize("payload", [
    {"students": -1},
    {"students": 100001},
    {"venues": [{"name": "Bad", "capacity": -1, "cost": 20}]},
    {"catering_options": [{"name": "Bad", "unit_cost": -20}]},
    {"expenses": {"printing": -100}},
    {"expenses": {"printing": float("nan")}},
    {"required_activities": [{"duration_mins": 10}]},
    {"required_activities": [{"name": "Break", "duration_mins": -10}]},
    {"start_time": "unparseable"},
    {"start_time": "27:99"},
    {"arbitrary_injected_tool": "execute_shell"},
])
def test_fact_schema_rejects_unsafe_model_output(payload):
    with pytest.raises(ValidationError):
        EventFacts.model_validate(payload)
