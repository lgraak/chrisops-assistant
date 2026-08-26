# ChrisOps Assistant Adapter Contract v1

## Purpose

This document defines the contract between the ChrisOps assistant
adapter and the acceptance framework.

The adapter provides the boundary between operational evidence and
assistant-generated responses.

The adapter is responsible for transforming approved input evidence into
a response format that can be evaluated by the acceptance system.

The adapter does not replace ChrisOps state evaluation and does not
become a source of truth.

------------------------------------------------------------------------

## Design Principle

The assistant adapter is an execution boundary.

It may:

-   receive approved evidence
-   provide structured context to a model
-   produce a response envelope
-   preserve evidence limitations
-   persist one content-free terminal InferenceResult.run through the
    configured ChrisOps store

It may not:

-   modify source evidence
-   invent operational facts
-   bypass acceptance validation
-   claim actions that did not occur

------------------------------------------------------------------------

## Adapter Flow

    ChrisOps State
          |
          v
    State Fixture
          |
          v
    Assistant Adapter
          |
          +--> optional terminal telemetry persistence
          |
          v
    Assistant Response
          |
          v
    Acceptance Evaluator

------------------------------------------------------------------------

## Input Contract

The adapter receives structured evidence.

Example:

``` json
{
  "id": "observation-overdue",
  "facts": {
    "asset_id": "ansible",
    "finding_type": "observation_overdue"
  }
}
```

The adapter must treat the input as evidence only.

------------------------------------------------------------------------

## Output Contract

The adapter produces a structured response.

Example:

``` json
{
  "classification": "observation-overdue",
  "summary": "Observation data is delayed.",
  "confidence": "bounded"
}
```

The response shape remains unchanged when persistence succeeds or is disabled.
When inference succeeds and persistence fails, the adapter raises a bounded
telemetry-persistence exception that retains the generated response for the
owning caller. It never exposes a database exception or path.

When provider inference fails, that provider category remains primary. A
simultaneous persistence failure is represented separately by the bounded
persistence_status value and does not replace the provider failure.

The adapter is the only persistence owner. Provider clients return
InferenceResult and do not call write_run().

------------------------------------------------------------------------

## Model Boundary

A future language model operates inside the adapter boundary.

The model may generate wording.

The adapter and acceptance framework define what is acceptable.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Acceptance Integration

Adapter outputs are valid only when they satisfy the acceptance
framework.

Validation includes:

-   scenario contract compliance
-   prohibited statement detection
-   expected outcome matching
-   policy boundary enforcement
