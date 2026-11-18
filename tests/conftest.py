"""Isolated test setup: automated tests never call a live AI provider or send messages."""
import os
from pathlib import Path

import pytest

os.environ["PLANNER_MODE"] = "offline"
os.environ["GROQ_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["PLANNER_DB_PATH"] = ":memory:"
os.environ["WHATSAPP_DB_PATH"] = ":memory:"
os.environ["WHATSAPP_ALLOW_LIVE_SEND"] = "false"

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def sample_pack():
    return (ROOT / "sample_pack.txt").read_text(encoding="utf-8")


@pytest.fixture
def varied_pack():
    """Synthetic test input, deliberately different from official sample facts."""
    return """# Message 1
From: Director (email)
Date: 17 Nov
Message: Approved: a 5-hour hackathon for 96 students in teams of 4. The budget is Rs 400,000, all in. Eight staff will be on duty. Please keep a 20-minute prayer break in the schedule.

# Message 2
From: Campus Facilities (email)
Date: 16 Nov
Message: Room North seats 60 at Rs 30,000. Hall East seats 120 at Rs 65,000. Hall West seats 160 at Rs 90,000. Hall West has a standby generator.

# Message 3
From: Caterer (WhatsApp)
Date: 14 Nov
Message: Standard lunch box Rs 900 per head. Basic lunch box Rs 600 per head. Delivery free hai.

# Message 4
From: Judging coordinator (email)
Date: 15 Nov
Message: 10 judges have confirmed. The honorarium is Rs 3,000 each. A judge needs 12 minutes per team and should cover no more than three teams.

# Message 5
From: Finance (email)
Date: 15 Nov
Message: Already ordered from the event budget: prizes Rs 60,000, backup internet Rs 12,000, printing Rs 8,000.
"""


@pytest.fixture
def engine():
    from backend.app.engine.pipeline import PlanningEngine

    return PlanningEngine(database_path=":memory:")


@pytest.fixture
def api_client(monkeypatch, engine, sample_pack):
    import importlib
    from fastapi.testclient import TestClient

    engine.run_full_pipeline(sample_pack, mode="offline")
    main = importlib.import_module("backend.app.main")
    routes = importlib.import_module("backend.app.api.routes")
    exports = importlib.import_module("backend.app.api.export")
    monkeypatch.setattr(routes, "global_engine", engine)
    monkeypatch.setattr(exports, "global_engine", engine)
    monkeypatch.setenv("ORGANIZER_API_KEY", "")
    main.requests_by_client.clear()
    with TestClient(main.app, raise_server_exceptions=False) as client:
        yield client
