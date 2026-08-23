# ChrisOps Assistant Adapter Milestone v1

## Purpose

This document records the completion of the first ChrisOps assistant
adapter milestone.

The project has moved from static acceptance examples to a working
assistant adapter boundary.

The adapter remains separate from the source of truth.

ChrisOps remains authoritative for operational state.

------------------------------------------------------------------------

## Completed Components

The following components are complete:

-   assistant interaction contract
-   assistant adapter contract
-   deterministic assistant adapter implementation
-   adapter response validation
-   adapter acceptance testing
-   shared response validation library

------------------------------------------------------------------------

## Current Flow

The current execution path is:

    ChrisOps Fixture
            |
            v
    Assistant Adapter
            |
            v
    Generated Response
            |
            v
    Response Validation
            |
            v
    Acceptance Result

------------------------------------------------------------------------

## Adapter Implementation

Location:

    tests/chrisops-assistant/lib/assistant_adapter.py

The adapter currently provides deterministic response generation.

It is intentionally simple.

The purpose is to prove the contract boundary before introducing
model-based generation.

------------------------------------------------------------------------

## Adapter Commands

Response generation:

    tests/chrisops-assistant/bin/generate_response.py

Adapter validation:

    tests/chrisops-assistant/bin/test_adapter.py

Adapter acceptance:

    tests/chrisops-assistant/bin/test_adapter_acceptance.py

------------------------------------------------------------------------

## Shared Validation

The validation layer has been separated into reusable libraries.

Current libraries:

    tests/chrisops-assistant/lib/

    manifest_validation.py
    response_validation.py
    assistant_adapter.py

Consumers use shared validation logic rather than maintaining duplicate
implementations.

------------------------------------------------------------------------

## Acceptance Coverage

Current scenarios:

### active-warning

Validates:

-   findings are explained accurately
-   remediation is not invented

### missing-observation

Validates:

-   missing evidence is preserved as uncertainty
-   unavailable data is not converted into failure state

### observation-overdue

Validates:

-   collector freshness problems are not treated as host outages

### finding-notification-policy

Validates:

-   findings and notification decisions remain separate concepts

------------------------------------------------------------------------

## Current Validation Commands

Acceptance suite:

    ./tests/chrisops-assistant/bin/run_acceptance.py

Adapter validation:

    ./tests/chrisops-assistant/bin/test_adapter_acceptance.py

Framework validation:

    ./tests/chrisops-assistant/bin/test_framework.py

All current checks must pass before changes are accepted.

------------------------------------------------------------------------

## Future Model Integration

The adapter boundary intentionally separates implementation from
contract.

Future implementations may introduce:

-   local language models
-   retrieval augmentation
-   additional reasoning components

The model is responsible for generating responses.

The acceptance framework remains responsible for determining whether
those responses stay within approved boundaries.

------------------------------------------------------------------------

## Design Principle

The assistant is an interpretation layer.

It may summarize evidence.

It may explain conditions.

It may communicate uncertainty.

It may not create evidence.

ChrisOps remains the source of truth.
