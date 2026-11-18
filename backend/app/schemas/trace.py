from typing import Literal
from pydantic import BaseModel, Field
AreaTag = Literal["reading", "venue", "schedule", "food", "judging", "budget"]
class TraceEntry(BaseModel):
    call_number: int
    model_name: str
    area_tag: AreaTag
    input: str
    output: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    duration_ms: float = 0
    status: str = "success"
    error: str | None = None
    retry: int = 0
    timestamp: str = ""
class TraceLog(BaseModel):
    entries: list[TraceEntry] = Field(default_factory=list)
    total_calls: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    overall_total_tokens: int = 0
    usage_complete: bool = True
    events: list[dict] = Field(default_factory=list)

