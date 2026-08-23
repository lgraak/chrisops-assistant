#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.manifest_validation import validate_manifest


INVALID_MANIFEST = ROOT / "framework" / "invalid-manifest.yml"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main():
    manifest = load_yaml(INVALID_MANIFEST)

    failures = validate_manifest(
        manifest,
        ROOT,
    )

    result = {
        "fixture": INVALID_MANIFEST.name,
        "expected": "fail",
        "actual": "failed" if failures else "passed",
        "failures": failures,
    }

    result["status"] = (
        "passed"
        if failures
        else "failed"
    )

    print(json.dumps(result, indent=2))

    if result["status"] != "passed":
        sys.exit(1)


if __name__ == "__main__":
    main()
