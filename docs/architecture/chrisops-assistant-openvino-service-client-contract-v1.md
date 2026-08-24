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
-   configured model identity
-   request serialization
-   response parsing
-   timeout handling
-   propagation of service and response errors

The provider does not handle:

-   dynamic model selection or routing
-   model loading or device selection
-   ChrisOps policy interpretation
-   assistant contracts
-   acceptance decisions

------------------------------------------------------------------------

## Request Contract

The provider sends an OpenAI-compatible chat completion request. Contract
instructions are placed in the system message. The approved assistant
context is JSON-serialized into the user message.

Example:

``` json
{
  "model": "qwen3-8b-openvino-gpu",
  "messages": [
    {
      "role": "system",
      "content": "Assistant response-contract instructions"
    },
    {
      "role": "user",
      "content": "{\"classification\": \"observation-overdue\", \"facts\": {\"asset_id\": \"ansible\", \"collector\": \"proxmox\", \"age_seconds\": 1482}}"
    }
  ],
  "max_tokens": 256,
  "temperature": 0.2,
  "stream": false,
  "enable_thinking": false
}
```

Only required context should be sent.

Secrets and unrelated operational data must not be included.

------------------------------------------------------------------------

## Response Contract

The service returns an OpenAI-compatible response. The response candidate
is a JSON string in `choices[0].message.content`.

Example:

``` json
{
  "id": "chatcmpl-local-openvino-1",
  "object": "chat.completion",
  "model": "qwen3-8b-openvino-gpu",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "{\"classification\":\"observation-overdue\",\"summary\":\"Observation data delayed.\",\"explanation\":\"The collector did not provide fresh evidence within the expected interval.\",\"confidence\":\"bounded\"}"
      },
      "finish_reason": "stop"
    }
  ]
}
```

The provider parses and normalizes the candidate into the assistant
response envelope. The normalized response is not trusted until it passes
the existing acceptance framework.

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

The provider uses the configured `timeout_seconds` value for the service
request. The current implementation does not retry automatically.

Timeout, HTTP, malformed-envelope, and invalid model-content errors
propagate to the caller as client or parsing exceptions.

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
