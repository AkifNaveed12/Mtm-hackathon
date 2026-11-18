"""Exercise actual provider adapter with a fake SDK boundary, not network calls."""
import json
from types import SimpleNamespace

import pytest

from backend.app.engine.llm import ModelFailure, call_model
from backend.app.engine.tracer import ExecutionTracer


def install_sdk(monkeypatch, response=None, error=None):
    import groq
    observed = {}
    class FakeGroq:
        def __init__(self, **kwargs):
            observed["client"] = kwargs
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def create(self, **kwargs):
            observed["request"] = kwargs
            if error is not None:
                raise error
            return response
    monkeypatch.setattr(groq, "Groq", FakeGroq)
    monkeypatch.setenv("GROQ_API_KEY", "dummy-test-key")
    monkeypatch.setenv("GROQ_MODEL", "requested-test-model")
    return observed


def result(usage):
    return SimpleNamespace(
        model="actual-provider-model-identifier",
        choices=[SimpleNamespace(message=SimpleNamespace(content='{"students":96}'))],
        usage=usage,
    )


def test_actual_provider_model_and_exact_request_are_traced(monkeypatch):
    observed = install_sdk(monkeypatch, result(SimpleNamespace(prompt_tokens=71, completion_tokens=9, total_tokens=80)))
    tracer = ExecutionTracer()
    output, input_tokens, output_tokens = call_model("reading", "Exact original input", tracer=tracer)
    entry = tracer.get_log().entries[0]
    assert entry.model_name == "actual-provider-model-identifier"
    assert entry.input == json.dumps({k: v for k, v in observed["request"].items() if k != "model"}, ensure_ascii=False)
    assert entry.output == output == '{"students":96}'
    assert (input_tokens, output_tokens, entry.total_tokens) == (71, 9, 80)
    assert observed["client"]["max_retries"] == 0
    assert observed["client"]["timeout"] <= 60
    assert "dummy-test-key" not in entry.input


def test_provider_missing_usage_remains_unavailable(monkeypatch):
    install_sdk(monkeypatch, result(None))
    tracer = ExecutionTracer()
    call_model("budget", "Printing update", tracer=tracer)
    entry = tracer.get_log().entries[0]
    assert entry.prompt_tokens is None
    assert entry.completion_tokens is None
    assert entry.total_tokens is None
    assert tracer.get_log().usage_complete is False


def test_provider_missing_total_is_not_invented_from_components(monkeypatch):
    install_sdk(monkeypatch, result(SimpleNamespace(prompt_tokens=71, completion_tokens=9)))
    tracer = ExecutionTracer()
    call_model("budget", "Printing update", tracer=tracer)
    entry = tracer.get_log().entries[0]
    assert entry.prompt_tokens == 71
    assert entry.completion_tokens == 9
    assert entry.total_tokens is None
    assert tracer.get_log().usage_complete is False


def test_provider_failure_is_traced_once_without_sensitive_error_body(monkeypatch):
    install_sdk(monkeypatch, error=RuntimeError("secret-value-must-never-appear"))
    tracer = ExecutionTracer()
    with pytest.raises(ModelFailure) as caught:
        call_model("food", "Original message", tracer=tracer)
    log = tracer.get_log()
    assert log.total_calls == 1
    assert log.entries[0].status == "error"
    assert log.entries[0].total_tokens is None
    assert "secret-value-must-never-appear" not in str(caught.value)
    assert "secret-value-must-never-appear" not in log.model_dump_json()


def test_unconfigured_provider_never_creates_a_fake_model_call(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "")
    tracer = ExecutionTracer()
    with pytest.raises(ModelFailure):
        call_model("reading", "Input", tracer=tracer)
    assert tracer.get_log().total_calls == 0


def test_model_cannot_invent_power_requirement_or_event_date_from_message_headers(sample_pack):
    from backend.app.engine.ingestor import parse_raw_message_pack, validate_source_support
    messages = parse_raw_message_pack(sample_pack)
    facts = {"backup_power_required": True, "event_date": "2026-11-09"}
    result = validate_source_support(facts, messages, ExecutionTracer())
    assert not result.get("backup_power_required")
    assert result.get("event_date") is None
