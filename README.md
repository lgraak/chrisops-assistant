# ChrisOps Assistant

ChrisOps Assistant provides the reasoning and model integration layer
for ChrisOps operational data.

## Purpose

This repository contains:

-   assistant adapter logic
-   model provider abstraction
-   inference providers
-   acceptance framework
-   assistant behavior contracts

ChrisOps provides the approved operational evidence and context consumed
by the assistant.

The assistant interprets evidence. Its output is advisory and never
becomes authoritative system state.

## Repository Ownership

The ChrisOps system is divided across three repositories:

-   `homelab-ops` owns infrastructure intent, desired environment state,
    Ansible automation, and deployment configuration.
-   `chrisops` owns operational runtime state, application behavior, APIs,
    collectors, and product contracts.
-   `chrisops-assistant` owns AI reasoning behavior, model and provider
    contracts, assistant workflows, and the evaluation framework.

The assistant does not replace or override the authority of
`homelab-ops` or `chrisops`.

## Providers

Current providers:

-   deterministic
-   OpenVINO service provider

## Validation

Run:

``` bash
./bin/run_acceptance.py
./bin/test_adapter.py
./bin/test_adapter_acceptance.py
./bin/test_framework.py
```

## Architecture

The assistant uses a layered architecture:

``` text
ChrisOps Evidence
        |
        v
Assistant Adapter
        |
        v
Model Provider Interface
        |
        +----------------+
        |                |
        v                v
Deterministic      OpenVINO Provider
Provider                 |
                         v
                  ai-lab Inference API
        |
        v
Response Validation
        |
        v
Acceptance Framework
```

## Design Principles

-   `homelab-ops` owns infrastructure intent and deployment configuration.
-   `chrisops` owns operational state and product behavior.
-   `chrisops-assistant` owns advisory interpretation and reasoning.
-   Models interpret evidence but do not create facts.
-   Providers abstract inference backends.
-   Acceptance tests define acceptable assistant behavior.

## Future Providers

Additional providers may be added without changing the assistant
contracts.

Examples:

-   Spark-based inference
-   coding-focused models
-   specialized task models
-   future local inference backends
