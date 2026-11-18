"""Read-only local source audit. Reports names/locations, never secret values."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    env = dotenv_values(ROOT / ".env")
    secret_values = {
        name: value for name, value in env.items()
        if re.search(r"KEY|TOKEN|SECRET|PASSWORD", name, re.I)
        and value and len(value) >= 12 and not value.startswith("your_")
    }
    listed = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True).stdout
    tracked = set(listed.decode("utf-8").split("\0")) - {""}
    # Scan current application sources as well as tracked files, including untracked new code.
    sources = set(tracked)
    for directory in ("backend", "frontend/app", "frontend/components", "frontend/lib", "tests", "scripts"):
        for path in (ROOT / directory).rglob("*"):
            if path.is_file() and path.suffix in {".py", ".ts", ".tsx", ".js", ".mjs", ".json", ".md"}:
                if not any(part in {"node_modules", "__pycache__", ".next"} for part in path.parts):
                    sources.add(path.relative_to(ROOT).as_posix())
    findings = []
    for relative in sorted(sources):
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            if relative in tracked:
                findings.append({"severity": "critical", "file": relative, "issue": "Real environment file is tracked"})
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for name, value in secret_values.items():
            if value in text:
                findings.append({"severity": "critical", "file": relative,
                                 "issue": "Configured secret value found", "variable": name})
        if relative.startswith("frontend/"):
            for name in set(re.findall(r"NEXT_PUBLIC_[A-Z0-9_]+", text)):
                if re.search(r"SECRET|TOKEN|PASSWORD|SERVICE_ROLE|PRIVATE|API_KEY", name):
                    findings.append({"severity": "critical", "file": relative,
                                     "issue": "Private credential uses a public variable", "variable": name})
    ignored_checks = {}
    for candidate in (".env", ".venv/", "frontend/node_modules/", "data/planner.sqlite3", "data/whatsapp.sqlite3", ".local-logs/backend.err.log"):
        result = subprocess.run(["git", "check-ignore", "-q", candidate], cwd=ROOT, capture_output=True)
        ignored_checks[candidate] = result.returncode == 0
        if result.returncode != 0:
            findings.append({"severity": "high", "file": candidate, "issue": "Private/generated path is not ignored"})
    report = {"scanned_files": len(sources), "configured_secret_names_checked": sorted(secret_values),
              "ignored_paths": ignored_checks, "findings": findings,
              "limitations": ["This source audit does not prove absence of unknown secrets or all application vulnerabilities.",
                              "Dependency advisory checks and runtime authorization/webhook tests are separate checks."]}
    print(json.dumps(report, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
