# Pack Manager Source

## Purpose

This directory contains the source implementation for the Pack Manager verification workflow.

The implementation should connect the documented contracts and headless agent workflow to the actual verification logic.

## Responsibilities

The source implementation is responsible for:

- accepting a verification request
- validating required inputs
- loading expected order contents
- accessing submitted image evidence
- invoking the configured verification/model logic
- evaluating item presence
- evaluating quantity correctness
- detecting extra items
- determining evidence sufficiency
- producing a structured verification decision
- preserving evidence and reasoning
- handling model/API failures
- supporting pending review
- preserving tenant isolation

## Contract Alignment

The implementation should produce records compatible with:

- `contract/evidence-record.md`
- `contract/decision-schema.md`
- `contract/override-record.md`
- `agent/output-contract.md`

The source implementation must not contradict these contracts.

## Evidence-First Behaviour

The implementation must distinguish between:

- expected contents
- observed contents
- available evidence
- inferred or uncertain observations

Expected order contents must not automatically be treated as observed contents.

The implementation must not claim that an item, quantity, or attribute was observed unless the available image evidence supports that observation.

## Verdict Handling

The implementation must support:

- `PASS`
- `FAIL`
- `UNCERTAIN`
- `PENDING_REVIEW`

Insufficient evidence must result in `UNCERTAIN` rather than an unsupported `PASS`.

Model or API failures that prevent reliable verification must result in `PENDING_REVIEW`.

## Model/API Failure Handling

A model or API failure must not be represented as a successful verification.

When verification cannot be completed reliably, the implementation should:

1. preserve the verification context
2. preserve the submitted capture reference
3. record the model/API status
4. record relevant error information
5. create a pending-review result
6. return the structured result downstream

## Tenant Isolation

Every verification operation must remain associated with its `org_id`.

The implementation must prevent cross-tenant access to:

- verification requests
- order contents
- images
- evidence
- decision records

Image references must also remain protected by tenant context.

## Auditability

The implementation should preserve enough information to determine:

- what was expected
- what was observed
- what checks were performed
- what evidence supported the decision
- what verdict was produced
- what model/API status occurred
- whether human review is required

Automated decisions must remain available if an operator later overrides the result.

## Downstream Interoperability

The source implementation should return structured information that downstream stages can consume without requiring:

- internal model prompts
- private model configuration
- interactive UI state
- implementation-specific details

## Current Status

This directory currently defines the intended source boundary for Pack Manager.

Implementation files may be added beneath this directory as the verification workflow is developed.

No production accuracy or reliability claim should be made without appropriate evaluation.