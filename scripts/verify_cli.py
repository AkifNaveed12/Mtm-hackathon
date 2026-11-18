"""Verify the official same-command full-pack/update flow in isolated local state."""
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    from backend.app.engine.pipeline import PlanningEngine

    directory = ROOT / "data"
    directory.mkdir(exist_ok=True)
    database = directory / f"cli-test-{uuid.uuid4().hex[:8]}.sqlite3"
    environment = dict(os.environ, PLANNER_MODE="offline", PLANNER_DB_PATH=str(database))
    total = None
    previous = None
    results = []
    for filename in ("sample_pack.txt", "tests/fixtures/printing_update.txt", "tests/fixtures/catering_invalid.txt"):
        result = subprocess.run([sys.executable, "run.py", filename], cwd=ROOT,
                                env=environment, capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, f"CLI failed for {filename}; output is intentionally not echoed."
        assert result.stdout.count(": PASS") == 6, "All six quality checks must pass."
        current = PlanningEngine(database_path=str(database))
        snapshot = current.active_plan.model_dump()
        assert current.tracer.get_log().total_calls == 0, "Offline parsing must not invent model calls."
        if total is None:
            total = snapshot["budget"]["total_projected"]
        elif filename.endswith("printing_update.txt"):
            assert snapshot["budget"]["total_projected"] == total + 5000
        else:
            assert "REJECTED:" in result.stdout
            assert snapshot == previous, "Rejected update must preserve the valid plan exactly."
            assert current.rejected_records
        previous = snapshot
        results.append({"input": filename, "exit_code": result.returncode,
                        "checks": "6 passed", "model_calls": 0})
    print(json.dumps({"same_command_cli": "passed", "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
