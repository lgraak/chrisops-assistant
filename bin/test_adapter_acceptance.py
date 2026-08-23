#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.assistant_adapter import AssistantAdapter
from lib.provider_factory import get_provider
from lib.response_validation import validate_response


FIXTURES = ROOT / "fixtures"
PROVIDER_CONFIG = ROOT / "config/provider.yml"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_provider():
    with PROVIDER_CONFIG.open(
        "r",
        encoding="utf-8",
    ) as handle:
        config = yaml.safe_load(handle)

    return get_provider(config["provider"])


def test_fixture(path):
    fixture = load_json(path)

    adapter = AssistantAdapter(
        load_provider()
    )

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
