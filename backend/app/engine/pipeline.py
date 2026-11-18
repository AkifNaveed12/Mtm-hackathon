from typing import Dict, Any, Tuple, List, Optional
from backend.app.schemas.plan import OperationalPlan, RejectedMessageRecord
from backend.app.schemas.checks import CoreChecks
from backend.app.engine.tracer import global_tracer
from backend.app.engine.llm import call_model
from backend.app.engine.ingestor import ingest_and_extract_facts
from backend.app.engine.areas.venue import evaluate_venue
from backend.app.engine.areas.schedule import evaluate_schedule
from backend.app.engine.areas.food import evaluate_food
from backend.app.engine.areas.judging import evaluate_judging
from backend.app.engine.areas.budget import evaluate_budget
from backend.app.engine.verifier import verify_plan
from backend.app.engine.arbiter import evaluate_message_mutation

class PlanningEngine:
    def __init__(self):
        self.active_plan: OperationalPlan = OperationalPlan()
        self.active_facts: Dict[str, Any] = {}
        self.rejected_records: List[RejectedMessageRecord] = []
        self.checks: CoreChecks = CoreChecks()

    def run_full_pipeline(self, raw_text: str) -> Tuple[OperationalPlan, CoreChecks]:
        # Reset trace for new full run
        global_tracer.reset()
        self.rejected_records.clear()

        # Step 1: Universal Message Ingestor ('reading')
        self.active_facts, msg_count = ingest_and_extract_facts(raw_text)

        # Step 2: Venue Specialist ('venue')
        call_model("venue", "Evaluate venue options against 180 headcount and standby power requirement.")
        venue_plan = evaluate_venue(self.active_facts)

        # Step 3: Schedule Specialist ('schedule')
        call_model("schedule", "Structure 4-hour timeline with required 15-minute prayer break.")
        schedule_plan = evaluate_schedule(self.active_facts)

        # Step 4: Food Specialist ('food')
        call_model("food", "Compute catering plan for 180 headcount using latest valid quote from 12 Nov.")
        food_plan = evaluate_food(self.active_facts)

        # Step 5: Judging Specialist ('judging')
        call_model("judging", "Calculate judge-to-team allocation: 20 confirmed judges evaluating 50 teams.")
        judging_plan = evaluate_judging(self.active_facts)

        # Step 6: Budget Specialist ('budget')
        call_model("budget", f"Synthesize total projected budget vs Rs {self.active_facts['budget_cap']:,.0f} limit.")
        budget_plan = evaluate_budget(
            self.active_facts,
            venue_cost=venue_plan.cost,
            food_cost=food_plan.total_cost,
            judging_cost=judging_plan.total_honoraria
        )

        # Assemble full plan
        self.active_plan = OperationalPlan(
            status="VALID",
            venue=venue_plan,
            schedule=schedule_plan,
            food=food_plan,
            judging=judging_plan,
            budget=budget_plan,
            raw_messages_count=msg_count
        )

        # Step 7: 6-Point Invariant Gate
        self.checks = verify_plan(self.active_plan)
        return self.active_plan, self.checks

    def process_incremental_message(self, message_text: str, sender: str = "External") -> Tuple[bool, Optional[str], OperationalPlan, CoreChecks]:
        accepted, area_tag, reason, mutated_plan = evaluate_message_mutation(
            self.active_plan,
            self.active_facts,
            message_text,
            sender
        )

        if accepted and mutated_plan:
            self.active_plan = mutated_plan
            self.checks = verify_plan(self.active_plan)
            return True, None, self.active_plan, self.checks
        else:
            record = RejectedMessageRecord(
                message_index=len(self.rejected_records) + 1,
                sender=sender,
                raw_text=message_text,
                target_area=str(area_tag),
                attempted_action="Plan mutation",
                rejection_reason=reason or "Rule conflict detected"
            )
            self.rejected_records.append(record)
            # Active plan remains preserved and valid
            self.checks = verify_plan(self.active_plan)
            return False, reason, self.active_plan, self.checks

global_engine = PlanningEngine()
