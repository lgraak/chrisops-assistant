# ChrisOps Assistant Repository Split

## Purpose

This document records the separation of ChrisOps Assistant from the
homelab-ops repository.

That extraction is historical context. Current ownership follows a
three-repository architecture separating infrastructure intent, ChrisOps
runtime and product behavior, and assistant reasoning.

------------------------------------------------------------------------

## Repository Separation

The three repositories have separate current responsibilities.

### homelab-ops

The homelab-ops repository contains infrastructure intent and deployment
configuration.

Responsibilities include:

-   infrastructure automation
-   Ansible roles and playbooks
-   desired environment state
-   deployment configuration and workflows
-   infrastructure documentation

It does not own ChrisOps application behavior, collectors, APIs, or
assistant reasoning.

------------------------------------------------------------------------

### chrisops

The chrisops repository contains the operational control plane and
application behavior.

Responsibilities include:

-   operational runtime state
-   application and controller behavior
-   APIs
-   collectors and evidence processing
-   product contracts
-   operational workflows and presentation

It consumes infrastructure intent and deployment context from
homelab-ops and provides approved operational evidence to the assistant.

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
operational truth. Its output is advisory and never becomes authoritative
system state.

------------------------------------------------------------------------

## Architecture Boundary

The current relationship between the repositories is:

    homelab-ops

    Infrastructure Intent
    Desired Environment State
    Ansible and Deployment Configuration
          |
          v
    Managed Infrastructure
    Observed Runtime State
          |
          v


    chrisops

    Collectors and Evidence Processing
          |
          v
    Operational State, APIs, and Product Contracts
          |
          v
    Approved Evidence and Context
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

-   homelab-ops owns infrastructure intent and deployment configuration.
-   chrisops owns operational state and product behavior.
-   chrisops-assistant owns reasoning behavior and evaluation.
-   The assistant consumes evidence.
-   Models interpret evidence but do not define facts.
-   Assistant output is advisory and never authoritative system state.
-   Providers abstract inference backends.
-   Acceptance tests define acceptable assistant behavior.

------------------------------------------------------------------------

## Future Expansion

The dedicated assistant repository allows future additions without
expanding infrastructure or ChrisOps application ownership.

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
