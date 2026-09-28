# Pack Manager Failure Handling

## Purpose

This document defines how the Pack Manager headless agent should handle validation errors, image problems, model failures, API failures, timeouts, and other conditions that prevent reliable automated verification.

Failure handling must preserve the verification context and must never turn an execution failure into a false successful verification.

## General Principles

The agent should follow these principles:

- preserve the submitted verification context
- preserve available evidence
- distinguish packing failures from execution failures
- do not invent observations
- do not convert insufficient evidence into PASS
- do not convert model/API failures into PASS
- use UNCERTAIN when evidence is insufficient for a reliable judgment
- use PENDING_REVIEW when automated verification cannot complete reliably
- preserve tenant isolation
- keep the result auditable

## Input Validation Failure

If required input is missing or invalid, the agent must not perform a successful verification.

Examples include:

- missing unit_id
- missing org_id
- missing expected contents
- invalid quantity
- missing image reference
- invalid verification request structure

The agent should record the validation problem and return an appropriate structured failure or review result according to the implementation.

The agent must not fabricate missing information.

## Missing Image

If the submitted image cannot be found or accessed, the agent must not claim that the expected contents were observed.

The agent should:

1. preserve the verification request
2. record the image access problem
3. mark evidence as insufficient
4. avoid unsupported observations
5. return an appropriate UNCERTAIN or PENDING_REVIEW result according to the implementation

## Unusable Image

An image may be present but unsuitable for reliable verification.

Examples include:

- unreadable image
- incomplete capture
- severe obstruction
- insufficient visibility
- image quality that prevents reliable identification

The agent should record the limitation.

It must not infer item identity or quantity from evidence that cannot support the observation.

When the limitation prevents reliable automated verification, the result should be UNCERTAIN or PENDING_REVIEW as appropriate.

## Model Failure

If the model invocation fails, the agent must not treat the failure as a successful verification.

The agent should:

1. preserve the verification request
2. preserve the submitted image reference
3. record the model failure
4. preserve any valid evidence already available
5. set model_status appropriately
6. create a PENDING_REVIEW result
7. set pending_review to true

The failure should remain visible to downstream stages and reviewers.

## API Failure

If a required API call fails, the agent should preserve the verification context and record the API failure.

Examples include:

- service unavailable
- authentication failure
- request rejection
- invalid API response
- unexpected response format

The agent must not create a successful verification from an unsuccessful API operation.

If the API failure prevents reliable verification, the result should be:

overall_verdict = PENDING_REVIEW
pending_review = true

## Timeout

If model or API processing exceeds the permitted execution time, the agent should treat the operation as incomplete.

The agent should:

1. preserve the submitted verification context
2. record the timeout
3. set model_status to timeout when applicable
4. preserve available evidence
5. create a pending-review result

A timeout must not become PASS.

## Invalid Model Response

If the model returns an invalid, incomplete, or unusable response, the agent should not attempt to invent missing fields.

Examples include:

- invalid JSON
- missing required decision information
- unsupported verdict
- missing evidence
- inconsistent check results

The agent should record the response problem and return PENDING_REVIEW when reliable automated verification cannot be completed.

## Insufficient Evidence

Insufficient evidence is different from a model or API failure.

When the system successfully processes the request but the available image evidence cannot support a reliable conclusion, the appropriate outcome may be:

overall_verdict = UNCERTAIN

The check results should identify which checks could not be established reliably.

The system must not use expected contents as proof that an item was observed.

## Packing Failure

A packing problem supported by the available evidence is a verification result, not an execution failure.

Examples include:

- expected item is missing
- wrong item is observed
- quantity is incorrect
- extra item is observed

When the evidence supports the problem, the appropriate overall result is:

overall_verdict = FAIL

The evidence and reasoning should explain the observed problem.

## Evidence vs Execution Failure

The agent should distinguish between:

### Verification Failure

The system successfully performed verification and the evidence indicates a packing problem.

Result:

FAIL

### Insufficient Evidence

The system processed the available evidence but could not reliably determine the packing condition.

Result:

UNCERTAIN

### Execution Failure

The system could not reliably complete automated verification because of a model, API, timeout, or related operational failure.

Result:

PENDING_REVIEW

This distinction must remain visible in the structured output.

## Error Information

When an error occurs, the record should preserve relevant error information without exposing unnecessary secrets.

Error information may include:

- error category
- operation that failed
- model/API status
- timeout status
- safe diagnostic message

The record must not expose:

- API keys
- passwords
- private credentials
- authentication tokens
- other secrets

## Retry Behavior

Retries may be used for transient model or API failures when supported by the implementation.

Retries should not:

- create duplicate verification records
- overwrite the original verification context
- hide the occurrence of a failure
- convert an unresolved failure into an unsupported PASS

If retries are exhausted, the agent should create the appropriate pending-review result.

## Idempotency

Repeated processing of the same verification unit should not silently create conflicting decisions.

The implementation should use the available record or unit identifiers to prevent accidental duplication where required.

The original verification context must remain traceable.

## Tenant Isolation During Failure Handling

Failure handling must preserve tenant isolation.

Error records, image references, evidence, and verification results must remain associated with the correct org_id.

An error in one organisation's workflow must not expose information belonging to another organisation.

## Downstream Handoff

When automated verification cannot complete, the agent should still return a structured result whenever the implementation permits.

The result should provide downstream stages with:

- record_id
- unit_id
- org_id
- expected contents
- available observed contents
- check results
- evidence
- reasoning
- model/API status
- overall verdict
- pending-review status

This allows downstream stages to continue the workflow without treating an incomplete verification as successful.

## Auditability

Failure handling should preserve enough information to determine:

- what request was received
- what evidence was available
- what operation failed
- why automated verification could not complete
- what result was returned
- whether human review is required

Failures should remain auditable after the workflow completes.

## Security

Failure handling must not weaken security controls.

The agent must continue to enforce:

- tenant isolation
- access control
- safe error reporting
- protection of image references
- protection of credentials and secrets

Operational errors must not expose private data.

## Evidence-First Rule

The agent must always prefer an explicit uncertain or review result over an unsupported conclusion.

In particular:

- missing evidence must not become PASS
- invalid model output must not become PASS
- API failure must not become PASS
- timeout must not become PASS
- expected contents must not become observed contents
- unsupported observations must not be added to the record

## Final Failure States

The agent should use the following outcomes consistently:

| Situation | Overall Verdict | Pending Review |
|---|---|---|
| Evidence supports correct packing | PASS | false |
| Evidence supports packing problem | FAIL | false |
| Evidence is insufficient | UNCERTAIN | false |
| Model/API/operational failure prevents reliable verification | PENDING_REVIEW | true |

The exact implementation may include additional internal error categories, but the downstream contract should continue to use the defined verdict values.

## Current Status

This document defines the intended failure-handling behavior for the Pack Manager headless agent.

Failure scenarios should be tested with representative cases before the workflow is considered production-ready.