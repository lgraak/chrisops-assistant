# ChrisOps Assistant Provider Selection Milestone v1

## Purpose

This document records the completion of the ChrisOps assistant provider
selection milestone.

The assistant architecture now supports configuration-driven provider
selection.

The provider implementation can change without changing the assistant
adapter or acceptance framework.

ChrisOps remains the source of truth.

------------------------------------------------------------------------

## Completed Components

The following components are complete:

-   model provider interface
-   deterministic provider implementation
-   provider factory
-   provider configuration
-   adapter integration with provider selection
-   provider-independent acceptance testing

------------------------------------------------------------------------

## Current Flow

The current execution path is:

    Provider Configuration
            |
            v
    Provider Factory
            |
            v
    Model Provider
            |
            v
    Assistant Adapter
            |
            v
    Response Validation
            |
            v
    Acceptance Framework

------------------------------------------------------------------------

## Provider Configuration

Location:

    tests/chrisops-assistant/config/provider.yml

The configuration determines which provider implementation is selected.

Example:

``` yaml
provider:
  type: deterministic
```

The adapter does not directly select providers.

------------------------------------------------------------------------

## Provider Factory

Location:

    tests/chrisops-assistant/lib/provider_factory.py

The factory translates configuration into provider implementations.

The factory is the only component that knows concrete provider classes.

------------------------------------------------------------------------

## Current Provider

Current implementation:

    tests/chrisops-assistant/lib/providers/deterministic.py

The deterministic provider provides:

-   repeatable responses
-   predictable testing behavior
-   contract validation

It is the baseline provider.

------------------------------------------------------------------------

## Adapter Boundary

The assistant adapter receives a provider.

The adapter is responsible for:

-   orchestration
-   passing approved context
-   returning provider output

The adapter is not responsible for:

-   provider selection
-   model implementation details
-   inference logic

------------------------------------------------------------------------

## Validation

All providers must pass the same validation path.

Current checks:

    run_acceptance.py

Static acceptance validation.

    test_adapter.py

Adapter generation validation.

    test_adapter_acceptance.py

Generated response contract validation.

    test_framework.py

Framework integrity validation.

------------------------------------------------------------------------

## Adding Future Providers

Future providers should only require:

1.  Provider implementation.
2.  Factory registration.
3.  Configuration entry.
4.  Acceptance validation.

The following components should not change:

-   AssistantAdapter
-   response validation
-   acceptance framework
-   scenario contracts

------------------------------------------------------------------------

## Next Provider

The next planned provider is a local inference provider.

Candidate implementations:

-   OpenVINO provider
-   Ollama-compatible provider
-   other local inference backends

The first real provider should validate the architecture while
preserving the existing acceptance boundaries.

------------------------------------------------------------------------

## Design Principle

The provider can change.

The model can change.

The hardware can change.

The contracts remain stable.

ChrisOps remains the source of truth.
