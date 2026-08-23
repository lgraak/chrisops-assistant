#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.manifest_validation import validate_manifest


INVALID_MANIFEST = ROOT / "framework" / "invalid-manifest.yml"
MANIFEST = ROOT / "manifest.yml"
SCENARIO_INDEX = ROOT / "scenario-index.yml"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_scenario_index(manifest, scenario_index):
    failures = []

    manifest_scenarios = {
        scenario["id"]
        for scenario in manifest.get("scenarios", [])
    }

    indexed_scenarios = {
        scenario["id"]
        for scenario in scenario_index.get("scenarios", [])
    }

    missing = manifest_scenarios - indexed_scenarios

    for scenario_id in sorted(missing):
        failures.append(
            f"scenario missing from index: {scenario_id}"
        )

    return failures


def run_invalid_manifest_test():
    manifest = load_yaml(INVALID_MANIFEST)

    failures = validate_manifest(
        manifest,
        ROOT,
    )

    return {
        "fixture": INVALID_MANIFEST.name,
        "expected": "fail",
        "actual": "failed" if failures else "passed",
        "failures": failures,
        "status": "passed" if failures else "failed",
    }


def run_scenario_index_test():
    manifest = load_yaml(MANIFEST)
    scenario_index = load_yaml(SCENARIO_INDEX)

    failures = validate_scenario_index(
        manifest,
        scenario_index,
    )

    return {
        "fixture": SCENARIO_INDEX.name,
        "expected": "pass",
        "actual": "failed" if failures else "passed",
        "failures": failures,
        "status": "passed" if not failures else "failed",
    }


def main():
    results = [
        run_invalid_manifest_test(),
        run_scenario_index_test(),
    ]

    failed = [
        result
        for result in results
        if result["status"] != "passed"
    ]

    output = {
        "status": "failed" if failed else "passed",
        "tests_checked": len(results),
        "results": results,
    }

    print(json.dumps(output, indent=2))

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
