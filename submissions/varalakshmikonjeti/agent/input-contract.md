# Pack Manager Agent Input Contract

## Purpose

This document defines the input expected by the Pack Manager headless agent for each packing verification request.

The input contract ensures that the agent receives enough information to identify the verification unit, determine the expected contents, access the submitted image, and preserve tenant context.

## Required Fields

Each verification request should contain:

- `unit_id`
- `org_id`
- `expected_contents`
- `image_reference`

The following fields should be preserved when available:

- `record_id`
- `capture_timestamp`
- `channel`
- `operator_id`

## Unit Identity

`unit_id` is the shared chain identifier for the verification workflow.

The agent must preserve the supplied `unit_id` without changing it.

The same `unit_id` should be available in the resulting decision so downstream stages can correlate the verification result with the original packing unit.

## Organisation Identity

`org_id` identifies the organisation that owns the verification request.

The agent must associate all verification data with the supplied `org_id`.

The agent must not use data, images, or evidence belonging to another organisation when processing the request.

## Expected Contents

`expected_contents` contains the order lines that the submitted packing photograph must be checked against.

Each expected item should provide enough information to identify the item and expected quantity.

Example:

{
  "sku": "SKU-A",
  "quantity": 2
}

Expected contents must be treated as the reference condition for the verification.

## Image Reference

`image_reference` identifies the submitted packing photograph used as evidence.

The agent should access only the image associated with the current verification request and organisation.

The image reference should be preserved in the resulting evidence record where supported.

The agent must not claim that an item was observed when the submitted image does not provide sufficient evidence.

## Capture Information

When available, the request may contain:

- capture timestamp
- capture channel
- operator identifier

Capture information should be preserved as part of the verification context.

Missing optional capture information must not by itself be treated as a successful verification.

## Input Validation

Before verification begins, the agent should validate:

- `unit_id` is present
- `org_id` is present
- `expected_contents` is present
- `image_reference` is present
- expected quantities are valid
- the referenced image belongs to the correct organisation

Invalid input must not produce a successful `PASS` decision.

## Invalid Input Handling

If required input is missing or invalid, the agent should preserve the verification context and return an appropriate failure or review result according to the implementation.

The agent must not invent missing identifiers, quantities, image evidence, or order contents.

## Example Input

{
  "record_id": "PCK-000001",
  "unit_id": "UNIT-0001",
  "org_id": "org_demo_alpha",
  "created_at": "2026-09-27T12:00:00Z",
  "expected_contents": [
    {
      "sku": "SKU-A",
      "quantity": 2
    },
    {
      "sku": "SKU-B",
      "quantity": 1
    }
  ],
  "image_reference": "captures/org_demo_alpha/UNIT-0001.jpg",
  "capture_timestamp": "2026-09-27T11:59:45Z",
  "channel": "packing_station",
  "operator_id": "operator-001"
}

## Tenant Isolation

Every input request must remain associated with its `org_id`.

The agent must prevent:

- cross-organisation image access
- cross-organisation evidence access
- cross-organisation verification data access

An image reference must not be trusted solely because it exists. The implementation should ensure that the referenced evidence belongs to the organisation associated with the request.

## Evidence Integrity

The input contract describes what was supplied to the verification workflow.

The agent must distinguish between:

- expected information supplied by the order
- evidence actually observed in the image
- conclusions produced by the verification process

Expected contents must not be recorded as observed contents unless the image provides supporting evidence.

## Downstream Compatibility

The input should provide enough information for the agent to produce a decision conforming to:

- `contract/evidence-record.md`
- `contract/decision-schema.md`
- `contract/override-record.md`

The input contract does not require downstream stages to access internal model prompts or implementation details.

## Operational Rule

The agent should follow an evidence-first approach:

1. validate the input
2. preserve the verification context
3. access the submitted evidence
4. perform the verification
5. record observations and checks
6. produce the appropriate verdict
7. preserve the resulting decision for downstream processing

The agent must never convert missing or insufficient evidence into an unsupported `PASS`.