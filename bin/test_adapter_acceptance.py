#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.configuration import load_adapter
from lib.response_validation import validate_response


FIXTURES = ROOT / "fixtures"
PROVIDER_CONFIG = ROOT / "config/provider.yml"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_fixture(path):
    fixture = load_json(path)

    adapter = load_adapter(PROVIDER_CONFIG)

    response = adapter.generate(fixture)

    failures = validate_response(
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
    fixtures = sorted(
        FIXTURES.glob("*.json")
    )

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
