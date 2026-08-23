#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
INVALID_MANIFEST = ROOT / "framework" / "invalid-manifest.yml"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_manifest(manifest):
    failures = []

    if not isinstance(manifest, dict):
        return ["manifest is not a YAML object"]

    if manifest.get("schema") != "chrisops.assistant.acceptance-manifest.v1":
        failures.append(
            "unsupported or missing manifest schema"
        )

    if "scenarios" not in manifest:
        failures.append(
            "manifest missing scenarios"
        )

    if failures:
        return failures

    for scenario in manifest["scenarios"]:
        scenario_id = scenario.get("id", "<missing>")

        required_keys = {
            "id",
            "fixture",
            "responses",
        }

        missing = required_keys - scenario.keys()

        if missing:
            failures.append(
                f"{scenario_id}: missing keys {sorted(missing)}"
            )

    return failures


def main():
    manifest = load_yaml(INVALID_MANIFEST)

    failures = validate_manifest(manifest)

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
