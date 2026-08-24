# ChrisOps Assistant Interaction Contract v1

## Purpose

This document defines the interface contract between ChrisOps operational state and an assistant interpretation layer.

The assistant exists to interpret approved operational evidence and communicate it to users.

The assistant does not replace ChrisOps state evaluation and does not become a source of truth.

---

## Design Principle

The assistant is an interpretation layer.

The assistant may:

- summarize known evidence
- explain detected conditions
- describe uncertainty
- identify relevant policy information
- organize information for human understanding

The assistant may not:

- create evidence
- infer unavailable system state
- claim actions occurred without evidence
- override operational policy
- convert uncertainty into certainty

---

## Interaction Flow

The expected interaction flow is:

```
ChrisOps State
      |
      v
Assistant Input Contract
      |
      v
Assistant Adapter
      |
      v
Assistant Response Contract
      |
      v
Acceptance Validation
```

Each stage has a defined responsibility.

---

## Input Contract

The assistant receives structured evidence.

Input data may include:

- asset identity
- observed conditions
- findings
- policy information
- timestamps
- evidence references

Example:

```json
{
  "asset_id": "ansible",
  "condition": {
    "type": "observation_overdue",
    "severity": "warning"
  },
  "evidence": {
    "collector": "proxmox",
    "age_seconds": 1482
  }
}
```

---

## Evidence Boundary

The assistant may only reason from provided evidence.

If evidence is unavailable, the assistant must state that the current state cannot be confirmed.

The assistant must not fill missing information with assumptions.

Allowed:

```
Observation data is unavailable.
Additional collection may be required.
```

Not allowed:

```
The host is offline.
```

unless that fact exists in evidence.

---

## Response Contract

Assistant responses should contain structured fields.

Example:

```json
{
  "classification": "observation-overdue",
  "summary": "Observation data is delayed.",
  "explanation": "The Proxmox collector did not provide fresh evidence within the expected interval.",
  "confidence": "bounded"
}
```

---

## Classification

The classification field identifies the assistant interpretation category.

Examples:

```
active-finding
missing-observation
observation-overdue
notification-policy
```

Classification describes the evidence category being explained.

It does not represent a diagnosis.

---

## Summary

The summary field provides a concise description of the observed condition.

The summary must:

- reflect available evidence
- avoid unsupported conclusions
- preserve uncertainty

Allowed:

```
Observation data is delayed.
```

Not allowed:

```
The server is down.
```

unless supported by evidence.

---

## Explanation

The explanation field provides additional context.

It may include:

- evidence relationships
- policy interpretation
- relevant timestamps
- additional information required

It must not include fabricated actions.

Allowed:

```
The collector did not provide fresh evidence within the expected interval. Review collector status and gather additional evidence.
```

Not allowed:

```
The collector was restarted successfully.
```

unless evidence confirms that action occurred.

---

## Confidence and Uncertainty

The assistant should communicate evidence limitations.

Supported confidence values:

```
confirmed
bounded
insufficient-evidence
```

### confirmed

Evidence directly supports the statement.

### bounded

The assistant can explain the condition but cannot determine the root cause.

### insufficient-evidence

Available information is not enough to determine current state.

---

## Policy Interpretation

The assistant must distinguish:

```
Finding exists
```

from:

```
Action required
```

A finding does not automatically imply:

- notification
- escalation
- incident declaration
- remediation

Those decisions require supporting policy evidence.

---

## Acceptance Relationship

The interaction contract is validated by the repository-local acceptance framework:

```
fixtures/
responses/
bin/run_acceptance.py
```

The acceptance suite verifies:

- valid interpretations pass
- unsupported interpretations fail
- policy boundaries remain enforced

---

## Future Model Integration

When a model is introduced, it must operate behind this contract.

The model is responsible for generating responses.

The acceptance framework is responsible for determining whether responses remain within approved boundaries.

The model does not become the source of truth.

ChrisOps remains the source of truth.
