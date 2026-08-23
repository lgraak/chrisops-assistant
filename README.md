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

ChrisOps remains the source of truth for operational state.

The assistant interprets evidence. It does not create operational truth.

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

-   ChrisOps owns operational truth.
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
