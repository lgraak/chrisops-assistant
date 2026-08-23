#!/usr/bin/env python3

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.assistant_adapter import AssistantAdapter
from lib.providers.deterministic import DeterministicProvider


def main():
    if len(sys.argv) != 2:
        print(
            "usage: generate_response.py <fixture.json>",
            file=sys.stderr,
        )
        sys.exit(2)

    fixture_path = Path(sys.argv[1])

    with fixture_path.open("r", encoding="utf-8") as handle:
        fixture = json.load(handle)

    adapter = AssistantAdapter(
        DeterministicProvider()
    )

    response = adapter.generate(fixture)

    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
