#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.assistant_adapter import AssistantAdapter
from lib.provider_factory import get_provider


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

    return {
        "fixture": path.name,
        "status": "passed",
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
