# PR/FAQ

## Press Release

### Pack Manager adds an evidence-backed check before an outbound box is sealed

Pack Manager is a photograph-based verification agent for merchant-fulfilled and 3PL outbound orders.

Before a box is sealed, the operator provides the order lines and a photograph of the open box. Pack Manager compares the expected contents with what can be identified in the photograph and checks:

- whether each expected item is present
- whether quantities appear correct
- whether an unexpected item is present
- whether the evidence is sufficient to make a reliable judgment

The result is recorded as PASS, FAIL, or UNCERTAIN, together with the evidence and reasoning used for the decision.

Pack Manager is deliberately designed around evidence rather than a binary automation claim. When the image or model response is insufficient, the system records an UNCERTAIN result instead of treating uncertainty as a successful verification.

The system also follows a fail-open operational model. A model error or timeout should not prevent the capture from being recorded. The resulting record can remain pending review so the warehouse process can continue.

The initial target is sellers and 3PL operators that do not have a dedicated automated packing station or hardware budget. The product is not intended to claim that vision-based verification works reliably for every product catalogue or warehouse environment.

The evaluation will use an unseen set and report results separately for each check, including false positives, false negatives, UNCERTAIN cases, and observed failure modes.

---

## FAQ

### What exactly does Pack Manager verify?

It verifies the contents visible in an open outbound box against the expected order lines. The intended checks are item presence, quantity, extra items, and evidence sufficiency.

### Does Pack Manager guarantee that the box is correct?

No.

The system provides an evidence-backed automated judgment. It does not guarantee that every physical item was correctly identified.

### What happens when the image is unclear?

The system should return UNCERTAIN when the available evidence is insufficient for a reliable judgment. The capture should still be retained for review.

### What happens when the model fails or times out?

The operational workflow should fail open. The capture and decision record should still be saved, with the result marked pending rather than blocking the operator.

### Can it recognize every product?

That is an open question.

The core assumption being tested is whether a vision model can identify products and verify contents across a long-tail catalogue without per-SKU training. The evaluation should expose where this assumption fails rather than hiding those failures.

### What about visually similar products?

Visually similar products are a known failure mode. A system that confuses two similar products can produce an incorrect PASS or FAIL. The evaluation therefore needs to record such errors separately rather than reporting only an aggregate accuracy number.

### Why not just have a human check every box?

Manual inspection is the existing fallback, but checking every box takes operator time. Pack Manager is intended to test whether a lightweight camera-and-model workflow can reduce the amount of routine checking while retaining human review for uncertain cases.

The project does not assume that automation should replace every human decision.

### Why target sellers and 3PLs rather than FBA?

The problem statement specifically targets merchant-fulfilled and 3PL outbound orders. In fully FBA workflows, Amazon handles the packing operation, so the seller does not control this packing step.

### What happens if the model confidently makes the wrong decision?

That is one of the most important risks.

A confident incorrect PASS could allow a mis-ship to leave the facility. A confident incorrect FAIL could create unnecessary manual work. The evaluation therefore needs to measure false positives and false negatives separately and identify the conditions that produce them.

### Does a content hash make the record tamper-proof?

No.

A content hash can help identify whether the hashed content changed, but it does not by itself provide an immutable or tamper-evident record. The implementation should not claim stronger guarantees than it actually provides.

### Does Pack Manager use the sample CSV as authoritative Amazon rules?

No.

The repository sample data is explicitly synthetic. It can be used to design the schema and workflow, but its requirement flags and fee amounts must not be treated as real Amazon rules or fees.

### What would make us stop?

If evaluation on unseen data shows that the system cannot reliably distinguish correct contents from common packing errors, or if its false-positive and false-negative behaviour creates unacceptable operational risk, the vision-based approach should not be treated as ready for autonomous sealing decisions.

That result would be a useful finding rather than something to hide.

### What would we measure before wider use?

At minimum:

- per-check false positives
- per-check false negatives
- UNCERTAIN rate
- agreement between independent human labels
- model-versus-human disagreements
- failure modes by image/product condition
- latency and model/API failures
- whether every decision leaves sufficient evidence for later review

### What is deliberately not claimed?

Pack Manager does not claim:

- perfect product recognition
- universal catalogue coverage
- autonomous operation without human fallback
- tamper-proof records
- that the synthetic sample data represents real Amazon policies or fees
- that the approach is ready for every warehouse environment


