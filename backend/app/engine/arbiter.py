"""Compatibility facade; all mutations use PlanningEngine's transactional validator."""
def evaluate_message_mutation(plan, active_facts, message_text, sender="External"):
    from backend.app.engine.pipeline import PlanningEngine
    engine = PlanningEngine()
    engine.active_plan, engine.active_facts = plan.model_copy(deep=True), dict(active_facts)
    from backend.app.engine.verifier import verify_plan
    engine.checks = verify_plan(engine.active_plan)
    accepted, reason, candidate, _ = engine.process_incremental_message(message_text, sender)
    areas = engine.last_execution.get("affected_areas", ["reading"])
    if accepted:
        active_facts.update(engine.active_facts)
    return accepted, areas[0] if areas else "reading", reason, candidate
