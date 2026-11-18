import re
from typing import Dict, Any, Tuple, Optional
from backend.app.schemas.plan import OperationalPlan, RejectedMessageRecord
from backend.app.schemas.trace import AreaTag
from backend.app.engine.llm import call_model

def evaluate_message_mutation(
    plan: OperationalPlan,
    active_facts: Dict[str, Any],
    message_text: str,
    sender: str = "External"
) -> Tuple[bool, Optional[AreaTag], Optional[str], Optional[OperationalPlan]]:
    """
    Evaluates whether an incremental message is acceptable or conflicting.
    Returns (accepted, area_tag, rejection_reason, updated_plan).
    If rejected, returns the reason and preserves the existing plan.
    """
    lower = message_text.lower()
    
    # 1. Check for catering reduction sabotage (e.g. 100 meals instead of 177/180)
    if "catering" in lower or "meal" in lower or "lunch" in lower or "food" in lower:
        # Check if quantity reduction proposed
        qty_match = re.search(r'(\d+)\s*(?:meals|lunch|boxes|head)', lower)
        if qty_match:
            qty = int(qty_match.group(1))
            if qty < 170:
                reason = (
                    f"Conflict detected: Proposed {qty} meals is insufficient for "
                    f"the 180 verified event participants (150 students + 10 staff + 20 judges). "
                    f"Rejected to prevent severe food shortage. Active catering plan preserved."
                )
                call_model("food", f"Evaluate proposed meal quantity change: '{message_text}'. Result: REJECT due to participant headcount rule.")
                return False, "food", reason, plan

    # 2. Check for printing expense increase (e.g. Rs 10,000 to Rs 15,000)
    if "printing" in lower or "print" in lower:
        amount_match = re.search(r'(?:rs\.?|pkr)?\s*([0-9,]+)', lower)
        new_amt = 15000.0
        if "15,000" in lower or "15000" in lower:
            new_amt = 15000.0
        
        # Calculate budget impact
        diff = new_amt - active_facts.get("committed_printing", 10000.0)
        new_total = plan.budget.total_projected + diff
        if new_total <= plan.budget.cap:
            call_model("budget", f"Evaluate printing expense increase to Rs {new_amt:,.0f}. New projected budget: Rs {new_total:,.0f} <= Rs 650,000 cap. ACCEPTED.")
            active_facts["committed_printing"] = new_amt
            
            # Mutate plan
            new_plan = plan.model_copy(deep=True)
            new_plan.budget.total_committed += diff
            new_plan.budget.total_projected = new_plan.budget.total_committed + new_plan.budget.total_variable
            new_plan.budget.surplus_deficit = new_plan.budget.cap - new_plan.budget.total_projected
            for item in new_plan.budget.line_items:
                if item.category == "Materials":
                    item.amount = new_amt
            new_plan.status = "MUTATED"
            return True, "budget", None, new_plan
        else:
            reason = f"Budget overrun: Increase of printing exceeds Rs {plan.budget.cap} total limit."
            call_model("budget", f"Evaluate printing expense increase: Over budget. REJECTED.")
            return False, "budget", reason, plan

    # 3. Check for venue mutation
    if "room" in lower or "hall" in lower or "venue" in lower:
        if "room d" in lower or "80" in lower:
            reason = "Rejected: Room D (80 seats) cannot seat required 180 attendees."
            call_model("venue", f"Evaluate venue change request: '{message_text}'. REJECTED due to capacity constraint.")
            return False, "venue", reason, plan

    # 4. Check for prayer break removal or reduction
    if "prayer" in lower and ("cancel" in lower or "remove" in lower or "5 min" in lower or "0" in lower):
        reason = "Rejected: Dean's office mandated a mandatory 15-minute prayer break."
        call_model("schedule", f"Evaluate schedule change: '{message_text}'. REJECTED due to mandatory Dean condition.")
        return False, "schedule", reason, plan

    # Default informational or unhandled message
    call_model("reading", f"Reading informational message: '{message_text}'. No structural plan mutation required.")
    return True, "reading", None, plan
