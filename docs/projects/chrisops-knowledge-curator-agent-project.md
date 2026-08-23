# ChrisOps Knowledge Curator Agent Project

## Status

Planned / Future Project

Do not start during the repository split effort.

This project should begin after the ChrisOps, homelab-ops, and
chrisops-assistant boundaries are stable.

------------------------------------------------------------------------

## Purpose

Create a knowledge curation workflow for ChrisOps-related RAG data.

The goal is to prevent the knowledge base from becoming stale,
duplicated, contradictory, or difficult for AI systems to reason over.

The curator should help maintain knowledge quality without allowing AI
systems to silently change source-of-truth documents.

------------------------------------------------------------------------

## Problem Statement

As the documentation and knowledge base grow, several issues will
appear:

-   duplicate documents covering the same topic
-   outdated handoff documents
-   historical decisions mixed with current architecture
-   conflicting statements between documents
-   stale implementation details
-   unclear ownership of information

The goal is to create a process for identifying and managing these
issues.

------------------------------------------------------------------------

## Proposed Architecture

The knowledge curator should operate as an assistant over the knowledge
lifecycle.

    Documentation Repositories
              |
              v
    Knowledge Ingestion
              |
              v
    Knowledge Curator Agent
              |
              +----------------+
              |                |
              v                v
     Document Analysis    Metadata Management
              |
              v
     Recommendations
              |
              v
     Human Approval
              |
              v
     RAG Index Update

------------------------------------------------------------------------

## Core Principles

The curator agent must:

-   recommend changes, not silently modify truth
-   preserve source repositories as authoritative
-   distinguish active documents from historical documents
-   identify uncertainty and conflicts
-   require human approval for destructive changes

The workflow should follow:

    Observe
      |
    Analyze
      |
    Recommend
      |
    Approve
      |
    Apply

------------------------------------------------------------------------

## Initial Capabilities

### Duplicate Detection

Identify documents with overlapping content.

Examples:

-   multiple architecture documents describing the same system
-   old handoffs that are superseded
-   repeated implementation notes

Output:

-   similarity analysis
-   recommendation to merge/archive/retain

------------------------------------------------------------------------

### Staleness Detection

Identify documents that reference outdated systems.

Examples:

-   retired Kubernetes references
-   old deployment methods
-   removed services
-   obsolete architecture decisions

Output:

-   affected documents
-   suspected stale sections
-   recommended action

------------------------------------------------------------------------

### Contradiction Detection

Identify conflicting statements.

Examples:

-   different source-of-truth definitions
-   conflicting deployment instructions
-   outdated ownership models

Output:

-   conflicting documents
-   conflicting statements
-   human review required

------------------------------------------------------------------------

### RAG Summary Generation

Generate structured summaries for retrieval.

Possible output:

``` markdown
Purpose:
Defines repository ownership.

Key facts:
- homelab-ops owns infrastructure truth
- ChrisOps owns operational interpretation
- chrisops-assistant consumes evidence

Boundaries:
- assistant does not modify infrastructure
```

------------------------------------------------------------------------

## Future Metadata Model

Documents should eventually include metadata.

Example:

``` yaml
---
title: ChrisOps Assistant Provider Selection
domain: chrisops-assistant
type: architecture
status: active
stability: stable
created: 2026-08-23
supersedes:
  - previous-document.md
---
```

Potential metadata fields:

-   domain
-   document type
-   status
-   stability
-   ownership
-   creation date
-   superseded documents

------------------------------------------------------------------------

## Potential Repository Location

Likely location:

    chrisops-assistant

Possible structure:

    agents/
      knowledge-curator/

    rag/
      ingestion/
      indexing/
      metadata/

    docs/
      knowledge-management/

The curator belongs with the assistant ecosystem because it manages AI
knowledge quality, not infrastructure state.

------------------------------------------------------------------------

## Future Tasks

-   [ ] Define document metadata standard
-   [ ] Add document lifecycle states
-   [ ] Create duplicate detection workflow
-   [ ] Create stale document detection workflow
-   [ ] Create contradiction detection workflow
-   [ ] Create RAG summary generation workflow
-   [ ] Define human approval workflow
-   [ ] Integrate with assistant knowledge ingestion
-   [ ] Add acceptance tests for curator behavior

------------------------------------------------------------------------

## Notes

This project should remain separate from repository split work.

Current priority:

1.  Complete repository split.
2.  Stabilize ownership boundaries.
3.  Update repository documentation.
4.  Return to knowledge lifecycle automation.
