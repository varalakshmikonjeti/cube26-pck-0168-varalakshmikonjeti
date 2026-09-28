# Build Brief

## Project

Pack Manager — photograph-based outbound packing verification.

## Objective

Build a measurable verification agent that checks whether the contents visible in an open outbound box match the expected order lines before the box is sealed.

The system should produce an evidence-backed decision rather than only a binary answer.

## Target Workflow

1. Operator provides the expected order lines.
2. Operator provides a photograph of the open box.
3. The agent analyses the photograph and expected contents.
4. The agent checks item presence, quantities, and unexpected items.
5. The agent determines whether the evidence is sufficient.
6. The system produces PASS, FAIL, or UNCERTAIN.
7. The decision and supporting evidence are retained for review.

## Inputs

### Required

- Expected order lines
- Photograph of the open box

### Example Order Lines

SKU-A:2
SKU-B:1

The exact application schema is defined by the implementation.

## Checks

### Item Presence

Determine whether each expected item can be identified in the photograph.

### Quantity

Determine whether the visible quantity matches the expected quantity.

### Extra Items

Determine whether an item is visible that is not part of the expected order.

### Evidence Sufficiency

Determine whether the image provides enough evidence for a reliable judgment.

If the evidence is insufficient, return UNCERTAIN rather than assuming PASS.

## Output

The verification result should contain:

- overall verdict
- per-check results
- expected contents
- observed contents
- evidence or observations
- reasoning
- timestamp or request identifier
- model/API status
- pending-review state when appropriate

## Verdicts

### PASS

The available evidence supports the expected packing condition.

### FAIL

The available evidence shows a packing problem such as a missing item, wrong item, incorrect quantity, or extra item.

### UNCERTAIN

The available evidence is insufficient for a reliable decision.

UNCERTAIN is a first-class outcome and must not be converted into PASS.

## Failure Handling

The system should fail open operationally.

If the model or API times out or returns an error:

- preserve the capture
- preserve the request context
- create a decision record
- mark the result as pending review
- do not block the operator

## Evidence

The implementation should make the decision traceable:

Expected contents
    |
    v
Observed contents
    |
    v
Checks performed
    |
    v
Evidence and reasoning
    |
    v
Verdict

A reviewer should be able to understand why the system produced the recorded result.

## Evaluation Plan

Development fixtures are used to verify implementation behaviour.

The final evaluation should use an unseen set that was not used to develop the verification logic.

Report results separately for:

- item presence
- quantity
- extra items
- UNCERTAIN cases
- false positives
- false negatives
- human-labeller agreement
- model/API failures
- important failure modes

## Scope

The initial implementation targets merchant-fulfilled and 3PL outbound packing.

It does not attempt to solve every warehouse inspection problem.

The project does not claim universal catalogue recognition or autonomous operation without human review.

## Success Criteria

The implementation should:

- run repeatably from the documented setup
- produce structured verification results
- preserve evidence needed for review
- distinguish PASS, FAIL, and UNCERTAIN
- fail open on model/API errors
- provide measurable evaluation results
- document known limitations and failure modes

## Non-Goals

This build does not claim:

- perfect product recognition
- universal catalogue coverage
- tamper-proof records
- replacement of all human inspection
- that synthetic repository data represents real Amazon requirements or fees
- production readiness without supporting evaluation evidence
