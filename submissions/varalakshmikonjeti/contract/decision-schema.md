# Pack Manager Decision Schema

## Purpose

This document defines the structured decision produced by Pack Manager for each outbound packing verification.

The schema is designed so that downstream stages can consume the decision without depending on internal model prompts or implementation details.

## Required Fields

Each decision record should contain:

- `record_id`
- `unit_id`
- `org_id`
- `created_at`
- `overall_verdict`
- `expected_contents`
- `observed_contents`
- `checks`
- `evidence`
- `reasoning`
- `model_status`
- `pending_review`

## Verdict Values

The `overall_verdict` must be one of:

- `PASS`
- `FAIL`
- `UNCERTAIN`
- `PENDING_REVIEW`

### PASS

The available evidence supports the expected packing condition.

### FAIL

The available evidence shows a packing problem such as a missing item, wrong item, incorrect quantity, or extra item.

### UNCERTAIN

The available evidence is insufficient for a reliable automated judgment.

### PENDING_REVIEW

The automated workflow could not complete a reliable decision, such as when a model or API failure occurs.

## Check Results

The `checks` object should contain:

- `item_presence`
- `quantity`
- `extra_items`
- `evidence_sufficiency`

Each check should have one of these values:

- `PASS`
- `FAIL`
- `UNCERTAIN`

## Expected Contents

`expected_contents` represents the order lines supplied for the verification.

Example:

{
  "sku": "SKU-A",
  "quantity": 2
}

## Observed Contents

`observed_contents` represents items that can be identified from the submitted photograph.

The system should not invent an observed item when the image does not provide sufficient evidence.

## Evidence

The `evidence` field should contain observations or references that support the recorded checks and verdict.

Evidence should be sufficient for a reviewer to understand how the decision was reached.

## Reasoning

The `reasoning` field should explain the relevant observations that led to the recorded decision.

It should not claim observations that are not supported by the submitted image or other available evidence.

## Model Status

`model_status` should indicate the state of the model/API operation.

Examples include:

- `completed`
- `error`
- `timeout`

## Pending Review

`pending_review` should be:

- `false` when the automated workflow completed normally
- `true` when human review is required

A model/API failure should preserve the capture and create a pending-review record rather than blocking the packing workflow.

## Example

{
  "record_id": "PCK-000001",
  "unit_id": "UNIT-0001",
  "org_id": "org_demo_alpha",
  "created_at": "2026-09-27T12:00:00Z",
  "overall_verdict": "PASS",
  "expected_contents": [
    {
      "sku": "SKU-A",
      "quantity": 2
    }
  ],
  "observed_contents": [
    {
      "description": "identified item",
      "quantity": 2
    }
  ],
  "checks": {
    "item_presence": "PASS",
    "quantity": "PASS",
    "extra_items": "PASS",
    "evidence_sufficiency": "PASS"
  },
  "evidence": [],
  "reasoning": "The expected item and quantity are supported by the available image evidence.",
  "model_status": "completed",
  "pending_review": false
}

## Tenant Isolation

Every decision record must remain associated with its `org_id`.

Records and image references belonging to one organisation must not be accessible to another organisation.

## Interoperability

Downstream stages should be able to understand the decision using this contract without requiring access to private model prompts or internal implementation details.

This schema does not claim that the record is immutable or tamper-proof.