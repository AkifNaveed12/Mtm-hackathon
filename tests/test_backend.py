import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "HackPlan AI Backend Online" in response.json()["message"]

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_provider" in data

def test_api_run_default():
    response = client.post("/api/run", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "plan" in data
    assert "checks" in data
    assert "trace" in data
    assert data["checks"]["all_passed"] is True

def test_api_plan():
    # After run, plan should be retrievable
    response = client.get("/api/plan")
    assert response.status_code == 200
    data = response.json()
    assert "plan" in data
    assert "checks" in data

def test_api_trace():
    response = client.get("/api/trace")
    assert response.status_code == 200
    data = response.json()
    assert "entries" in data
    assert len(data["entries"]) >= 1

def test_api_message_update_valid():
    msg = {"message": "Printing expense is updated to Rs 15,000.", "sender": "Finance"}
    response = client.post("/api/message", json=msg)
    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is True
    assert data["plan"]["budget"]["total_projected"] == 601000.0

def test_api_message_rejection_catering():
    msg = {"message": "Can we reduce lunch boxes to 100 meals?", "sender": "Caterer"}
    response = client.post("/api/message", json=msg)
    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is False
    assert data["rejection_reason"] is not None

def test_api_rejected():
    response = client.get("/api/rejected")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["target_area"] == "food"

def test_api_export():
    response = client.get("/api/export")
    assert response.status_code == 200
    data = response.json()
    assert data["competition"] == "Mind to Machine Hackathon 2026"
    assert "plan" in data
    assert "checks" in data
    assert "trace" in data
