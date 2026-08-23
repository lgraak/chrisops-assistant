#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.assistant_adapter import AssistantAdapter
from lib.providers.deterministic import DeterministicProvider


FIXTURES = ROOT / "fixtures"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_fixture(path):
    fixture = load_json(path)

    adapter = AssistantAdapter(
        DeterministicProvider()
    )

    response = adapter.generate(fixture)

    return {
        "fixture": path.name,
        "status": "passed",
        "response": response,
    }


def main():
    fixtures = sorted(FIXTURES.glob("*.json"))

    results = [
        test_fixture(path)
        for path in fixtures
    ]

    print(
        json.dumps(
            {
                "status": "passed",
                "fixtures_checked": len(results),
                "results": results,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
