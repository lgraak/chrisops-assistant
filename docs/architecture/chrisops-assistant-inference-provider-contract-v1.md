# ChrisOps Assistant Inference Provider Contract v1

## Purpose

This document defines the contract for inference-backed model providers
used by the ChrisOps assistant architecture.

The inference provider is responsible for model execution.

It is not responsible for operational truth, policy decisions, or
acceptance decisions.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Design Principle

The inference provider is an execution component.

It may:

-   load and execute a model
-   receive approved assistant context
-   generate response candidates
-   report inference metadata

It may not:

-   modify source evidence
-   determine operational state
-   bypass acceptance validation
-   convert uncertainty into certainty

------------------------------------------------------------------------

## Inference Flow

    ChrisOps Evidence
            |
            v
    Assistant Adapter
            |
            v
    Inference Provider
            |
            v
    Model Runtime
            |
            v
    Response Candidate
            |
            v
    Acceptance Validation

------------------------------------------------------------------------

## Provider Responsibility

An inference provider is responsible for:

-   model loading
-   runtime interaction
-   device selection
-   inference execution
-   returning generated output

The provider is not responsible for:

-   interpreting ChrisOps findings
-   deciding remediation
-   deciding escalation
-   changing assistant contracts

------------------------------------------------------------------------

## Input Boundary

The provider receives only approved assistant context.

The context should contain information required for the response task.

Example:

``` json
{
  "classification": "observation-overdue",
  "facts": {
    "asset_id": "ansible",
    "collector": "proxmox",
    "age_seconds": 1482
  }
}
```

The provider must not receive unrelated secrets or unnecessary
operational data.

------------------------------------------------------------------------

## Output Boundary

The provider returns a response candidate.

The output must be processed by the existing response validation layer.

A fluent response is not automatically a valid response.

Validation remains authoritative.

------------------------------------------------------------------------

## Runtime Selection

Inference providers may support different runtimes.

Examples:

-   OpenVINO
-   Ollama-compatible runtimes
-   other local inference backends

Runtime selection must remain behind the provider interface.

The assistant adapter must not contain runtime-specific logic.

------------------------------------------------------------------------

## OpenVINO Provider Expectations

An OpenVINO provider should:

-   use the existing ModelProvider interface
-   expose model execution through generate()
-   keep device selection configurable
-   report inference failures separately from operational findings

Example failure:

Allowed:

    The assistant inference provider is unavailable.

Not allowed:

    The monitored asset is unhealthy.

An inference failure is not an infrastructure finding.

------------------------------------------------------------------------

## Hardware Boundary

Hardware acceleration is an implementation detail.

Possible targets may include:

-   CPU inference
-   integrated accelerators
-   discrete GPUs
-   future accelerator hardware

The provider contract remains unchanged.

------------------------------------------------------------------------

## Acceptance Requirement

Every inference provider must pass the existing acceptance framework.

Validation includes:

-   response contract compliance
-   prohibited statement detection
-   scenario acceptance
-   policy boundary checks

A new model or runtime is accepted only after it demonstrates equivalent
contract behavior.

------------------------------------------------------------------------

## Future Expansion

Future inference providers may add:

-   streaming responses
-   batching
-   model routing
-   specialized models
-   retrieval augmentation support

All additions must preserve the provider boundary.

The model can change.

The runtime can change.

The contracts remain stable.
