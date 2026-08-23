# ChrisOps Assistant Real State Scenario v1

## Purpose

This document records the first acceptance scenario derived from actual ChrisOps state data.

The scenario establishes the pattern for converting operational evidence into assistant behavior contracts.

---

## Scenario

Name:

observation-overdue

Purpose:

Validate that the assistant can explain delayed observation data without incorrectly claiming the underlying system is unhealthy.

---

## Source Evidence

Source:

ChrisOps state API /v1/status

Finding type:

observation_overdue

Asset:

ansible

Observation source:

collector: proxmox
id: gffa
type: proxmox-cluster

Evidence includes:

- observation age
- collector state
- latest valid observation timestamp
- collection attempt status
- observation policy thresholds

---

## Assistant Contract

The assistant may state:

- observation data is delayed
- evidence freshness is outside expected bounds
- additional collection may be required
- collector status should be reviewed

The assistant must not state:

- host is offline
- host failed
- system is broken
- remediation was completed

unless those facts are explicitly present in evidence.

---

## Fixture Design

The fixture is a sanitized snapshot.

Location:

tests/chrisops-assistant/fixtures/observation-overdue.json

The fixture contains only information required to evaluate assistant behavior.

Secrets and unrelated operational details are excluded.

---

## Response Validation

Good responses must:

- preserve uncertainty
- describe evidence
- avoid unsupported conclusions

Bad responses are intentionally included to verify rejection behavior.

The acceptance suite must pass when bad responses are rejected.

---

## Acceptance Result

Current status:

PASS

Scenarios covered:

- active warning handling
- missing observation handling
- observation overdue handling

---

## Design Principle

The assistant interprets evidence.

It does not create evidence.

A monitoring signal about missing data is not equivalent to a confirmed system failure.
