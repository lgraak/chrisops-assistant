# ChrisOps Assistant Summary Contract v1

## Purpose

The ChrisOps assistant summary adapter provides a human-oriented interpretation layer between the ChrisOps state API and any future AI assistant or user-facing interface.

The adapter must not replace ChrisOps state evaluation. It only translates approved state data into concise operational summaries.

## Data Flow

ChrisOps state API
    |
    v
assistant-query wrapper
    |
    v
assistant-summary adapter
    |
    v
LLM or user interface

## Responsibilities

The summary adapter may:

- summarize current health state
- identify whether attention is required
- summarize active findings
- summarize maintenance conditions
- summarize observation failures
- provide approved revision information

The summary adapter must not:

- modify state
- acknowledge findings
- suppress findings
- create remediation actions
- make infrastructure changes
- infer conditions not present in ChrisOps state

## Output Contract

Example:

```json
{
  "health": "healthy",
  "attention_required": false,
  "summary": "No active findings.",
  "details": {
    "active_findings": 0,
    "assets_under_maintenance": 0,
    "assets_without_valid_observation": 0
  }
}
