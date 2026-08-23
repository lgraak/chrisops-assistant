#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.assistant_adapter import AssistantAdapter
from lib.provider_factory import get_provider


PROVIDER_CONFIG = ROOT / "config/provider.yml"


def load_provider():
    with PROVIDER_CONFIG.open(
        "r",
        encoding="utf-8",
    ) as handle:
        config = yaml.safe_load(handle)

    return get_provider(config["provider"])


def main():
    if len(sys.argv) != 2:
        print(
            "usage: generate_response.py <fixture.json>",
            file=sys.stderr,
        )
        sys.exit(2)

    fixture_path = Path(sys.argv[1])

    with fixture_path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        fixture = json.load(handle)

    adapter = AssistantAdapter(
        load_provider()
    )

    response = adapter.generate(fixture)

    print(
        json.dumps(
            response,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
