"""Read-only OSV advisory lookup for installed Python package versions.

Only public package names and versions are submitted. No environment variables,
source messages, credentials or application records are sent.
"""
from importlib.metadata import distributions
import json
from pathlib import Path

import httpx


def main():
    packages = sorted({(dist.metadata["Name"], dist.version) for dist in distributions()})
    findings = []
    try:
        for offset in range(0, len(packages), 100):
            batch = packages[offset:offset+100]
            response = httpx.post("https://api.osv.dev/v1/querybatch", timeout=25,
                json={"queries": [{"package": {"name": name, "ecosystem": "PyPI"}, "version": version}
                                  for name, version in batch]})
            response.raise_for_status()
            results = response.json()["results"]
            for (name, version), result in zip(batch, results):
                for advisory in result.get("vulns", []):
                    findings.append({"package": name, "version": version, "id": advisory["id"],
                                     "url": "https://osv.dev/vulnerability/" + advisory["id"]})
    except (httpx.HTTPError, ValueError, KeyError):
        print("Dependency advisory lookup unavailable; no clean-audit claim is made.")
        return 2
    report = {"source": "https://api.osv.dev", "packages_checked": len(packages), "findings": findings}
    output = Path(__file__).resolve().parents[1] / "artifacts"
    output.mkdir(exist_ok=True)
    (output / "python-dependency-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
