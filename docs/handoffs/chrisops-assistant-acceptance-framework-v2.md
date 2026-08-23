# ChrisOps Assistant Acceptance Framework v2

## Status

The ChrisOps assistant acceptance system has evolved from scenario validation into a reusable acceptance framework.

Current commit:

29bfc58

## Completed Components

### Acceptance Manifest

The acceptance suite is now manifest-driven.

The manifest defines:

- available scenarios
- fixture location
- response location
- expected validation outcome

The manifest is the authoritative index of assistant acceptance scenarios.

## Acceptance Runner

Location:

tests/chrisops-assistant/bin/run_acceptance.py

Responsibilities:

- load acceptance manifest
- validate manifest structure
- execute declared scenarios
- evaluate expected responses
- report pass/fail state

## Framework Validation

Location:

tests/chrisops-assistant/bin/test_framework.py

Responsibilities:

- verify acceptance framework behavior
- confirm invalid manifests are rejected

## Shared Validation Library

Location:

tests/chrisops-assistant/lib/manifest_validation.py

The manifest validator is maintained as a shared library.

Consumers:

- acceptance runner
- framework tests

This prevents validation logic divergence.

## Current Scenarios

Implemented:

### active-warning

Purpose:

Validate that active findings are explained without unsupported remediation claims.

### missing-observation

Purpose:

Validate that missing observation data does not become an assumed outage or failure state.

## Current Guarantees

The framework verifies:

- expected passing responses pass
- expected failing responses fail
- invalid manifests are rejected
- assistant behavior contracts remain explicit

## Next Phase

The next development phase is integration with real ChrisOps state data.

Planned additions:

- state-derived fixtures
- operational finding scenarios
- asset health scenarios
- observation freshness scenarios

The acceptance framework remains the boundary between raw system state and assistant interpretation.
