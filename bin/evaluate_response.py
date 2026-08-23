#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_response(fixture, response):
    expected = fixture["expected"]

    classification = expected["classification"]
    required = expected.get("required_statements", [])
    allowed = expected.get("allowed_statements", [])
    prohibited = expected.get("prohibited_statements", [])

    response_text = json.dumps(response).lower()

    failures = []

    if classification not in response_text:
        failures.append(
            f"missing expected classification: {classification}"
        )

    for statement in required:
        if statement.lower() not in response_text:
            failures.append(
                f"missing required statement: {statement}"
            )

    for statement in prohibited:
        if statement.lower() in response_text:
            failures.append(
                f"contains prohibited statement: {statement}"
            )

    allowed_matches = [
        statement
        for statement in allowed
        if statement.lower() in response_text
    ]

    return {
        "fixture": fixture["id"],
        "classification": classification,
        "status": "passed" if not failures else "failed",
        "allowed_statement_matches": allowed_matches,
        "failures": failures,
    }


def main():
    if len(sys.argv) != 3:
        print(
            "usage: evaluate_response.py <fixture.json> <response.json>",
            file=sys.stderr,
        )
        sys.exit(2)

    fixture_path = Path(sys.argv[1])
    response_path = Path(sys.argv[2])

    fixture = load_json(fixture_path)
    response = load_json(response_path)

    result = validate_response(fixture, response)

    print(json.dumps(result, indent=2))

    if result["status"] != "passed":
        sys.exit(1)


if __name__ == "__main__":
    main()
