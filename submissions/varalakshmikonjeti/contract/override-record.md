# Pack Manager Override Record

## Purpose

This document defines how a human override of an automated Pack Manager decision should be recorded.

An override must preserve the original automated decision rather than silently replacing it.

## Required Fields

Each override record should contain:

- `record_id`
- `unit_id`
- `org_id`
- `original_verdict`
- `new_verdict`
- `override_reason`
- `operator_id`
- `override_timestamp`

## Original Verdict

The `original_verdict` is the automated verdict produced by Pack Manager before the operator made a change.

It should not be modified after the override is recorded.

## New Verdict

The `new_verdict` is the verdict selected by the operator after reviewing the available evidence.

It should be one of:

- `PASS`
- `FAIL`
- `UNCERTAIN`

## Override Reason

The `override_reason` should explain why the operator changed the automated decision.

The reason should be based on the available evidence or operational context.

## Operator Identity

The `operator_id` identifies the operator who made the override when operator identity is available.

## Override Timestamp

The `override_timestamp` records when the override was made.

## Evidence Preservation

The original evidence and automated reasoning should remain associated with the verification record.

An override must not delete or replace the original evidence.

## Tenant Isolation

Every override must remain associated with its `org_id`.

An operator from one organisation must not be able to modify or access records belonging to another organisation.

## Example

{
  "record_id": "PCK-000001",
  "unit_id": "UNIT-0001",
  "org_id": "org_demo_alpha",
  "original_verdict": "FAIL",
  "new_verdict": "PASS",
  "override_reason": "Operator confirmed the item was present after reviewing the physical box.",
  "operator_id": "operator-001",
  "override_timestamp": "2026-09-27T12:15:00Z"
}

## Auditability

The override should be retained as part of the verification history.

The system should allow a reviewer to determine:

- what the automated system originally decided
- what the operator changed it to
- why the change was made
- who made the change
- when the change was made

The override record does not claim that the underlying record is immutable or tamper-proof.