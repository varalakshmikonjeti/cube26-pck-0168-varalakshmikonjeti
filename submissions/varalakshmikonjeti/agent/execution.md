# Pack Manager Agent Execution Guide

## Purpose

This document describes how the Pack Manager headless agent should execute a packing verification from input through structured output.

The execution flow is designed to preserve evidence, avoid unsupported claims, and provide a deterministic handoff to downstream stages.

## Execution Flow

The agent should execute the following sequence:

1. Receive the verification request.
2. Validate the request.
3. Confirm tenant and verification identifiers.
4. Load the expected order contents.
5. Access the submitted packing image.
6. Verify that the image can be processed.
7. Invoke the Pack Manager verification logic.
8. Evaluate the verification checks.
9. Determine the overall verdict.
10. Preserve evidence and reasoning.
11. Handle model/API failures when they occur.
12. Construct the structured output.
13. Return the output to the downstream workflow.

## Step 1: Receive Verification Request

The agent receives a verification unit containing the information required to perform the packing check.

The request should provide:

- `unit_id`
- `org_id`
- expected order contents
- image reference
- capture information when available

The `unit_id` must remain unchanged throughout execution.

## Step 2: Validate Input

Before invoking the model, validate that:

- `unit_id` is present
- `org_id` is present
- expected contents are present
- expected quantities are valid
- an image reference is available

Invalid input must not result in a successful verification.

If required information is missing, the agent should return an appropriate failure or review result according to the implementation.

## Step 3: Confirm Tenant Context

The agent must associate the verification request with its `org_id`.

All subsequent reads and writes must remain within that organisation's context.

The agent must not use another organisation's:

- order data
- images
- verification records
- evidence
- decisions

## Step 4: Load Expected Contents

The agent loads the order lines associated with the verification unit.

Expected contents should contain enough information to determine:

- expected item identity
- expected quantity

The expected contents are the comparison baseline.

Expected contents must not automatically be treated as observed contents.

## Step 5: Access Submitted Image

The agent loads or accesses the submitted packing photograph using the image reference provided by the verification request.

The image reference must remain associated with the correct `org_id`.

The agent should preserve available capture information such as:

- capture timestamp
- source or channel
- image reference

## Step 6: Validate Image Evidence

Before model verification, the agent should confirm that the submitted image is available and usable.

Relevant limitations should be recorded when the image is:

- missing
- unreadable
- incomplete
- too unclear to identify required contents
- otherwise insufficient for reliable verification

The agent must not infer evidence that cannot be supported by the image.

## Step 7: Invoke Pack Manager Verification

The agent invokes the Pack Manager verification logic using:

- expected order contents
- submitted image evidence
- relevant verification context

Where supported, related checks should be evaluated as part of the same verification unit.

The model output must be treated as evidence for the decision rather than as permission to invent unsupported observations.

## Step 8: Evaluate Verification Checks

The agent evaluates:

- item presence
- quantity correctness
- extra-item detection
- evidence sufficiency

Each check must result in:

- `PASS`
- `FAIL`
- `UNCERTAIN`

The checks must be based on available evidence.

## Step 9: Determine Overall Verdict

The agent determines the overall verification result.

The allowed values are:

- `PASS`
- `FAIL`
- `UNCERTAIN`
- `PENDING_REVIEW`

The decision must follow the evidence.

### PASS

Use `PASS` when the available evidence supports the expected packing condition.

### FAIL

Use `FAIL` when the available evidence shows a packing problem such as:

- missing item
- wrong item
- incorrect quantity
- extra item

### UNCERTAIN

Use `UNCERTAIN` when the evidence is insufficient to make a reliable automated judgment.

Insufficient evidence must not be converted into `PASS`.

### PENDING_REVIEW

Use `PENDING_REVIEW` when the automated workflow cannot complete a reliable decision and human review is required.

This includes relevant model or API failures.

## Step 10: Preserve Evidence

The agent should preserve:

- expected contents
- observed contents
- check results
- evidence references
- image limitations
- reasoning
- model/API status
- overall verdict
- pending-review status

The resulting record must remain consistent with the contracts in the `contract/` directory.

## Step 11: Handle Model or API Failure

If the model or API fails, times out, or otherwise cannot complete verification, the agent must not create a false successful result.

The agent should:

1. preserve the submitted capture and verification context
2. record the model/API status
3. record relevant error information
4. create a `PENDING_REVIEW` result
5. set `pending_review` to `true`
6. return the structured result to the downstream workflow

The operational workflow should continue without falsely claiming that automated verification succeeded.

## Step 12: Construct Output

The agent constructs the output according to:

- `contract/evidence-record.md`
- `contract/decision-schema.md`
- `contract/override-record.md`
- `agent/output-contract.md`

The output should contain the required identity, contents, checks, evidence, reasoning, verdict, and model status fields.

## Step 13: Return Downstream Result

The completed decision should be returned to the downstream workflow as a structured record.

Downstream stages should not need access to:

- internal model prompts
- private model configuration
- internal implementation details
- interactive UI state

The returned record should contain enough information for downstream processing and audit.

## Error Handling

The agent should distinguish between verification failures and execution failures.

A packing problem supported by evidence should produce `FAIL`.

Insufficient evidence should produce `UNCERTAIN`.

A model/API failure that prevents reliable verification should produce `PENDING_REVIEW`.

The agent must not convert execution failures into `PASS`.

## Audit Trail

For each execution, preserve enough information to determine:

- what verification unit was processed
- which organisation owned the unit
- what contents were expected
- what evidence was available
- what items were observed
- which checks were performed
- what verdict was produced
- what model/API status occurred
- whether human review is required

If an operator later overrides the automated result, the original result must remain available.

## Tenant Isolation

Tenant isolation must apply throughout execution.

The agent must verify that:

- input belongs to the requested `org_id`
- image references belong to the same organisation
- evidence belongs to the same organisation
- output records remain associated with the same organisation

Cross-tenant access must be rejected.

## Evidence-First Rules

The agent must follow these rules:

- expected contents are not automatically observed contents
- image evidence must support observations
- uncertain observations must remain uncertain
- insufficient evidence must not become `PASS`
- model/API failures must not become successful verification
- reasoning must remain grounded in available evidence
- synthetic repository data must not be represented as authoritative external policy data

## Output Guarantee

The execution flow guarantees the structure and preservation of the verification result, not the correctness of the underlying model prediction.

No production accuracy, latency, or reliability claim should be made unless supported by appropriate evaluation.

## Current Status

This document describes the intended headless execution flow.

The workflow should be validated against representative verification cases, failure cases, and the organisers' evaluation requirements before being considered production-ready.
