#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.manifest_validation import validate_manifest
from lib.response_validation import validate_response


MANIFEST = ROOT / "manifest.yml"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_scenario(scenario):
    fixture_path = ROOT / scenario["fixture"]
    fixture = load_json(fixture_path)

    response_results = []

    for response in scenario["responses"]:
        response_path = ROOT / response["file"]
        response_data = load_json(response_path)

        failures = validate_response(
            fixture,
            response_data,
        )

        expected_result = response["expected"]

        actual_result = (
            "pass"
            if not failures
            else "fail"
        )

        response_results.append(
            {
                "response": response_path.name,
                "expected": expected_result,
                "actual": (
                    "passed"
                    if actual_result == "pass"
                    else "failed"
                ),
                "failures": failures,
                "result_match": (
                    actual_result == expected_result
                ),
            }
        )

    failed = [
        result
        for result in response_results
        if not result["result_match"]
    ]

    return {
        "scenario": scenario["id"],
        "status": "failed" if failed else "passed",
        "results": response_results,
    }


def main():
    manifest = load_yaml(MANIFEST)

    manifest_failures = validate_manifest(
        manifest,
        ROOT,
    )

    if manifest_failures:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "reason": "invalid acceptance manifest",
                    "failures": manifest_failures,
                },
                indent=2,
            )
        )
        sys.exit(1)

    results = [
        validate_scenario(scenario)
        for scenario in manifest["scenarios"]
    ]

    failed = [
        result
        for result in results
        if result["status"] != "passed"
    ]

    output = {
        "status": "failed" if failed else "passed",
        "scenarios_checked": len(results),
        "results": results,
    }

    print(json.dumps(output, indent=2))

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
