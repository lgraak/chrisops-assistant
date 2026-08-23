# ChrisOps Assistant OpenVINO Provider Contract v1

## Purpose

This document defines the contract for the OpenVINO-backed inference
provider used by the ChrisOps assistant architecture.

The OpenVINO provider is an implementation of the existing model
provider interface.

It does not change assistant contracts, acceptance rules, or operational
truth boundaries.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Design Principle

The OpenVINO provider is responsible for model execution.

It may:

-   load an approved model
-   execute inference
-   manage runtime interaction
-   return generated response candidates

It may not:

-   interpret operational truth independently
-   modify ChrisOps evidence
-   bypass acceptance validation
-   convert inference uncertainty into operational certainty

------------------------------------------------------------------------

## Provider Position

The OpenVINO provider exists behind the model provider interface.

Flow:

    Assistant Adapter
            |
            v
    Model Provider Interface
            |
            v
    OpenVINO Provider
            |
            v
    OpenVINO Runtime
            |
            v
    Response Candidate

The adapter does not contain OpenVINO-specific logic.

------------------------------------------------------------------------

## Configuration

OpenVINO configuration should define:

-   provider type
-   model location
-   model identity
-   device selection
-   runtime options

Example:

``` yaml
provider:
  type: openvino
  model_path: /path/to/model
  device: GPU
```

Configuration changes must be reviewable.

------------------------------------------------------------------------

## Model Identity

Models must have identifiable versions.

Model identity may include:

-   model name
-   model version
-   quantization format
-   runtime compatibility
-   deployment revision

A model change may affect assistant behavior.

Model changes require acceptance validation.

------------------------------------------------------------------------

## Device Selection

Device selection is an implementation detail.

Possible targets may include:

-   CPU
-   integrated GPU
-   discrete GPU
-   other supported accelerators

The provider must expose device configuration without changing the
adapter contract.

------------------------------------------------------------------------

## Failure Handling

Inference failures must remain separate from operational findings.

Allowed:

    The assistant inference provider is unavailable.

Not allowed:

    The monitored asset is unhealthy.

A provider failure does not indicate a ChrisOps state failure.

------------------------------------------------------------------------

## Acceptance Requirement

The OpenVINO provider must pass the existing acceptance framework.

Validation includes:

-   response contract compliance
-   prohibited statement checks
-   scenario acceptance
-   policy boundary enforcement

The provider is accepted based on behavior, not only successful
inference.

------------------------------------------------------------------------

## Initial Implementation Scope

The first OpenVINO provider implementation should:

-   satisfy the ModelProvider interface
-   execute a configured model
-   return a response envelope
-   preserve existing acceptance behavior

The first implementation should not add:

-   new contracts
-   new validation paths
-   provider-specific assistant logic

------------------------------------------------------------------------

## Future Expansion

Future OpenVINO provider improvements may include:

-   streaming output
-   batching
-   hardware optimization
-   model lifecycle management
-   performance telemetry

All improvements must preserve the provider boundary.

The runtime can change.

The model can change.

The contracts remain stable.
