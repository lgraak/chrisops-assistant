#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "manifest.yml"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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
            continue

        fixture = ROOT / scenario["fixture"]

        if not fixture.exists():
            failures.append(
                f"{scenario_id}: fixture not found: {fixture}"
            )

        if not isinstance(scenario["responses"], list):
            failures.append(
                f"{scenario_id}: responses must be a list"
            )
            continue

        for response in scenario["responses"]:
            response_file = response.get("file")
            expected = response.get("expected")

            if not response_file:
                failures.append(
                    f"{scenario_id}: response missing file"
                )

            if expected not in {"pass", "fail"}:
                failures.append(
                    f"{scenario_id}: invalid expected result {expected}"
                )

            if response_file:
                path = ROOT / response_file

                if not path.exists():
                    failures.append(
                        f"{scenario_id}: response not found: {path}"
                    )

    return failures


def evaluate_response(fixture, response):
    expected = fixture["expected"]

    classification = expected["classification"]
    required = expected.get("required_statements", [])
    prohibited = expected.get("prohibited_statements", [])

    response_text = json.dumps(response).lower()

    failures = []

    if classification.lower() not in response_text:
        failures.append(
            f"missing expected classification: {classification}"
        )

    for statement in required:
        if statement.lower() not in response_text:
            failures.append(
                f"missing required statement: {statement}"
            )

    for statement in prohibited:
        if statement.lower() in response_text:
            failures.append(
                f"contains prohibited statement: {statement}"
            )

    return {
        "actual": "passed" if not failures else "failed",
        "failures": failures,
    }


def validate_scenario(scenario):
    fixture_path = ROOT / scenario["fixture"]
    fixture = load_json(fixture_path)

    response_results = []

    for response in scenario["responses"]:
        response_path = ROOT / response["file"]
        response_data = load_json(response_path)

        evaluation = evaluate_response(
            fixture,
            response_data,
        )

        expected_result = response["expected"]

        actual_result = (
            "pass"
            if evaluation["actual"] == "passed"
            else "fail"
        )

        response_results.append(
            {
                "response": response_path.name,
                "expected": expected_result,
                "actual": evaluation["actual"],
                "failures": evaluation["failures"],
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

    manifest_failures = validate_manifest(manifest)

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

    scenarios = manifest["scenarios"]

    results = [
        validate_scenario(scenario)
        for scenario in scenarios
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
