#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.response_validation import validate_response


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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

    failures = validate_response(
        fixture,
        response,
    )

    result = {
        "fixture": fixture["id"],
        "classification": fixture["expected"]["classification"],
        "status": "passed" if not failures else "failed",
        "failures": failures,
    }

    print(json.dumps(result, indent=2))

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
