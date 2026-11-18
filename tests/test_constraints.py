"""New source rules must change decisions or remain visibly unresolved."""


def test_unseen_generator_requirement_changes_venue_decision(engine, varied_pack):
    text = varied_pack + """
# Message 6
From: Director (email)
Date: 18 Nov
Message: A standby generator is mandatory for the venue.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert checks.all_passed, checks.model_dump()
    assert plan.venue.selected_room == "Hall West"
    assert plan.venue.generator_standby


def test_unrecognized_logical_constraint_is_never_silently_ignored(engine, varied_pack):
    text = varied_pack + """
# Message 6
From: Director (email)
Date: 18 Nov
Message: Teams may enter only if each team brings a signed robotics safety certificate.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert plan.unresolved_constraints
    assert not checks.all_passed
    assert "certificate" in " ".join(plan.unresolved_constraints).lower()


def test_required_extra_break_fits_in_complete_timeline(engine, varied_pack):
    text = varied_pack + """
# Message 6
From: Director (email)
Date: 18 Nov
Message: Include a 25-minute mandatory lunch break.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert checks.all_passed
    lunch = [item for item in plan.schedule.timeline if "lunch" in item.activity.lower()]
    assert len(lunch) == 1
    assert lunch[0].duration_mins == 25
    assert sum(item.duration_mins for item in plan.schedule.timeline) == 300


def test_oversized_required_break_reports_schedule_infeasibility(engine, varied_pack):
    text = varied_pack + """
# Message 6
From: Director (email)
Date: 18 Nov
Message: Include a 300-minute mandatory lunch break.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert not checks.schedule_valid
    assert not checks.all_passed
    assert plan.schedule.conflicts


def test_known_rule_does_not_hide_unknown_rule_in_same_message(engine, varied_pack):
    text = varied_pack + """
# Message 6
From: Director (email)
Date: 18 Nov
Message: Keep a 20-minute prayer break. Catering must be nut-free.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert not checks.all_passed
    assert any("nut-free" in item.lower() for item in plan.unresolved_constraints)


def test_source_opening_duration_replaces_generated_opening(engine, varied_pack):
    text = varied_pack + """
# Message 6
From: Director (email)
Date: 18 Nov
Message: Include a 25-minute mandatory opening.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert checks.all_passed
    opening = [item for item in plan.schedule.timeline if "opening" in item.activity.lower()]
    assert len(opening) == 1
    assert opening[0].duration_mins == 25
    assert sum(item.duration_mins for item in plan.schedule.timeline) == 300


def test_all_judges_arriving_after_their_block_is_infeasible(engine, varied_pack):
    text = varied_pack + """
# Message 6
From: Judging coordinator (email)
Date: 18 Nov
Message: All 10 judges will be 295 minutes late on the day.
"""
    plan, checks = engine.run_full_pipeline(text, mode="offline")
    assert not checks.all_passed
    assert not checks.schedule_valid
    assert plan.schedule.conflicts


def test_approved_constraint_and_operator_aliases_are_enforced(engine, sample_pack):
    import copy
    from backend.app.engine.constraints import check_constraints, normalize_facts
    plan, _ = engine.run_full_pipeline(sample_pack, mode="offline")
    facts = copy.deepcopy(engine.active_facts)
    facts["constraints"].append({"identifier": "approved-capacity", "area": "venue",
                                 "constraint_type": "capacity", "operator": "ge",
                                 "value": 999, "effective_status": "approved"})
    normalized = normalize_facts(facts)
    assert any("approved-capacity" in issue for issue in check_constraints(plan, normalized))


def test_unknown_constraint_status_is_explicitly_unresolved(engine, sample_pack):
    import copy
    from backend.app.engine.constraints import normalize_facts
    engine.run_full_pipeline(sample_pack, mode="offline")
    facts = copy.deepcopy(engine.active_facts)
    facts["constraints"].append({"identifier": "ambiguous-rule", "area": "venue",
                                 "constraint_type": "capacity", "operator": ">=",
                                 "value": 999, "effective_status": "maybe-effective"})
    normalized = normalize_facts(facts)
    assert any("ambiguous-rule" in issue for issue in normalized["unresolved_constraints"])
