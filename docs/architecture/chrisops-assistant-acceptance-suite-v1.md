# ChrisOps Assistant Acceptance Suite v1

## Purpose

The acceptance suite validates assistant behavior against deterministic contracts.

The suite exists to ensure the assistant:

- reports known facts accurately
- preserves uncertainty boundaries
- does not invent remediation
- does not claim unsupported system state

## Test Structure

Tests are organized into three components.

### Fixtures

Location:

fixtures/

Fixtures define:

- input facts
- expected classification
- required statements
- allowed statements
- prohibited statements

Fixtures represent the scenario contract.

### Response Fixtures

Location:

responses/

Response fixtures represent candidate assistant outputs.

Naming convention:

<fixture-id>-good.json
<fixture-id>-bad.json

Good responses must satisfy the fixture contract.

Bad responses intentionally violate one or more rules and should fail evaluation.

### Evaluator

Location:

bin/evaluate_response.py

The evaluator performs deterministic checks.

It verifies:

- classification matches
- required statements exist
- prohibited statements are absent
- contract boundaries are respected

## Design Decision

The acceptance suite intentionally avoids semantic grading.

The purpose is not to determine whether a response is generally good.

The purpose is to prevent unsafe or unsupported assistant behavior.

## Future Expansion

Future versions may add:

- automated response discovery
- batch execution
- CI integration
- regression reporting
- additional reasoning boundary tests
