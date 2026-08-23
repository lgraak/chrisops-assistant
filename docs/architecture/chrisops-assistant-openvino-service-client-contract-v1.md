# ChrisOps Assistant OpenVINO Service Client Contract v1

## Purpose

This document defines the contract between the ChrisOps assistant
OpenVINO provider and an external OpenVINO inference service.

The OpenVINO provider acts as a client boundary.

The provider does not own model lifecycle, hardware allocation, or
operational truth.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Design Principle

The OpenVINO provider is responsible for communication with the
inference service.

It may:

-   construct inference requests
-   send approved assistant context
-   parse inference responses
-   report provider failures

It may not:

-   interpret operational findings
-   modify evidence
-   bypass acceptance validation
-   treat inference failures as infrastructure failures

------------------------------------------------------------------------

## Service Flow

    Assistant Adapter
            |
            v
    OpenVINO Provider
            |
            v
    OpenVINO Service API
            |
            v
    Model Runtime
            |
            v
    Response
            |
            v
    Acceptance Validation

------------------------------------------------------------------------

## Provider Responsibility

The OpenVINO provider handles:

-   service endpoint configuration
-   request serialization
-   response parsing
-   timeout handling
-   service error reporting

The provider does not handle:

-   model selection logic
-   ChrisOps policy interpretation
-   assistant contracts
-   acceptance decisions

------------------------------------------------------------------------

## Request Contract

The provider sends approved assistant context.

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

Only required context should be sent.

Secrets and unrelated operational data must not be included.

------------------------------------------------------------------------

## Response Contract

The service returns a response candidate.

Example:

``` json
{
  "classification": "observation-overdue",
  "summary": "Observation data delayed.",
  "explanation": "The collector did not provide fresh evidence within the expected interval.",
  "confidence": "bounded"
}
```

The response is not trusted until it passes the existing acceptance
framework.

------------------------------------------------------------------------

## Failure Handling

Service failures must remain separate from operational findings.

Examples:

Allowed:

    The assistant inference service is unavailable.

Not allowed:

    The monitored system is unhealthy.

A model service outage does not indicate a ChrisOps finding.

------------------------------------------------------------------------

## Timeout Behavior

The provider should define:

-   request timeout
-   retry behavior
-   failure reporting

Timeouts should produce provider errors.

They should not produce invented operational conclusions.

------------------------------------------------------------------------

## Authentication Boundary

Authentication requirements belong to the service client configuration.

Credentials must not be stored in fixtures or committed source files.

The provider should consume approved runtime configuration.

------------------------------------------------------------------------

## Future Expansion

Future service capabilities may include:

-   streaming responses
-   multiple models
-   model routing
-   performance telemetry
-   hardware-specific optimization

All changes must preserve the provider interface.

The service can change.

The model can change.

The contracts remain stable.
