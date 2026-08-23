#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.assistant_adapter import generate_response


FIXTURES = ROOT / "fixtures"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_fixture(path):
    fixture = load_json(path)

    response = generate_response(fixture)

    expected_classification = fixture["expected"]["classification"]

    failures = []

    if response.get("classification") != expected_classification:
        failures.append(
            f"expected classification {expected_classification}, "
            f"got {response.get('classification')}"
        )

    if not response.get("summary"):
        failures.append("missing summary")

    if not response.get("explanation"):
        failures.append("missing explanation")

    if not response.get("confidence"):
        failures.append("missing confidence")

    return {
        "fixture": path.name,
        "status": "passed" if not failures else "failed",
        "failures": failures,
        "response": response,
    }


def main():
    fixtures = sorted(FIXTURES.glob("*.json"))

    results = [
        test_fixture(path)
        for path in fixtures
    ]

    failed = [
        result
        for result in results
        if result["status"] != "passed"
    ]

    output = {
        "status": "failed" if failed else "passed",
        "fixtures_checked": len(results),
        "results": results,
    }

    print(json.dumps(output, indent=2))

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
