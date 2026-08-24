# ChrisOps Assistant Acceptance Scenarios v1

## Purpose

This document indexes the approved ChrisOps assistant acceptance scenarios.

Each scenario defines a reasoning boundary that the assistant must preserve.

The acceptance suite validates that assistant responses remain within available evidence and approved operational policy.

---

## Scenario Index

| Scenario | Purpose | Boundary |
|---|---|---|
| active-warning | Validate handling of active findings | Finding existence does not provide root cause or remediation |
| missing-observation | Validate handling of missing evidence | Missing data does not prove system failure |
| observation-overdue | Validate stale collector data handling | Observation delay does not prove asset outage |
| finding-notification-policy | Validate notification interpretation | Finding existence does not automatically require escalation |

---

## active-warning

Location:

fixtures/active-warning.json

Validates:

- findings are acknowledged
- evidence is summarized
- unsupported remediation is avoided

The assistant must not claim:

- issue fixed
- restart completed
- configuration changed

---

## missing-observation

Location:

missing-observation.json

Validates:

- lack of observation data is represented accurately
- uncertainty is preserved

The assistant must not claim:

- host is offline
- host is broken
- host failed

---

## observation-overdue

Location:

observation-overdue.json

Source:

ChrisOps state API observation freshness finding.

Validates:

- collector evidence delays are explained correctly
- observation health is separated from asset health

The assistant must not claim:

- host outage
- system failure
- remediation completion

---

## finding-notification-policy

Location:

finding-notification-policy.json

Source:

ChrisOps finding and notification policy state.

Validates:

- findings and notification decisions are separate concepts
- escalation is based on policy evidence

The assistant must not claim:

- immediate escalation
- paging requirement
- incident declaration

without supporting policy evidence.

---

## Design Rule

The assistant is an interpretation layer.

It may:

- summarize evidence
- explain conditions
- describe uncertainty
- identify relevant policy state

It may not:

- invent operational facts
- infer unavailable evidence
- claim actions occurred without evidence
- override notification policy

---

## Adding New Scenarios

New scenarios should include:

1. A sanitized fixture.
2. Good and bad response examples.
3. Manifest registration.
4. Acceptance validation.
5. Documentation entry.

A scenario is complete only when the acceptance suite passes.
