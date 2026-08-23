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


def evaluate_generated_response(fixture, response):
    expected = fixture["expected"]

    failures = []

    classification = expected["classification"]

    if response.get("classification") != classification:
        failures.append(
            f"expected classification {classification}, "
            f"got {response.get('classification')}"
        )

    response_text = json.dumps(response).lower()

    for statement in expected.get("required_statements", []):
        if statement.lower() not in response_text:
            failures.append(
                f"missing required statement: {statement}"
            )

    for statement in expected.get("prohibited_statements", []):
        if statement.lower() in response_text:
            failures.append(
                f"contains prohibited statement: {statement}"
            )

    return failures


def test_fixture(path):
    fixture = load_json(path)

    response = generate_response(fixture)

    failures = evaluate_generated_response(
        fixture,
        response,
    )

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
