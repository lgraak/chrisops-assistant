# ChrisOps Assistant Acceptance Evaluation Policy v1

## Purpose

This document records the evaluation strategy used by the ChrisOps assistant acceptance test framework.

The acceptance layer validates that assistant responses remain within defined reasoning and safety boundaries. It does not attempt to evaluate general intelligence, writing quality, or semantic equivalence.

## Decision: Strict Contract Matching

The acceptance evaluator uses explicit contract statements defined by each fixture.

Required statements are matched using deterministic text checks.

Example:

A fixture requiring:
warning exists
expects that phrase or equivalent contract wording to be explicitly represented in the response fixture.

## Why Strict Matching Was Chosen

The acceptance layer exists to prevent unsafe reasoning behavior.

The goal is not to determine whether a human would consider two statements equivalent. The goal is to verify that:

- required facts are present
- prohibited assumptions are absent
- unsupported remediation is not invented
- classification boundaries remain stable

Using semantic similarity or an LLM judge would introduce another reasoning layer into the validation system and could hide failures.

## Fixture Responsibilities

Acceptance fixtures should contain:

- known input facts
- expected classification
- required statements
- allowed statements
- prohibited statements

Response fixtures should represent acceptable assistant behavior against those contracts.

## Future Consideration

A future user-facing evaluation system may use semantic scoring or human review.

That is separate from acceptance testing.

The acceptance layer should remain deterministic and reproducible.
