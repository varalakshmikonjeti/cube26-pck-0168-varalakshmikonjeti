# Pack Manager Contracts

This directory contains the contracts that define the evidence and decision information produced by Pack Manager.

## Files

### evidence-record.md

Defines the evidence record produced by a verification.

It describes:

- record identity
- expected contents
- observed contents
- verification checks
- verdicts
- reasoning and evidence
- overrides
- tenant isolation
- downstream interoperability

### decision-schema.md

Defines the structured decision returned by Pack Manager.

It describes:

- required decision fields
- overall verdict values
- per-check results
- expected contents
- observed contents
- evidence
- reasoning
- model/API status
- pending review
- tenant isolation

### override-record.md

Defines how a human override is recorded.

It preserves:

- original automated verdict
- new verdict
- override reason
- operator identity
- override timestamp
- original evidence and reasoning

## Shared Rules

The contracts follow these project rules:

- `UNCERTAIN` is a first-class outcome.
- Insufficient evidence must not be converted into `PASS`.
- Model/API failures should fail open operationally.
- Captures and decision records should be preserved when review is required.
- Automated decisions must remain auditable after an operator override.
- Tenant isolation must be preserved.
- Synthetic repository data must not be treated as authoritative Amazon policy or fee data.
- The system must not claim tamper-proof or immutable records unless such guarantees are actually implemented and demonstrated.

## Downstream Use

Downstream stages should be able to consume the Pack Manager decision and evidence without requiring access to internal model prompts or implementation-specific details.

The contracts describe the information that should be preserved. They do not by themselves guarantee persistence, immutability, security, or production reliability.