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

The repository entry points load the `provider` mapping from:

    config/provider.yml

The provider factory translates that mapping into a provider instance and
injects the instance into the assistant adapter. The adapter does not load
configuration or select a concrete provider.

The current deterministic configuration is:

``` yaml
provider:
  type: deterministic
```

The current factory also supports the service-backed OpenVINO provider:

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
telemetry:
  persistence_enabled: false
  database_path: /var/lib/chrisops/inference/inference.sqlite3
```

`config/provider-openvino.yml` records this OpenVINO configuration as an
alternate example. The current entry points do not select that file
automatically; they read `config/provider.yml`.

An Ollama-compatible provider is not currently implemented. A future
configuration may use:

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
-   service endpoint and request timeout for service-backed providers
-   safe telemetry aliases and the externally installed schema path
-   optional provider credential-file reference
-   persistence enablement and database path

Provider configuration does not control:

-   source-of-truth data
-   acceptance requirements
-   policy decisions

The production configuration is rendered by homelab-ops; product source
contains no private endpoint or credential. The deployed workflow also has a
separate runtime.workflow_enabled activation gate. Both workflow and telemetry
persistence remain disabled before M5B.

When persistence is enabled, configuration constructs
InferenceRunStore(require_existing=True). Ordinary assistant requests
therefore cannot create or migrate the database. M5B must initialize and verify
schema version 4 explicitly before enabling the workflow.

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

## Supported and Future Model Providers

The current factory supports:

-   deterministic response generation
-   OpenVINO service-backed inference

Future providers may include:

-   Ollama-compatible inference
-   other API-backed inference

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
