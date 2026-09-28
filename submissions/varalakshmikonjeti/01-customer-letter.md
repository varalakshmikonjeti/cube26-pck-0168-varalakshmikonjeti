# Customer Letter

## To: A Seller or 3PL Packing Operations Team

Your team has to decide whether an outbound order contains the right items and quantities before the box is sealed.

Today, that check can depend on a person looking into the open box and making a quick judgment. A missed item, wrong item, incorrect quantity, or extra item can become a mis-shipment and create downstream returns, replacements, refunds, or customer disputes.

Pack Manager is designed for merchant-fulfilled and 3PL outbound orders. It takes a photograph of the open box together with the order lines and records what the system found, which checks were performed, the evidence used, and a verdict:

- PASS — the evidence supports sealing the box.
- FAIL — the evidence shows a packing problem that should be fixed.
- UNCERTAIN — the photograph or evidence is insufficient for a reliable judgment.

The important part is not only the verdict. The system leaves a record of what was expected, what was observed, what checks were performed, and why the verdict was produced.

The first version is intentionally narrow. It does not claim to replace every warehouse inspection or work reliably across every possible product catalogue. Its purpose is to test whether photograph-based verification can provide useful evidence for outbound packing without requiring a dedicated hardware station.

The system should fail open operationally: if the model cannot make a reliable decision, the capture and evidence record should still be saved and marked for review rather than blocking the packing operation.

The key question for evaluation is therefore measurable: on an unseen evaluation set, how accurately can the system identify missing items, quantity mismatches, extra items, and wrong items, and how often does it correctly identify cases where the evidence is insufficient?

That evidence—not a claim of perfect automation—will determine whether the approach is useful.
