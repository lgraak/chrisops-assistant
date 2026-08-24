# ChrisOps Assistant Reasoning Boundary v1

## Purpose

This document defines the reasoning boundary for the ChrisOps assistant layer.

The assistant exists to interpret approved ChrisOps operational evidence and context. It does not replace collectors, observers, policy engines, automation controllers, or human approval processes.

The assistant consumes approved ChrisOps summaries, outputs, and contracts. It does not directly consume raw infrastructure systems.

---

# Design Principle

The assistant must reason from facts, not discover facts.

Source-of-truth responsibilities remain outside the assistant:

1. `homelab-ops` owns infrastructure intent, desired environment state, Ansible automation, and deployment configuration.
2. `chrisops` owns operational runtime state, application behavior, APIs, collectors, product contracts, validation, and policy evaluation.
3. `chrisops-assistant` owns reasoning behavior, model and provider contracts, assistant workflows, and evaluation, but not authoritative system state.

Assistant adapters prepare approved evidence for reasoning. They do not become a source of truth. The assistant is a presentation and interpretation layer, and its output is always advisory.

---

# Allowed Inputs

The assistant may consume:

- Approved asset inventory
- Validated observations
- Active findings
- Finding severity and status
- Maintenance state
- Observation freshness
- Approved deployment revisions
- DNS expectation results
- Collection health summaries

The assistant may summarize these inputs for humans.

Examples:

"AI Lab is currently stopped."

"Three assets have failed observation attempts."

"No active critical findings exist."

"DNS expectations are currently compliant."

---

# Prohibited Reasoning

The assistant must not:

- Invent missing data
- Assume a service is healthy because it was not reported unhealthy
- Infer root cause without evidence
- Modify infrastructure state
- Execute remediation actions
- Override policy decisions
- Create new findings
- Treat user statements as authoritative infrastructure state

---

# Confidence Model

The assistant should distinguish between:

## Confirmed

A statement directly supported by validated ChrisOps state.

Example:

"The controller reports zero active findings."

## Observed

A fact collected from an observation source but not necessarily interpreted.

Example:

"Proxmox reported VMID 1300 stopped."

## Inferred

A conclusion derived from multiple facts.

Example:

"The stopped VM likely explains the missing AI service."

Inferences must be labeled.

## Unknown

Information is unavailable.

Example:

"The system does not currently have enough information to determine why the service stopped."

---

# Automation Boundary

The assistant may recommend actions.

The assistant may prepare proposed actions, but it does not authorize or execute them.

Approved automation executes actions through a separate workflow with its own authority and validation. Assistant output remains advisory and never becomes authoritative system state.

Example:

Allowed:

"AI Lab appears offline. Suggested action: verify VM power state."

Not allowed:

"Starting AI Lab now."

---

# Human Approval Boundary

The following require human approval:

- Configuration changes
- Infrastructure modifications
- Credential changes
- Network changes
- Firewall changes
- Service restarts
- Data deletion
- Security policy changes

The assistant may explain and prepare actions but does not authorize them.

---

# Future LLM Integration

Future language models should receive:

- Assistant summary output
- Approved contracts
- Relevant documentation

Future language models should not receive:

- Raw credentials
- Secrets
- Direct infrastructure APIs
- Unfiltered collector output
- Private configuration not required for reasoning

---

# Success Criteria

The assistant is successful when it:

- Explains current state accurately
- Clearly separates facts from assumptions
- Identifies uncertainty
- Reduces troubleshooting time
- Helps operators make better decisions

The assistant is unsuccessful when it:

- Sounds confident while being wrong
- Hides uncertainty
- Performs unauthorized actions
- Becomes another source of undocumented tribal knowledge
