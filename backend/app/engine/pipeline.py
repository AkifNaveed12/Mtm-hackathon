"""Finite LangGraph extraction -> facts -> deterministic planners -> validation -> persistence."""
import copy
import os
import re
import threading
import time
from pathlib import Path
from typing import Any, TypedDict
from langgraph.graph import StateGraph, START, END
from backend.app.schemas.plan import OperationalPlan, RejectedMessageRecord, now
from backend.app.schemas.checks import CoreChecks
from backend.app.engine.tracer import ExecutionTracer, global_tracer
from backend.app.engine.ingestor import extract_facts
from backend.app.engine.constraints import normalize_facts, check_constraints
from backend.app.engine.store import PlanningStore
from backend.app.engine.areas.venue import evaluate_venue
from backend.app.engine.areas.schedule import evaluate_schedule
from backend.app.engine.areas.food import evaluate_food
from backend.app.engine.areas.judging import evaluate_judging
from backend.app.engine.areas.budget import evaluate_budget
from backend.app.engine.verifier import verify_plan

ALL_AREAS = ["venue", "schedule", "food", "judging", "budget"]
FIELD_AREAS = {
    "students": ALL_AREAS, "staff": ["venue", "food", "budget"], "team_size": ALL_AREAS,
    "teams_count": ALL_AREAS, "judges_confirmed": ALL_AREAS, "max_teams_per_judge": ALL_AREAS,
    "minutes_per_team": ["judging", "schedule"], "honorarium_per_judge": ["judging", "budget"],
    "venues": ["venue", "budget"], "selected_venue": ["venue", "budget"],
    "backup_power_required": ["venue", "budget"], "required_facilities": ["venue", "budget"],
    "catering_options": ["food", "budget"], "meal_quantity": ["food", "budget"],
    "budget_cap": ["budget"], "expenses": ["budget"], "total_duration_hours": ["schedule"],
    "prayer_break_mins": ["schedule"], "required_activities": ["schedule"],
    "judge_availability": ["judging", "schedule"], "start_time": ["schedule"],
    "constraints": ALL_AREAS, "attending_judges": ALL_AREAS, "pay_all_confirmed_judges": ["judging", "budget"],
}

class WorkflowState(TypedDict, total=False):
    raw_text: str
    mode: str
    facts: dict
    extraction_mode: str
    messages: list
    plan: OperationalPlan
    checks: CoreChecks

