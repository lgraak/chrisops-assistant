#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = ROOT / "fixtures"
RESPONSE_ROOT = ROOT / "responses"
EVALUATOR = Path(__file__).resolve().parent / "evaluate_response.py"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_evaluator(fixture, response):
    result = subprocess.run(
        [
            str(EVALUATOR),
            str(fixture),
            str(response),
        ],
        capture_output=True,
        text=True,
    )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "status": "failed",
            "reason": result.stderr.strip(),
        }


def validate_fixture(path):
    fixture = load_json(path)

    required = {
        "id",
        "description",
        "facts",
        "expected",
    }

    missing = required - fixture.keys()

    if missing:
        return {
            "fixture": path.name,
            "status": "failed",
            "reason": f"missing keys: {sorted(missing)}",
        }

    return None


def evaluate_fixture(fixture_path):
    fixture = load_json(fixture_path)

    fixture_id = fixture["id"]

    results = []

    good_response = RESPONSE_ROOT / f"{fixture_id}-good.json"
    bad_response = RESPONSE_ROOT / f"{fixture_id}-bad.json"

    if good_response.exists():
        result = run_evaluator(
            fixture_path,
            good_response,
        )

        results.append(
            {
                "response": good_response.name,
                "expected": "pass",
                "actual": result["status"],
            }
        )

        if result["status"] != "passed":
            return {
                "fixture": fixture_id,
                "status": "failed",
                "results": results,
            }

    if bad_response.exists():
        result = run_evaluator(
            fixture_path,
            bad_response,
        )

        results.append(
            {
                "response": bad_response.name,
                "expected": "fail",
                "actual": result["status"],
            }
        )

        if result["status"] != "failed":
            return {
                "fixture": fixture_id,
                "status": "failed",
                "results": results,
            }

    return {
        "fixture": fixture_id,
        "status": "passed",
        "results": results,
    }


def main():
    fixtures = sorted(FIXTURE_ROOT.glob("*.json"))

    if not fixtures:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "reason": "no fixtures found",
                },
                indent=2,
            )
        )
        sys.exit(1)

    results = []

    for fixture in fixtures:
        validation_error = validate_fixture(fixture)

        if validation_error:
            results.append(validation_error)
            continue

        results.append(
            evaluate_fixture(fixture)
        )

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
