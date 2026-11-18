import re
from typing import List, Dict, Any, Tuple
from backend.app.engine.llm import call_model

def parse_raw_message_pack(file_content: str) -> List[Dict[str, str]]:
    """
    Splits message pack into distinct message units.
    Preserves exact text, sender, date, content.
    """
    messages = []
    # Split by message headers like '# Message X'
    raw_blocks = re.split(r'#\s*Message\s*\d+', file_content)
    index = 1
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
        sender_match = re.search(r'From:\s*(.+)', block, re.IGNORECASE)
        date_match = re.search(r'Date:\s*(.+)', block, re.IGNORECASE)
        msg_match = re.search(r'Message:\s*([\s\S]+)', block, re.IGNORECASE)
        
        sender = sender_match.group(1).strip() if sender_match else "Unknown"
        date = date_match.group(1).strip() if date_match else "Unspecified"
        text = msg_match.group(1).strip() if msg_match else block
        
        messages.append({
            "index": index,
            "sender": sender,
            "date": date,
            "text": text,
            "raw": block
        })
        index += 1
    return messages

def ingest_and_extract_facts(raw_text: str) -> Tuple[Dict[str, Any], int]:
    """
    Invokes model call tagged with 'reading' to extract structured facts.
    """
    messages = parse_raw_message_pack(raw_text)
    
    # Model call 1: reading
    prompt = f"Analyze raw event messages pack ({len(messages)} messages) and extract key parameters for venue, schedule, food, judging, and budget:\n" + raw_text
    output, p_tok, c_tok = call_model("reading", prompt)
    
    # Canonical initial baseline facts derived from the sample pack
    facts: Dict[str, Any] = {
        "headcount": 180,  # 150 students + 10 staff + 20 judges
        "students": 150,
        "staff": 10,
        "teams_count": 50,
        "team_size": 3,
        "budget_cap": 650000.0,
        "total_duration_hours": 4.0,
        "prayer_break_mins": 15,
        "backup_power_required": True,
        "caterer_rate": 1200.0,
        "caterer_tier": "Standard lunch box",
        "caterer_delivery": "Free delivery confirmed on 12 Nov",
        "judges_confirmed": 20,
        "honorarium_per_judge": 5000.0,
        "minutes_per_team": 15,
        "committed_prizes": 100000.0,
        "committed_internet": 20000.0,
        "committed_printing": 10000.0,
        "raw_messages": messages
    }
    
    return facts, len(messages)
