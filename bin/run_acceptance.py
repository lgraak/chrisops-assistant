#!/usr/bin/env python3

import json
import sys
from pathlib import Path


FIXTURE_ROOT = Path(__file__).resolve().parent.parent / "fixtures"


REQUIRED_TOP_LEVEL_KEYS = {
    "id",
    "description",
    "facts",
    "expected",
}


REQUIRED_EXPECTED_KEYS = {
    "classification",
    "required_statements",
    "allowed_statements",
    "prohibited_statements",
}


def load_fixture(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_fixture(path):
    fixture = load_fixture(path)

    missing = REQUIRED_TOP_LEVEL_KEYS - fixture.keys()

    if missing:
        return {
            "fixture": str(path),
            "status": "failed",
            "reason": f"missing top-level keys: {sorted(missing)}",
        }

    expected_missing = REQUIRED_EXPECTED_KEYS - fixture["expected"].keys()

    if expected_missing:
        return {
            "fixture": str(path),
            "status": "failed",
            "reason": f"missing expected keys: {sorted(expected_missing)}",
        }

    return {
        "fixture": str(path),
        "status": "passed",
        "classification": fixture["expected"]["classification"],
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

    results = [
        validate_fixture(path)
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
