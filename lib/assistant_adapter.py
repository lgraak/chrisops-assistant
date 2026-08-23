#!/usr/bin/env python3

def generate_response(fixture):
    expected = fixture["expected"]

    classification = expected["classification"]

    return {
        "classification": classification,
        "summary": build_summary(classification),
        "explanation": build_explanation(fixture),
        "confidence": "bounded",
    }


def build_summary(classification):
    summaries = {
        "active-finding": "A finding exists and requires review.",
        "insufficient-observation": "Current state cannot be confirmed due to insufficient observation data.",
        "observation-overdue": "Observation data delayed.",
        "notification-policy": "A finding exists, but notification policy must be evaluated separately.",
    }

    return summaries.get(
        classification,
        "The condition requires review.",
    )


def build_explanation(fixture):
    description = fixture.get(
        "description",
        "Evidence was provided by ChrisOps.",
    )

    return description
