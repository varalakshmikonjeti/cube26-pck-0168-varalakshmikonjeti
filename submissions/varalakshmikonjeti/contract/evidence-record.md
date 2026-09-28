# Pack Manager Evidence Contract

## Purpose
This contract defines the evidence record produced by Pack Manager so that another stage in the commerce workflow can understand what was checked and why the decision was made.

## Record Identity

Each verification record should contain:

- `record_id`
- `unit_id`
- `org_id`
- `created_at`

`unit_id` is the shared chain identifier used by the buildathon stages.

## Input Evidence

The record should preserve:

- expected order lines
- reference to the submitted image
- capture timestamp when available
- channel
- operator identifier when available

## Observed Evidence

The record should preserve:

- items identified in the image
- observed quantities
- unidentified or ambiguous items
- image/evidence limitations

## Checks

Each verification should record the result of:

- item presence
- quantity correctness
- extra-item detection
- evidence sufficiency

Each check should have a verdict of:

- `PASS`
- `FAIL`
- `UNCERTAIN`

## Overall Verdict

The overall verification result should be one of:

- `PASS`
- `FAIL`
- `UNCERTAIN`
- `PENDING_REVIEW`

`UNCERTAIN` means the available evidence is insufficient for a reliable judgment.

`PENDING_REVIEW` is used when the workflow cannot complete a reliable automated decision, such as a model/API failure.

## Reasoning and Evidence

The record should preserve:

- observations used for each check
- evidence supporting the observation
- reasoning for the resulting verdict
- model/API status
- relevant error information when a model call fails

The implementation must not claim evidence that was not actually observed.

## Overrides

If an operator changes an automated decision, the record should retain:

- original verdict
- new verdict
- override reason
- operator identifier
- override timestamp

The original automated decision must not be silently discarded.

## Tenant Isolation

Every record is associated with an `org_id`.

Records belonging to one organisation must not be accessible to another organisation.

Image references must also be protected from cross-tenant access.

## Example Shape

{
  "record_id": "PCK-000001",
  "unit_id": "UNIT-0001",
  "org_id": "org_demo_alpha",
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
  "overall_verdict": "PASS",
  "evidence": [],
  "reasoning": "",
  "model_status": "completed",
  "pending_review": false
}

The example is illustrative. The implementation may use a different concrete schema as long as the required evidence and decision information is preserved.

## Interoperability

The record should be understandable by downstream stages without requiring access to internal model prompts or implementation details.

The contract describes the evidence and decision produced by Pack Manager, not a claim that the record itself is immutable or tamper-proof.