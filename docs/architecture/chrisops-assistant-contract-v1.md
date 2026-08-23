# ChrisOps Assistant Contract v1

## Purpose

The ChrisOps assistant boundary provides a read-only interface between AI clients and the ChrisOps operational state system.

The assistant does not collect data, modify state, execute automation, or access collectors directly.

## Data Flow

AI Client

↓

ChrisOps Assistant Adapter

↓

ChrisOps State API

↓

Authoritative ChrisOps State

## Allowed Operations

The assistant may:

- query current operational state
- summarize findings
- explain asset status
- provide context from approved ChrisOps state

## Forbidden Operations

The assistant must not:

- modify ChrisOps state
- execute Ansible actions
- access collectors directly
- alter observations
- acknowledge findings automatically
- change policy

## Authentication

The assistant uses the dedicated state-query bearer token.

Authentication is handled by:

/etc/chrisops/state-query-token

## Current Interface

Endpoint:

/v1/status

Source:

chrisops-state-api

## Current Implementation

Binary:

/opt/chrisops-assistant/bin/chrisops-assistant-query

The initial implementation provides a reduced operational summary.

## Future Expansion

Future versions may add:

- natural language query translation
- finding explanations
- asset context retrieval
- RAG grounding
- operator-approved workflows

Automation remains outside the assistant boundary.
