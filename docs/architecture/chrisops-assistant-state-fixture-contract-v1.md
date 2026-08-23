# ChrisOps Assistant State Fixture Contract v1

## Purpose

This document defines how ChrisOps state data becomes assistant acceptance fixtures.

The acceptance framework must validate assistant behavior against stable, reproducible inputs.

Live system state must not directly drive acceptance results.

Acceptance fixtures represent approved snapshots of system conditions.

---

## Fixture Philosophy

Fixtures are not a live monitoring feed.

They are controlled evidence snapshots used to verify assistant behavior.

A fixture represents:

- known system facts
- available evidence
- expected assistant interpretation boundaries

A fixture does not represent:

- a diagnosis
- a remediation plan
- an operator decision

The assistant must reason only from the facts contained in the fixture.

---

## Fixture Lifecycle

The fixture lifecycle is:

ChrisOps State API
        |
        v
State extraction
        |
        v
Sanitization
        |
        v
Acceptance fixture
        |
        v
Assistant contract validation

Each stage has a defined responsibility.

---

## Source Data

The source of operational facts is the ChrisOps state API.

Example:

/v1/status

The API is the source of truth for observed system state.

Acceptance fixtures are derived artifacts.

They are not authoritative replacements for ChrisOps state.

---

## Fixture Requirements

A valid fixture must contain:

- scenario identifier
- description
- available facts
- expected assistant behavior

Example structure:

```json
{
  "id": "observation-overdue",
  "description": "Observation freshness exceeded policy threshold.",
  "facts": {},
  "expected": {}
}
Sanitization Rules
Fixtures must not contain:
- authentication tokens
- credentials
- private keys
- secrets
- unnecessary personal information
Fixtures should contain only information required to evaluate assistant behavior.
Snapshot Policy
Fixtures should be immutable after acceptance.
If behavior requirements change:
1. create a new fixture revision
2. document the reason
3. update acceptance expectations
4. commit the change
Do not silently modify existing fixtures.
The acceptance history must remain reviewable.
Real State Scenario Example
A future observation freshness scenario may contain:
Facts:
asset:
  id: ansible

condition:
  type: observation_overdue

evidence:
  collector: proxmox
  latest_valid_observation: timestamp
  age_seconds: value
The assistant may state:
- observation data is stale
- additional collection may be required
- investigation may be appropriate
The assistant may not state:
- host is offline
- system is broken
- remediation completed
- configuration changed
unless those facts exist in the evidence.
Acceptance Relationship
State fixtures connect operational truth to assistant behavior.
The relationship is:
ChrisOps state
      |
      v
Fixture facts
      |
      v
Assistant response
      |
      v
Acceptance evaluator
The evaluator determines whether the response stays within the approved reasoning boundary.
Design Principle
The assistant is an interpretation layer.
It may summarize evidence.
It may classify known conditions.
It may explain uncertainty.
It may not create evidence that does not exist.
The fixture system exists to preserve that boundary over time.

After saving:

```bash
