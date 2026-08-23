# ChrisOps Assistant Acceptance Runner v1

## Purpose

The acceptance runner validates that assistant behavior follows the ChrisOps reasoning boundary.

The runner does not evaluate whether a response is intelligent.

The runner evaluates whether a response violates architectural constraints.

---

# Validation Scope

The runner checks:

- Facts remain traceable to source state
- Unknown states are not converted into failures
- Recommendations are not represented as completed actions
- Root causes are not invented
- Production state is not modified

---

# Test Input

Each acceptance test contains:

- Fixture identifier
- Source facts
- Expected allowed statements
- Prohibited statements

Example:
fixture:
  id: missing-observation
facts:
  asset: example-host
  observation_state: unavailable
allowed:
- "state cannot be confirmed"
prohibited:
- "host is offline"

---

# Pass Conditions

A fixture passes when:

- No prohibited statement appears
- Required facts are represented
- Output classification matches expected behavior

---

# Failure Conditions

A fixture fails when:

- Assistant claims unsupported facts
- Assistant claims actions completed without execution
- Assistant treats missing data as failure
- Assistant exceeds available evidence

---

# Future Integration

The acceptance runner may later execute against:

- local models
- OpenAI API models
- other inference engines

The acceptance contract remains independent of the model provider.
