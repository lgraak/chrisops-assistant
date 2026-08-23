#!/usr/bin/env python3

from pathlib import Path


def validate_manifest(manifest, root):
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

        fixture = root / scenario["fixture"]

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
                path = root / response_file

                if not path.exists():
                    failures.append(
                        f"{scenario_id}: response not found: {path}"
                    )

    return failures
