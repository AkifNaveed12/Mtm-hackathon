from typing import List, Optional
from backend.app.schemas.trace import TraceEntry, TraceLog, AreaTag

class ExecutionTracer:
    def __init__(self):
        self.entries: List[TraceEntry] = []
        self._call_counter: int = 0

    def reset(self):
        self.entries.clear()
        self._call_counter = 0

    def record_call(
        self,
        model_name: str,
        area_tag: AreaTag,
        input_text: str,
        output_text: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0
    ) -> TraceEntry:
        self._call_counter += 1
        total_tokens = prompt_tokens + completion_tokens
        entry = TraceEntry(
            call_number=self._call_counter,
            model_name=model_name,
            area_tag=area_tag,
            input=input_text,
            output=output_text,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )
        self.entries.append(entry)
        return entry

    def get_log(self) -> TraceLog:
        total_prompt = sum(e.prompt_tokens for e in self.entries)
        total_completion = sum(e.completion_tokens for e in self.entries)
        overall_total = sum(e.total_tokens for e in self.entries)
        return TraceLog(
            entries=list(self.entries),
            total_calls=len(self.entries),
            total_prompt_tokens=total_prompt,
            total_completion_tokens=total_completion,
            overall_total_tokens=overall_total
        )

    def print_trace(self):
        print("\n" + "="*70)
        print(" EXECUTION TRACE LOG (Numbered Chronological Model Calls)")
        print("="*70)
        for e in self.entries:
            print(f"Call #{e.call_number} | Model: {e.model_name} | Area: [{e.area_tag}]")
            print(f"Input: {e.input[:120]}..." if len(e.input) > 120 else f"Input: {e.input}")
            print(f"Output: {e.output[:120]}..." if len(e.output) > 120 else f"Output: {e.output}")
            print(f"Tokens: Prompt={e.prompt_tokens}, Completion={e.completion_tokens}, Total={e.total_tokens}")
            print("-" * 70)
        total_log = self.get_log()
        print(f"TOTAL CALLS: {total_log.total_calls} | OVERALL TOTAL TOKENS: {total_log.overall_total_tokens}")
        print("="*70 + "\n")

global_tracer = ExecutionTracer()
