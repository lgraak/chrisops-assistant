# ChrisOps Assistant Summary Adapter Contract v1

## Purpose

The ChrisOps assistant summary adapter is the deterministic
interpretation layer between the authoritative ChrisOps state query API
and future conversational interfaces.

The adapter does not collect state, modify state, or make operational
decisions. It translates verified ChrisOps state into an
operator-oriented summary.

Architecture boundary:

    ChrisOps State API
            |
            v
    chrisops-assistant-query
            |
            v
    chrisops-assistant-summary
            |
            v
    Future assistant interfaces

## Design Principles

### ChrisOps remains authoritative

The assistant must never become the source of truth.

Operational facts originate from the ChrisOps state API.

### Deterministic before intelligent

The summary layer translates known facts only:

-   active findings
-   maintenance state
-   observation failures
-   approved revision state
-   generated timestamps

It must not:

-   infer causes
-   invent missing information
-   override findings
-   perform remediation

## Input Contract

The summary adapter consumes the authenticated output of:

    chrisops-assistant-query

Expected fields:

-   approved_revision
-   assets
-   active_findings
-   assets_under_maintenance
-   assets_with_failed_latest_attempt
-   assets_without_valid_observation
-   generated_at

## Output Contract

Example:

``` json
{
  "health": "healthy",
  "attention_required": false,
  "summary": "ChrisOps reports no active findings and all approved assets have valid observations.",
  "details": {
    "active_findings": 0,
    "maintenance_assets": 0,
    "observation_failures": 0
  }
}
```

## Health Evaluation

Healthy:

-   no active findings
-   no missing observations
-   no failed collection attempts requiring attention

Attention Required:

-   active findings exist
-   approved assets lack valid observations
-   failed collection attempts require review

The adapter reports state. It does not remediate.

## Future Expansion

Possible consumers:

-   Open WebUI tool integration
-   ChrisOps conversational assistant
-   operational dashboards
-   notification workflows

Boundary:

ChrisOps decides state. The assistant explains state.