class PlanningEngine:
    def __init__(self, database_path: str = ":memory:", tracer: ExecutionTracer | None = None):
        self.store = PlanningStore(str(database_path))
        self.tracer = tracer or ExecutionTracer()
        self.lock = threading.RLock()
        self.active_plan = OperationalPlan()
        self.active_facts: dict[str, Any] = {}
        self.rejected_records: list[RejectedMessageRecord] = []
        self.messages: list[dict] = []
        self.checks = CoreChecks()
        self.last_execution: dict = {}
        self.workflow_status = "idle"
        persisted = self.store.load()
        if persisted:
            self.active_plan = OperationalPlan.model_validate(persisted["plan"])
            self.active_facts = persisted.get("facts", {})
            self.messages = persisted.get("messages", [])
            self.checks = CoreChecks.model_validate(persisted["checks"])
            self.rejected_records = [RejectedMessageRecord.model_validate(item) for item in persisted.get("rejected_messages", [])]
            self.tracer.restore(persisted.get("trace", {}))
            self.last_execution = persisted.get("last_execution", {})
        graph = StateGraph(WorkflowState)
        graph.add_node("understand_messages", self._extract_node)
        graph.add_node("resolve_facts", self._normalize_node)
        graph.add_node("plan_affected_domains", self._plan_node)
        graph.add_node("validate_complete_plan", self._validate_node)
        graph.add_edge(START, "understand_messages")
        graph.add_edge("understand_messages", "resolve_facts")
        graph.add_edge("resolve_facts", "plan_affected_domains")
        graph.add_edge("plan_affected_domains", "validate_complete_plan")
        graph.add_edge("validate_complete_plan", END)
        self.workflow = graph.compile()

    def _extract_node(self, state):
        facts, extraction_mode, messages = extract_facts(state["raw_text"], state["mode"], self.tracer)
        return {"facts": facts, "extraction_mode": extraction_mode, "messages": messages}

    def _normalize_node(self, state):
        return {"facts": normalize_facts(state["facts"])}

    def _plan_node(self, state):
        return {"plan": self._plan(state["facts"], ALL_AREAS, state["extraction_mode"])}

    def _validate_node(self, state):
        return {"checks": verify_plan(state["plan"])}

    def _plan(self, facts: dict, areas: list[str], extraction_mode: str, previous=None):
        judging = evaluate_judging(facts) if "judging" in areas or not previous else previous.judging.model_copy(deep=True)
        facts["judging_duration_minutes"] = judging.duration_minutes
        venue = evaluate_venue(facts) if "venue" in areas or not previous else previous.venue.model_copy(deep=True)
        food = evaluate_food(facts) if "food" in areas or not previous else previous.food.model_copy(deep=True)
        schedule = evaluate_schedule(facts) if "schedule" in areas or not previous else previous.schedule.model_copy(deep=True)
        budget = evaluate_budget(facts, venue.cost, food.total_cost, judging.total_honoraria) if "budget" in areas or not previous else previous.budget.model_copy(deep=True)
        plan = OperationalPlan(status="VALID", event={"name": facts["event_name"], "date": facts["event_date"],
                    "location": facts["location"], "students": facts["students"], "staff": facts["staff"],
                    "team_size": facts["team_size"], "required_headcount": facts["headcount"],
                    "paid_judges": facts["judges_confirmed"] if facts.get("pay_all_confirmed_judges") else judging.selected_judges,
                    "judge_attendance_policy": "Minimum workload-feasible judge selection from the confirmed pool; generated planning decision, not a source attendance count."},
                    venue=venue, schedule=schedule, food=food, judging=judging, budget=budget,
                    raw_messages_count=len(facts.get("raw_messages", [])), constraints=facts["constraints"],
                    unresolved_constraints=list(facts["unresolved_constraints"]), affected_areas=areas,
                    extraction_mode=extraction_mode)
        plan.unresolved_constraints.extend(check_constraints(plan, facts))
        if not verify_plan(plan).all_passed:
            plan.status = "INVALID"
        return plan

    def snapshot(self):
        return {"plan": self.active_plan.model_dump(), "checks": self.checks.model_dump(),
                "facts": self.active_facts, "messages": self.messages,
                "trace": self.tracer.get_log().model_dump(),
                "rejected_messages": [record.model_dump() for record in self.rejected_records],
                "last_execution": self.last_execution}

    def _persist(self, summary, areas, version=False):
        self.active_plan.version = self.store.save(self.snapshot(), summary, areas, version=version, execution=self.last_execution)

    def run_full_pipeline(self, raw_text: str, mode: str | None = None):
        if not raw_text.strip():
            raise ValueError("The message pack is empty.")
        if len(raw_text.encode("utf-8")) > 200000:
            raise ValueError("Message pack exceeds the 200 KB limit.")
        with self.lock:
            start = time.perf_counter()
            self.workflow_status = "running"
            # Preserve complete historical trace across runs; no invisible reset of actual calls.
            call_start = len(self.tracer.entries)
            self.tracer.event("workflow_start", "Full planning workflow started.", affected_areas=ALL_AREAS)
            try:
                state = self.workflow.invoke({"raw_text": raw_text, "mode": mode or os.getenv("PLANNER_MODE", "auto")},
                                             {"recursion_limit": 12})
                candidate, checks = state["plan"], state["checks"]
                if checks.all_passed or self.active_plan.status == "EMPTY":
                    self.active_plan, self.active_facts = candidate, state["facts"]
                    self.checks = checks
                    self.messages = state["messages"]
                    for message in self.messages:
                        message["status"] = "processed" if checks.all_passed else "needs_review"
                else:
                    self.tracer.event("rejection", "New pack does not satisfy all constraints; previous valid plan preserved.")
                elapsed = time.perf_counter() - start
                self.last_execution = {"kind": "initial", "duration_seconds": elapsed, "model_calls": len(self.tracer.entries) - call_start,
                                       "affected_areas": ALL_AREAS, "mode": state["extraction_mode"],
                                       "status": "completed" if checks.all_passed else "invalid", "timestamp": now()}
                self.tracer.event("workflow_end", f"Full workflow ended in {elapsed:.3f}s; valid={checks.all_passed}.")
                self._persist("Imported message pack" if checks.all_passed else "Invalid pack requires review", ALL_AREAS, version=checks.all_passed)
                return self.active_plan, self.checks
            except Exception:
                self.tracer.event("workflow_error", "Planning failed; previous plan preserved.")
                self.last_execution = {"kind": "initial", "duration_seconds": time.perf_counter() - start,
                                       "model_calls": len(self.tracer.entries) - call_start, "status": "error", "timestamp": now()}
                self._persist("Failed planning execution", [])
                raise
            finally:
                self.workflow_status = "idle"

    @staticmethod
    def predict_areas(message: str):
        lower = message.lower()
        if re.search(r"print|invoice|finance|budget|prize|expense|internet", lower):
            return ["budget"]
        if re.search(r"food|meal|box|cater|lunch", lower):
            return ["food", "budget"]
        if re.search(r"venue|hall|room|generator|seating", lower):
            return ["venue", "budget"]
        if re.search(r"judge|judging|team|student", lower):
            return ALL_AREAS
        if re.search(r"schedule|prayer|break|duration|hour|late", lower):
            return ["schedule"]
        return ["reading"]

    def _reject(self, text, sender, reason, areas, start, call_start):
        record = RejectedMessageRecord(message_index=len(self.messages) + 1, sender=sender,
                 raw_text=text, target_area=areas[0] if areas else "reading", attempted_action="Plan update",
                 rejection_reason=reason, violated_constraints=[reason], source_reference=f"message-{len(self.messages) + 1}")
        self.rejected_records.append(record)
        self.messages.append({"index": len(self.messages) + 1, "sender": sender, "date": now(), "source": "Organizer submission",
                              "text": text, "raw": text, "status": "rejected", "rejection_reason": reason})
        self.tracer.event("rejection", reason, affected_areas=areas)
        self.last_execution = {"kind": "update", "status": "rejected", "duration_seconds": time.perf_counter() - start,
                               "model_calls": len(self.tracer.entries) - call_start, "affected_areas": areas, "timestamp": now()}
        self._persist("Rejected message", areas)
        return False, reason, self.active_plan, self.checks

    def process_incremental_message(self, message_text: str, sender: str = "External", mode: str | None = None):
        with self.lock:
            if self.active_plan.status == "EMPTY":
                raise ValueError("Import an initial message pack before submitting updates.")
            start, call_start = time.perf_counter(), len(self.tracer.entries)
            areas = self.predict_areas(message_text)
            if not message_text.strip():
                return self._reject(message_text, sender, "An empty message cannot update a plan.", areas, start, call_start)
            if len(message_text.encode("utf-8")) > 20000:
                raise ValueError("Update exceeds the 20 KB limit.")
            if re.search(r"ignore (?:all |previous )?instructions|environment variables|delete database|system prompt|api[_ ]?key", message_text, re.I):
                return self._reject(message_text, sender, "Untrusted instructions attempting to alter system behavior are not event facts.", areas, start, call_start)
            extraction_mode = mode or os.getenv("PLANNER_MODE", "auto")
            try:
                patch, used_mode, _ = extract_facts(f"From: {sender}\nMessage: {message_text}", extraction_mode, self.tracer,
                                                   area_tag=areas[0], update=True)
            except Exception:
                self.last_execution = {"kind": "update", "status": "error", "duration_seconds": time.perf_counter() - start,
                                       "model_calls": len(self.tracer.entries) - call_start, "affected_areas": areas, "timestamp": now()}
                self.tracer.event("workflow_error", "Update extraction failed; active plan preserved.")
                self._persist("Failed update execution", areas)
                raise
            relevant = {key: value for key, value in patch.items() if key in FIELD_AREAS and value not in (None, [], {})}
            if not relevant:
                return self._reject(message_text, sender, "No supported authorized change was extracted; existing plan preserved for review.", areas, start, call_start)
            # Organizer supplied sender labels are assertions, not cryptographic identity; API access is separately protected.
            identity = (sender + " " + message_text[:80]).lower()
            financial = {"budget_cap", "expenses"} & relevant.keys()
            if financial and not re.search(r"finance|dean|director|principal|organizer|admin|treasurer", identity):
                return self._reject(message_text, sender, "Financial changes require an authorized finance or event approval source.", ["budget"], start, call_start)
            institutional = {"students", "staff", "team_size", "teams_count", "budget_cap", "total_duration_hours", "prayer_break_mins"} & relevant.keys()
            if institutional and not re.search(r"dean|director|principal|organizer|admin", identity):
                return self._reject(message_text, sender, "This update conflicts with an institutional rule; the sender has no authority to replace it.", areas, start, call_start)
            candidate_facts = copy.deepcopy(self.active_facts)
            changes = []
            for key, value in relevant.items():
                if key == "expenses":
                    old_expenses = candidate_facts.get(key, {})
                    normalized_expenses = {}
                    for label, amount in value.items():
                        label = re.sub(r"^(?:the_|an?_)|_(?:bill|invoice|cost|expense)$", "", label.lower().replace(" ", "_"))
                        canonical = next((existing for existing in old_expenses if existing == label or existing in label or label in existing), label)
                        normalized_expenses[canonical] = amount
                    merged = {**old_expenses, **normalized_expenses}
                elif key == "constraints":
                    merged = candidate_facts.get(key, []) + value
                elif key == "judge_availability":
                    merged = candidate_facts.get(key, []) + value
                elif key in ("catering_options", "venues"):
                    merged_options = {item["name"].lower(): item for item in candidate_facts.get(key, [])}
                    merged_options.update({item["name"].lower(): item for item in value})
                    merged = list(merged_options.values())
                else:
                    merged = value
                if merged != candidate_facts.get(key):
                    candidate_facts[key] = merged
                    if key == "teams_count":
                        candidate_facts["_teams_derived"] = False
                    changes.append(key)
            areas = [area for area in ALL_AREAS if any(area in FIELD_AREAS.get(key, []) for key in changes)]
            if not changes:
                return self._reject(message_text, sender, "Duplicate or unchanged facts; no new plan version created.", areas, start, call_start)
            # Source index references from the update are mapped into the current message sequence.
            new_index = len(self.messages) + 1
            candidate_facts["source_facts"].extend({**item, "source_message": new_index} for item in patch.get("source_facts", []))
            candidate_facts["unresolved_constraints"].extend(patch.get("unresolved_constraints", []))
            message = {"index": new_index, "sender": sender, "date": now(), "source": "Organizer submission",
                       "text": message_text, "raw": message_text, "status": "accepted"}
            candidate_facts["raw_messages"] = self.messages + [message]
            candidate_facts = normalize_facts(candidate_facts)
            candidate = self._plan(candidate_facts, areas, used_mode, self.active_plan)
            checks = verify_plan(candidate)
            if not checks.all_passed:
                issues = candidate.food.issues + candidate.venue.issues + candidate.schedule.conflicts + candidate.judging.conflicts + candidate.budget.warnings + candidate.unresolved_constraints
                reason = "; ".join(issues) or "Update fails one or more plan validity checks."
                return self._reject(message_text, sender, reason, areas, start, call_start)
            candidate.status = "MUTATED"
            self.active_plan, self.active_facts, self.checks = candidate, candidate_facts, checks
            self.messages.append(message)
            elapsed = time.perf_counter() - start
            self.last_execution = {"kind": "update", "status": "accepted", "duration_seconds": elapsed,
                                   "model_calls": len(self.tracer.entries) - call_start, "affected_areas": areas,
                                   "changed_facts": changes, "mode": used_mode, "timestamp": now()}
            self.tracer.event("accepted", "Accepted update; recalculated " + ", ".join(areas) + ".", changed_facts=changes)
            self._persist("Updated " + ", ".join(changes), areas, version=True)
            return True, None, self.active_plan, self.checks


DEFAULT_DB = str(Path(__file__).resolve().parents[2] / "data" / "planner.sqlite3")
global_engine = PlanningEngine(os.getenv("PLANNER_DB_PATH", DEFAULT_DB), tracer=global_tracer)

