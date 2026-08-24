# ChrisOps Assistant OpenVINO API Contract v1

## Purpose

This document defines the API contract between the ChrisOps assistant
OpenVINO provider and the ai-lab OpenVINO inference service.

The OpenVINO provider consumes a model service.

It does not manage model lifecycle, hardware allocation, or operational
truth.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Service Identity

Current inference service:

    ai-lab OpenVINO FastAPI service

Base endpoint:

    http://192.168.20.70:8000

The service exposes an OpenAI-compatible chat completion interface.

------------------------------------------------------------------------

## Available Endpoints

Current supported endpoints:

    GET /health
    GET /status
    GET /v1/models
    POST /v1/chat/completions

The current assistant provider uses:

    POST /v1/chat/completions

The other endpoints are service capabilities used for operational
inspection and validation; the current provider client does not call them.

------------------------------------------------------------------------

## Model Identity

Current available model:

    qwen3-8b-openvino-gpu

Model response:

``` json
{
  "id": "qwen3-8b-openvino-gpu",
  "object": "model",
  "owned_by": "local-openvino"
}
```

Model identity must be configurable.

------------------------------------------------------------------------

## Chat Completion Request

The provider sends an OpenAI-compatible request.

Example:

``` json
{
  "model": "qwen3-8b-openvino-gpu",
  "messages": [
    {
      "role": "system",
      "content": "You are a ChrisOps assistant."
    },
    {
      "role": "user",
      "content": "Explain this evidence."
    }
  ],
  "max_tokens": 256,
  "temperature": 0.2,
  "stream": false,
  "enable_thinking": false
}
```

------------------------------------------------------------------------

## Context Boundary

The provider only sends approved assistant context.

The provider must not send:

-   secrets
-   credentials
-   unrelated operational data
-   raw system data outside the approved fixture/context

The model receives evidence, not authority.

------------------------------------------------------------------------

## Response Normalization

For a non-streaming request, the service returns an OpenAI-compatible chat
completion envelope. The generated model text is contained in
`choices[0].message.content`:

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

The provider parses the JSON object in `message.content` and normalizes it
into the assistant response envelope.

Expected output:

``` json
{
  "classification": "observation-overdue",
  "summary": "Observation data delayed.",
  "explanation": "The collector did not provide fresh evidence within the expected interval.",
  "confidence": "bounded"
}
```

The acceptance framework validates this normalized response.

------------------------------------------------------------------------

## Failure Handling

Inference failures must remain separate from operational state.

Examples:

Allowed:

    The assistant inference service is unavailable.

Not allowed:

    The monitored system is unhealthy.

A model service failure is not a ChrisOps finding.

------------------------------------------------------------------------

## Runtime Configuration

The provider configuration should include:

-   service endpoint
-   model identifier
-   timeout
-   generation parameters

Example:

``` yaml
provider:
  type: openvino
  endpoint: http://192.168.20.70:8000
  model: qwen3-8b-openvino-gpu
  timeout_seconds: 30
```

------------------------------------------------------------------------

## Acceptance Requirement

The OpenVINO provider must pass the existing acceptance framework.

The provider is evaluated on:

-   response contract compliance
-   evidence boundaries
-   prohibited statement handling
-   policy interpretation

The model is replaceable.

The contracts are not.

------------------------------------------------------------------------

## Future Expansion

Future API capabilities may include:

-   streaming responses
-   additional models
-   model routing
-   performance metrics
-   authentication

All changes must preserve the provider boundary.

The service can change.

The model can change.

The contracts remain stable.
