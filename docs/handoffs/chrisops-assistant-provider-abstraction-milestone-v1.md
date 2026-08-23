# ChrisOps Assistant Provider Abstraction Milestone v1

## Purpose

This document records the completion of the ChrisOps assistant provider
abstraction milestone.

The assistant architecture now separates response generation from
provider implementation.

The provider is an implementation detail.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Completed Components

The following components are complete:

-   assistant adapter boundary
-   model provider interface
-   deterministic provider implementation
-   adapter integration with provider interface
-   provider-independent acceptance validation

------------------------------------------------------------------------

## Current Flow

The current execution path is:

    ChrisOps Fixture
            |
            v
    Assistant Adapter
            |
            v
    Model Provider Interface
            |
            v
    Provider Implementation
            |
            v
    Response Envelope
            |
            v
    Response Validation
            |
            v
    Acceptance Result

------------------------------------------------------------------------

## Provider Interface

Location:

    tests/chrisops-assistant/lib/model_provider.py

The provider interface defines how response generation is performed.

Providers are responsible for generating response candidates.

Providers are not responsible for:

-   determining source-of-truth state
-   changing operational data
-   bypassing policy
-   deciding acceptance

------------------------------------------------------------------------

## Current Provider

Current implementation:

    tests/chrisops-assistant/lib/providers/deterministic.py

The deterministic provider exists to validate architecture before
introducing model-based generation.

It provides:

-   repeatable output
-   predictable testing
-   contract validation

------------------------------------------------------------------------

## Adapter Responsibility

The assistant adapter now acts as orchestration.

It is responsible for:

-   receiving approved context
-   invoking a provider
-   returning the provider response

It is not responsible for:

-   generating model-specific output
-   knowing provider implementation details

------------------------------------------------------------------------

## Validation

The following validation paths are complete:

    run_acceptance.py

Validates static acceptance scenarios.

    test_adapter.py

Validates adapter response generation.

    test_adapter_acceptance.py

Validates generated responses against acceptance contracts.

    test_framework.py

Validates framework integrity.

------------------------------------------------------------------------

## Future Providers

Future providers can implement the same interface.

Examples:

-   OpenVINO local inference provider
-   Ollama-compatible provider
-   API-backed provider
-   future model implementations

The adapter and acceptance framework should not change when providers
change.

------------------------------------------------------------------------

## Design Principle

The model generates language.

The acceptance framework defines acceptable behavior.

The provider can change.

The contracts remain stable.

ChrisOps remains the source of truth.
