# ChrisOps Assistant Model Provider Contract v1

## Purpose

This document defines the contract between the ChrisOps assistant
adapter and the underlying model provider.

The purpose of this contract is to allow different model implementations
without changing the assistant architecture or acceptance boundaries.

The model is an implementation detail.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Design Principle

The assistant architecture separates:

-   operational evidence
-   assistant orchestration
-   model generation
-   response validation

The model generates language.

The acceptance framework determines whether the result is acceptable.

------------------------------------------------------------------------

## Provider Flow

    ChrisOps Fixture
            |
            v
    Assistant Adapter
            |
            v
    Model Provider Interface
            |
            +--> Local Model
            |
            +--> Remote Model
            |
            +--> Rule Based Provider
            |
            v
    Response Envelope
            |
            v
    Acceptance Validation

------------------------------------------------------------------------

## Model Provider Responsibility

A model provider is responsible for:

-   receiving approved context
-   generating a response candidate
-   returning structured output
-   returning the terminal ChrisOps InferenceResult when it uses an
    instrumented provider

A model provider is not responsible for:

-   determining source-of-truth state
-   changing operational data
-   bypassing policy
-   deciding acceptance

------------------------------------------------------------------------

## Input Contract

The provider receives only approved assistant context.

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

The provider must not receive unrelated secrets or operational data that
are not required for the task.

------------------------------------------------------------------------

## Output Contract

The provider returns a response candidate.

Example:

``` json
{
  "classification": "observation-overdue",
  "summary": "Observation data delayed.",
  "explanation": "The collector did not provide fresh evidence within the expected interval.",
  "confidence": "bounded"
}
```

The response is not trusted until it passes acceptance validation.

------------------------------------------------------------------------

## Provider Abstraction

All providers must implement the same conceptual interface.

Example:

``` python
class ModelProvider:
    def invoke(self, context):
        pass
```

Implementations may include:

-   deterministic test provider
-   local inference provider
-   API-backed provider
-   future providers

The adapter should not depend on a specific implementation. Instrumented
providers return a provider invocation containing the translated response,
terminal telemetry result, and a bounded provider error category when
applicable. The adapter owns persistence and unwraps the normal response for
existing callers.

------------------------------------------------------------------------

## Validation Boundary

The model provider output must pass:

-   response schema validation
-   prohibited statement checks
-   acceptance scenario checks
-   policy boundary checks

A fluent response is not necessarily a correct response.

------------------------------------------------------------------------

## Local Model Integration

Initial model integrations should prefer a controlled local provider.

Potential providers may include:

-   local inference services
-   OpenVINO-backed models
-   Ollama-compatible backends
-   future hardware-specific deployments

The provider contract remains unchanged.

------------------------------------------------------------------------

## Future Expansion

Future capabilities may include:

-   retrieval augmentation
-   conversation memory
-   tool calling
-   multi-step reasoning

These capabilities must remain behind the adapter boundary.

The acceptance framework remains the final guardrail.
