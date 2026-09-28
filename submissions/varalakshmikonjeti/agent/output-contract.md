# Pack Manager Agent Output Contract

## Purpose

This document defines the structured output produced by the Pack Manager headless agent after processing a verification request.

The output provides downstream stages with the verification decision, observed evidence, check results, reasoning, and model/API status without requiring access to internal implementation details.

## Required Fields

Each output record should contain:

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

## Record Identity

`record_id` identifies the verification record.

`unit_id` identifies the packing verification unit and must remain unchanged from the input request.

`org_id` identifies the organisation that owns the verification.

The output must preserve these identifiers so downstream stages can correlate the decision with the original request.

## Overall Verdict

`overall_verdict` must be one of:

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

The automated workflow could not complete a reliable decision and human review is required.

A model or API failure must not be represented as `PASS`.

## Expected Contents

`expected_contents` contains the order contents supplied for verification.

The output should preserve the expected contents used by the agent when producing the decision.

Example:

{
  "sku": "SKU-A",
  "quantity": 2
}

## Observed Contents

`observed_contents` contains items identified from the submitted image.

Observed contents must be based on available evidence.

The agent must not invent an observed item, quantity, or attribute that is not supported by the image.

If the image does not provide sufficient evidence, the relevant observation should be marked as uncertain or omitted according to the implementation.

## Check Results

The `checks` object should contain:

- `item_presence`
- `quantity`
- `extra_items`
- `evidence_sufficiency`

Each check must be one of:

- `PASS`
- `FAIL`
- `UNCERTAIN`

The check results should reflect the evidence actually available for the verification.

## Evidence

The `evidence` field should preserve observations or references supporting the decision.

Evidence should allow a reviewer to understand why the recorded checks and overall verdict were produced.

The output must not claim evidence that was not actually observed.

## Reasoning

The `reasoning` field should summarize the relevant observations and checks that resulted in the overall verdict.

Reasoning must remain grounded in the supplied image and verification context.

The reasoning must not invent observations or unsupported conclusions.

## Model Status

`model_status` records the state of the model or API operation.

Possible values include:

- `completed`
- `error`
- `timeout`

The implementation may use additional status values when required, provided they remain understandable to downstream stages.

## Pending Review

`pending_review` indicates whether human review is required.

It should be:

- `false` when the automated workflow completed normally
- `true` when human review is required

A model or API failure should produce a pending-review result while preserving the submitted verification context and available evidence.

## Example Successful Output

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
  "reasoning": "The available image evidence supports the expected item and quantity.",
  "model_status": "completed",
  "pending_review": false
}

## Example Pending Review Output

{
  "record_id": "PCK-000002",
  "unit_id": "UNIT-0002",
  "org_id": "org_demo_alpha",
  "created_at": "2026-09-27T12:05:00Z",
  "overall_verdict": "PENDING_REVIEW",
  "expected_contents": [
    {
      "sku": "SKU-B",
      "quantity": 1
    }
  ],
  "observed_contents": [],
  "checks": {
    "item_presence": "UNCERTAIN",
    "quantity": "UNCERTAIN",
    "extra_items": "UNCERTAIN",
    "evidence_sufficiency": "UNCERTAIN"
  },
  "evidence": [],
  "reasoning": "The verification could not be completed because the model/API operation failed.",
  "model_status": "error",
  "pending_review": true
}

## Tenant Isolation

Every output record must remain associated with its `org_id`.

The output must not expose:

- another organisation's verification records
- another organisation's image references
- another organisation's evidence
- another organisation's order contents

Tenant isolation applies to both decision data and referenced evidence.

## Downstream Consumption

Downstream stages should be able to consume the output without requiring:

- internal model prompts
- private model configuration
- interactive UI state
- implementation-specific details

The output should conform to the contracts in the `contract/` directory.

## Auditability

The output should preserve enough information to determine:

- what was expected
- what was observed
- which checks were performed
- what decision was produced
- what evidence supported the decision
- whether a model/API failure occurred
- whether human review is required

If an operator later overrides the decision, the original automated output must remain available.

## Evidence-First Rule

The output must distinguish between expected information and observed evidence.

Expected contents must not automatically become observed contents.

Insufficient evidence must not be converted into `PASS`.

Model/API failures must not be converted into successful verification results.

## Interoperability

The output is intended for downstream workflow stages and should remain understandable without access to internal model prompts or implementation details.

The output contract does not claim that records are immutable, tamper-proof, or production-secure unless those properties are separately implemented and demonstrated.
