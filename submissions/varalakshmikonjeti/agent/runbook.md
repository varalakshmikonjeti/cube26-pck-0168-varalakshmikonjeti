# Pack Manager Headless Agent

## Purpose

This directory defines the headless workflow for running Pack Manager verification without requiring an interactive user interface.

The agent is responsible for receiving a verification unit, invoking the Pack Manager verification workflow, preserving the resulting evidence, and returning a structured decision for downstream stages.

## Workflow

The headless agent should follow this sequence:

1. Receive a verification unit.
2. Validate the required input fields.
3. Load the expected order contents.
4. Load or access the submitted packing photograph.
5. Invoke Pack Manager verification.
6. Evaluate item presence, quantity, extra items, and evidence sufficiency.
7. Produce `PASS`, `FAIL`, `UNCERTAIN`, or `PENDING_REVIEW`.
8. Preserve the evidence and reasoning associated with the decision.
9. Return the structured decision to the downstream workflow.

## Verification Unit

A verification unit should contain enough information to identify the packing task and its expected contents.

At minimum, the workflow should preserve:

- `unit_id`
- `org_id`
- expected order lines
- image reference
- capture information when available

The `unit_id` should remain unchanged throughout the workflow so downstream stages can correlate the decision with the same verification unit.

## Input Validation

Before model verification begins, the agent should validate:

- required identifiers are present
- the organisation identifier is available
- expected contents are present
- an image reference is available
- quantities are valid

Invalid input should not be treated as a successful verification.

## Model Invocation

The agent should invoke the Pack Manager verification logic using the available image evidence and expected contents.

Model checks should be batched per verification unit where supported.

The agent must not claim observations that were not supported by the submitted image.

## Decision Handling

The agent should preserve the following outcomes:

- `PASS`
- `FAIL`
- `UNCERTAIN`
- `PENDING_REVIEW`

`PASS` means the available evidence supports the expected packing condition.

`FAIL` means the available evidence shows a packing problem.

`UNCERTAIN` means the evidence is insufficient for a reliable automated judgment.

`PENDING_REVIEW` means the automated workflow could not complete a reliable decision and human review is required.

## Model or API Failure

A model or API failure must not be represented as a successful verification.

The agent should:

1. preserve the submitted capture and verification context
2. record the model/API error status
3. create a pending-review result
4. allow the operational workflow to continue without falsely claiming a successful automated decision

## Evidence Preservation

The agent should preserve:

- expected contents
- observed contents
- verification checks
- evidence references
- reasoning
- model/API status
- overall verdict
- pending-review status

The resulting record should follow the contracts in the `contract/` directory.

## Tenant Isolation

Every verification unit and decision must remain associated with its `org_id`.

The agent must not expose:

- one organisation's verification records to another organisation
- one organisation's image references to another organisation
- one organisation's evidence through another organisation's workflow

Tenant isolation must apply to both decision data and referenced images.

## Downstream Output

The agent should return a structured Pack Manager decision that downstream stages can consume without requiring:

- internal model prompts
- private implementation details
- interactive UI state

The output should conform to:

- `contract/evidence-record.md`
- `contract/decision-schema.md`
- `contract/override-record.md`

## Auditability

The agent must preserve enough information to determine:

- what was expected
- what was observed
- which checks were performed
- what decision was produced
- what evidence supported the decision
- whether a model/API failure occurred
- whether human review is required

If an operator later overrides the decision, the original automated decision and evidence must remain available.

## Operational Principles

The headless agent follows these principles:

- evidence before conclusions
- `UNCERTAIN` is a valid result
- model/API failures do not become false `PASS` results
- verification records remain auditable
- tenant isolation is preserved
- downstream stages receive structured information
- synthetic repository data is not treated as authoritative Amazon policy or fee data
- no production accuracy claim is made without appropriate evaluation

## Current Implementation Status

The Pack Manager verification implementation and core contracts are currently available.

The headless agent workflow is documented here as the intended execution flow.

Further implementation and integration work may be required before this workflow is considered production-ready.

## Limitations

The headless agent has not yet been validated against the organisers' unseen evaluation set.

Performance characteristics such as accuracy, false positives, false negatives, latency, model failure rates, and human-review rates require further evaluation.