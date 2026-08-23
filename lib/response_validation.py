#!/usr/bin/env python3


import json


def validate_response(fixture, response):
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

    return failures
