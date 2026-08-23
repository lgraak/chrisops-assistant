# ChrisOps Assistant Provider Configuration Contract v1

## Purpose

This document defines how ChrisOps assistant model providers are
selected, configured, and validated.

The provider configuration determines how response generation is
performed.

Provider configuration does not change the assistant contracts.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Design Principle

A provider is an implementation choice.

Changing providers must not change:

-   evidence boundaries
-   response contracts
-   acceptance rules
-   operational policy interpretation

The acceptance framework remains the final validation boundary.

------------------------------------------------------------------------

## Provider Selection

The assistant adapter selects a provider through configuration.

Example:

``` yaml
provider:
  type: deterministic
  version: v1
```

Future examples:

``` yaml
provider:
  type: openvino
  model: local-model-name
```

``` yaml
provider:
  type: ollama
  model: model-name
```

------------------------------------------------------------------------

## Provider Identity

Every provider execution should have an identifiable configuration.

Provider identity may include:

-   provider type
-   model name
-   model version
-   runtime version
-   configuration revision

Example:

``` json
{
  "provider": "openvino",
  "model": "assistant-model",
  "version": "1.0"
}
```

------------------------------------------------------------------------

## Configuration Boundary

Provider configuration controls:

-   backend selection
-   model selection
-   runtime options
-   resource settings

Provider configuration does not control:

-   source-of-truth data
-   acceptance requirements
-   policy decisions

------------------------------------------------------------------------

## Acceptance Requirements

Every provider must pass the same acceptance suite.

Validation includes:

-   scenario contract compliance
-   prohibited statement checks
-   response schema validation
-   policy boundary validation

A provider producing fluent responses is not sufficient.

Responses must remain within approved behavior.

------------------------------------------------------------------------

## Deterministic Provider

The deterministic provider is the baseline implementation.

Purpose:

-   validate architecture
-   provide repeatable tests
-   verify contracts

The deterministic provider is not intended to represent final assistant
behavior.

------------------------------------------------------------------------

## Future Model Providers

Future providers may include:

-   OpenVINO local inference
-   Ollama-compatible inference
-   API-backed inference

All providers must implement the same provider interface.

The adapter must not contain provider-specific logic.

------------------------------------------------------------------------

## Provider Changes

Changing the provider or model may change response behavior.

Therefore:

1.  provider changes must be identified
2.  acceptance tests must be executed
3.  failures must be reviewed
4.  changes must be documented

The acceptance suite protects against unintended behavior changes.

------------------------------------------------------------------------

## Failure Handling

Provider failures should be represented separately from operational
findings.

Examples:

Provider unavailable:

    The assistant provider is unavailable.

Not:

    The monitored system is unhealthy.

The assistant must not confuse inference failures with infrastructure
state.

------------------------------------------------------------------------

## Future Expansion

Provider configuration may eventually support:

-   model routing
-   fallback providers
-   hardware selection
-   performance profiles
-   specialized models

All expansion must preserve the same contract boundary.

The provider can change.

The contracts remain stable.
