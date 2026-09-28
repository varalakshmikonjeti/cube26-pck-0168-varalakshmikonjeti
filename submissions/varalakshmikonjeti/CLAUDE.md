# Pack Manager Engineering Constraints

## Purpose

Pack Manager verifies the contents of an open outbound box against the expected order lines for merchant-fulfilled and 3PL orders.

## Hard Rules

1. Preserve tenant isolation. Data belonging to one organisation must never be accessible to another organisation.

2. Batch model calls. Use one model call per verification unit carrying all required checks rather than one call per check.

3. Fail open operationally. Model errors and timeouts must not block the packing workflow. Preserve the capture and create a pending record for review.

4. Treat UNCERTAIN as a first-class verdict. Do not convert insufficient evidence into PASS.

5. Look up authoritative requirements where required. Synthetic repository data must not be treated as real Amazon policy or fee data.

6. Preserve decision evidence. A reviewer should be able to understand what was expected, what was observed, what checks were performed, what verdict was produced, and why.

7. Preserve overrides as data. If an operator changes an automated verdict, retain the original verdict, new verdict, and reason.

8. Report evaluation honestly. Report results per check, including false positives, false negatives, UNCERTAIN cases, human agreement, and failure modes.

## Evidence Rules

Every verification should preserve enough information to support later review.

The record should make it possible to trace:

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
Final verdict

## Verdicts

PASS means the available evidence supports the condition.

FAIL means the available evidence shows that the condition is not met.

UNCERTAIN means the available evidence is insufficient for a reliable judgment.

UNCERTAIN is not a low-confidence PASS.

## Forbidden Claims

Do not claim:

- perfect product recognition
- universal catalogue coverage
- guaranteed correctness
- autonomous operation without human fallback
- tamper-proof or immutable records unless actually implemented and demonstrated
- that a content hash alone makes a record tamper-proof
- that synthetic repository data represents real Amazon rules or fees
- production reliability that has not been measured

## Evaluation Discipline

Use an unseen evaluation set where possible.

Document:

- evaluation methodology
- per-check results
- false positives
- false negatives
- UNCERTAIN cases
- human-labeller agreement
- model-versus-human disagreements
- failure modes
- model/API failures
- latency
- evidence completeness

Do not hide failures behind a single aggregate accuracy number.

## Scope

The initial target is merchant-fulfilled and 3PL outbound packing.

Fully FBA workflows are outside the intended packing workflow because the seller does not control the FBA packing step.

The system is intended to assist packing verification, not to claim that every warehouse or product catalogue can be reliably automated.

