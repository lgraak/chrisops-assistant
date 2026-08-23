# ChrisOps Assistant Repository Split

## Purpose

This document records the separation of ChrisOps Assistant from the
homelab-ops repository.

The split creates a dedicated repository for assistant logic while
keeping operational state, infrastructure automation, and ChrisOps
source-of-truth components in homelab-ops.

------------------------------------------------------------------------

## Repository Separation

The repositories now have separate responsibilities.

### homelab-ops

The homelab-ops repository contains the operational plane.

Responsibilities include:

-   infrastructure automation
-   Ansible roles and playbooks
-   ChrisOps state collection
-   operational contracts
-   deployment workflows
-   infrastructure documentation

ChrisOps remains the source of truth for operational state.

------------------------------------------------------------------------

### chrisops-assistant

The chrisops-assistant repository contains the reasoning plane.

Responsibilities include:

-   assistant adapter logic
-   model provider abstraction
-   inference providers
-   assistant behavior contracts
-   acceptance framework
-   response validation
-   model integration testing

The assistant interprets operational evidence. It does not create
operational truth.

------------------------------------------------------------------------

## Architecture Boundary

The relationship between the repositories is:

    homelab-ops

    ChrisOps State
          |
          v
    Operational Evidence
          |
          v


    chrisops-assistant

    Assistant Adapter
          |
          v
    Model Provider
          |
          +----------------+
          |                |
          v                v
    Deterministic      OpenVINO Provider
    Provider                 |
                             v
                      Local Inference Service
          |
          v
    Response Validation
          |
          v
    Acceptance Framework

------------------------------------------------------------------------

## Repository History

The assistant repository was extracted from:

    homelab-ops/tests/chrisops-assistant

using Git history-preserving subtree extraction.

The extracted history was preserved in:

    aeons/chrisops-assistant

This allows continued development without losing the original
development history.

------------------------------------------------------------------------

## Design Principles

The split enforces several boundaries:

-   ChrisOps owns operational truth.
-   The assistant consumes evidence.
-   Models interpret evidence but do not define facts.
-   Providers abstract inference backends.
-   Acceptance tests define acceptable assistant behavior.

------------------------------------------------------------------------

## Future Expansion

The dedicated assistant repository allows future additions without
expanding the operational repository.

Potential future capabilities:

-   model routing
-   multiple specialized models
-   Spark-based inference providers
-   coding-focused models
-   retrieval augmentation
-   additional assistant workflows

The assistant repository can evolve independently while maintaining a
stable contract with ChrisOps.

------------------------------------------------------------------------

## Migration Status

Completed:

-   assistant code extracted
-   assistant history preserved
-   dedicated repository created
-   OpenVINO provider moved with assistant architecture
-   homelab-ops cleaned of assistant implementation code

Remaining future work:

-   continue refining assistant capabilities
-   add model routing when multiple useful models exist
-   maintain repository documentation consistency
