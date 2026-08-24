# ChrisOps Assistant OpenVINO Provider Contract v1

## Purpose

This document defines the contract for the service-backed OpenVINO
inference provider used by the ChrisOps assistant architecture.

The OpenVINO provider is an implementation of the existing model
provider interface.

It does not change assistant contracts, acceptance rules, or operational
truth boundaries.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Design Principle

The OpenVINO provider is responsible for invoking model execution through
the configured ai-lab OpenVINO service.

It may:

-   construct requests for an approved model identity
-   send approved assistant context to the inference service
-   manage service interaction
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
    OpenVINO Service API
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
-   service endpoint
-   model identity
-   request timeout

Example:

``` yaml
provider:
  type: openvino
  endpoint: http://192.168.20.70:8000
  model: qwen3-8b-openvino-gpu
  timeout_seconds: 30
```

Configuration changes must be reviewable.

------------------------------------------------------------------------

## Model Identity

The provider sends a configured model identifier to the service.

The service owns the loaded model artifact and must reject a requested
identifier that does not match the loaded model.

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

Device selection is an implementation detail of the external OpenVINO
service, not the assistant provider client.

Possible targets may include:

-   CPU
-   integrated GPU
-   discrete GPU
-   other supported accelerators

Changing service-side device selection must not change the adapter or
model-provider contract.

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

## Current Implementation Scope

The current OpenVINO provider implementation:

-   satisfy the ModelProvider interface
-   call a configured OpenAI-compatible service endpoint
-   request a configured model identifier
-   return a response envelope
-   preserve existing acceptance behavior

The implementation does not add:

-   new contracts
-   new validation paths
-   provider-specific assistant logic

------------------------------------------------------------------------

## Future Expansion

Future OpenVINO provider improvements may include:

-   streaming output
-   additional generation controls
-   client-side performance telemetry
-   service authentication

All improvements must preserve the provider boundary.

The runtime can change.

The model can change.

The contracts remain stable.
