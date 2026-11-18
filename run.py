# -*- coding: utf-8 -*-
"""
HackPlan AI — Single Command CLI Runner for Mind to Machine Hackathon
Usage:
    python run.py [message_pack.txt]
"""
import sys
import os
import time

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.engine.pipeline import global_engine
from backend.app.engine.tracer import global_tracer

def print_banner():
    print("=" * 72)
    print(" HACKPLAN AI - MIND TO MACHINE HACKATHON SINGLE-COMMAND RUNNER")
    print(" Neuro-Symbolic Agentic Event Planner (Islamabad physical event)")
    print("=" * 72)

def main():
    start_time = time.time()
    pack_file = sys.argv[1] if len(sys.argv) > 1 else 'sample_pack.txt'
    
    print_banner()
    print(f">> Ingesting Message Pack: {pack_file}")
    
    if not os.path.exists(pack_file):
        print(f"[ERROR] Specified message pack file does not exist: {pack_file}")
        sys.exit(1)
        
    with open(pack_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print(">> Executing Neural Reading & Symbolic Invariant Verification Pipeline...")
    plan, checks = global_engine.run_full_pipeline(raw_text)
    
    # 1. Print Official Execution Trace
    global_tracer.print_trace()
    
    # 2. Print 6 Quality Checks
    print("=" * 72)
    print(" 6 CORE QUALITY CHECKS (COMPETITION INVARIANT GATE)")
    print("=" * 72)
    print(f" [1] Figures Sound:       {'[PASS]' if checks.figures_valid else '[FAIL]'} - {checks.details.figures_note}")
    print(f" [2] Within Budget:       {'[PASS]' if checks.budget_valid else '[FAIL]'} - Spent Rs {checks.details.budget_spend:,.0f} / Cap Rs {checks.details.budget_cap:,.0f}")
    print(f" [3] Venue Fits:          {'[PASS]' if checks.venue_fits else '[FAIL]'} - Capacity {checks.details.venue_capacity} seats (Required: {checks.details.headcount_required}) | Standby Gen: {checks.details.venue_generator}")
    print(f" [4] Schedule Valid:      {'[PASS]' if checks.schedule_valid else '[FAIL]'} - Duration {checks.details.schedule_duration_mins} mins (4 hrs) | Prayer Break: {checks.details.prayer_break_mins} mins")
    print(f" [5] Enough Judges:       {'[PASS]' if checks.enough_judges else '[FAIL]'} - {checks.details.judges_confirmed} confirmed judges (Ratio: {checks.details.teams_per_judge:.1f} teams/judge <= 3.0 cap)")
    print(f" [6] All Areas Covered:   {'[PASS]' if checks.all_areas_covered else '[FAIL]'} - {', '.join(checks.details.areas_present)}")
    print("-" * 72)
    print(f" OVERALL COMPLIANCE STATUS: {'[ALL PASS - 100%]' if checks.all_passed else '[FAILURES DETECTED]'}")
    print("=" * 72)

    # 3. Print 5 Operational Plan Areas
    print("\n" + "=" * 72)
    print(" FINAL OPERATIONAL EVENT PLAN (5 AREAS)")
    print("=" * 72)
    print(f"VENUE:    {plan.venue.selected_room} ({plan.venue.capacity} seats, Rs {plan.venue.cost:,.0f}) | Generator: {plan.venue.generator_standby}")
    print(f"          Rationale: {plan.venue.rationale}")
    print(f"SCHEDULE: {plan.schedule.total_duration_hours:.1f} Hours (240 mins) | Prayer Break: {plan.schedule.prayer_break_minutes} mins")
    for item in plan.schedule.timeline:
        print(f"          * {item.time_slot} ({item.duration_mins}m): {item.activity}")
    print(f"FOOD:     {plan.food.caterer_tier} x {plan.food.headcount} attendees @ Rs {plan.food.unit_cost:,.0f}/head = Rs {plan.food.total_cost:,.0f}")
    print(f"          Delivery: {plan.food.delivery_terms}")
    print(f"JUDGING:  {plan.judging.confirmed_judges} Judges x Rs {plan.judging.honorarium_per_judge:,.0f} = Rs {plan.judging.total_honoraria:,.0f}")
    print(f"          {plan.judging.teams_count} Teams | {plan.judging.teams_per_judge} Teams/Judge (Max 3) | {plan.judging.minutes_per_team}m/team ({plan.judging.duration_minutes}m block)")
    print(f"BUDGET:   Projected Spend: Rs {plan.budget.total_projected:,.0f} / Cap: Rs {plan.budget.cap:,.0f} | Surplus: Rs {plan.budget.surplus_deficit:,.0f}")
    print("=" * 72)

    elapsed = time.time() - start_time
    print(f">> Total Execution Elapsed Time: {elapsed:.2f} seconds (Limit: 120s)")
    print(">> Pipeline Run Complete.\n")

if __name__ == '__main__':
    main()
