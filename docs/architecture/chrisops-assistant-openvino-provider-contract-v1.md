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
    ChrisOps InstrumentedA60Client
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
-   safe endpoint, model, workload, hardware, and serving-engine aliases
-   ChrisOps inference schema path
-   request timeout
-   optional credential-file reference

Example:

``` yaml
provider:
  type: openvino
  endpoint: https://a60.example.invalid/v1/chat/completions
  endpoint_alias: a60-private
  model: qwen3-8b-openvino-gpu
  workload_id: chrisops-assistant
  hardware_alias: intel-arc-pro-a60
  serving_engine: openvino
  schema_path: /opt/chrisops-source/state/schemas/inference-run-v1.schema.json
  timeout_seconds: 30
```

The example endpoint is deliberately non-routable. Environment-specific
endpoint and credential references are owned by homelab-ops.
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

-   satisfies the ModelProvider.invoke() interface
-   builds the existing system/user prompt and bounded generation options
-   invokes the accepted ChrisOps InstrumentedA60Client
-   receives generated content plus one schema-valid terminal run
-   translates generated JSON back to the existing assistant response
-   returns provider failure categories separately from operational findings
-   preserve existing acceptance behavior

The provider never writes SQLite. The assistant adapter owns exactly one
optional InferenceRunStore.write_run() call after terminal normalization.

The implementation does not add:

-   new contracts
-   new validation paths
-   provider-specific database logic

------------------------------------------------------------------------

## Future Expansion

Future OpenVINO provider improvements may include:

-   streaming output
-   additional generation controls
-   additional accepted telemetry fields
-   service authentication

All improvements must preserve the provider boundary.

The runtime can change.

The model can change.

The contracts remain stable.
