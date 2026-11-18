"""Actual provider requests are model calls; deterministic steps are events."""
from backend.app.schemas.plan import now
from backend.app.schemas.trace import TraceEntry, TraceLog, AreaTag
class ExecutionTracer:
    def __init__(self):
        self.entries: list[TraceEntry] = []
        self.events: list[dict] = []
    def reset(self):
        self.entries.clear()
        self.events.clear()
    def event(self, kind: str, detail: str, **metadata):
        self.events.append({"timestamp": now(), "kind": kind, "detail": detail, **metadata})
    def record_call(self, model_name: str, area_tag: AreaTag, input_text: str,
                    output_text: str, prompt_tokens: int | None = None,
                    completion_tokens: int | None = None, total_tokens: int | None = None,
                    duration_ms: float = 0, status: str = "success", error: str | None = None,
                    retry: int = 0) -> TraceEntry:
        entry = TraceEntry(call_number=len(self.entries) + 1, model_name=model_name,
                           area_tag=area_tag, input=input_text, output=output_text,
                           prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
                           total_tokens=total_tokens, duration_ms=duration_ms,
                           status=status, error=error, retry=retry, timestamp=now())
        self.entries.append(entry)
        return entry
    def get_log(self) -> TraceLog:
        return TraceLog(entries=list(self.entries), total_calls=len(self.entries),
                        total_prompt_tokens=sum(e.prompt_tokens or 0 for e in self.entries),
                        total_completion_tokens=sum(e.completion_tokens or 0 for e in self.entries),
                        overall_total_tokens=sum(e.total_tokens or 0 for e in self.entries),
                        usage_complete=all(e.total_tokens is not None and e.prompt_tokens is not None and e.completion_tokens is not None for e in self.entries),
                        events=list(self.events))
    def restore(self, value: dict):
        log = TraceLog.model_validate(value)
        self.entries, self.events = log.entries, log.events
    def print_trace(self):
        print("\n" + "=" * 72 + "\nMODEL CALL TRACE")
        for e in self.entries:
            print(f"Call #{e.call_number} | Model: {e.model_name} | Area: [{e.area_tag}] | {e.status}")
            print(f"Input: {e.input}\nOutput: {e.output}")
            print(f"Provider tokens: input={e.prompt_tokens}, output={e.completion_tokens}, total={e.total_tokens}")
            print(f"Duration: {e.duration_ms:.1f} ms; error: {e.error or 'none'}")
        for event in self.events:
            print(f"[{event['kind']}] {event['detail']}")
        log = self.get_log()
        print(f"TOTAL CALLS: {log.total_calls} | TOTAL REPORTED TOKENS: {log.overall_total_tokens}")
        if not log.usage_complete:
            print("Some token usage unavailable; total includes reported usage only.")
        print("=" * 72)
global_tracer = ExecutionTracer()

