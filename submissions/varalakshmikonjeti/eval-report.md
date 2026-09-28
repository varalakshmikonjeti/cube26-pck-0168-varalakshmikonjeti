# Pack Manager · Evaluation Report

## Purpose

This evaluation report documents the verification checks, test coverage,
agreement approach, and known failure modes for the Pack Manager workflow.

The system is designed to verify expected package contents against observed
contents from image/model evidence and to avoid making an automated decision
when the evidence or model result is insufficient.

## Evaluation Method

Evaluation is based on structured verification cases covering:

1. Expected item presence
2. Expected quantities
3. Extra items
4. Evidence sufficiency
5. Model/API failure handling
6. Tenant isolation
7. Headless runner execution
8. Structured downstream record generation

The current automated test suite provides deterministic software-level
coverage for these behaviours.

The latest completed test run contained 11 tests and all 11 passed.

## Two-Labeller Agreement

Two independent human labellers should review the same evaluation image set
using the agreed decision contract.

Each labeller should independently record:

- Expected SKU
- Expected quantity
- Observed SKU
- Observed quantity
- Item presence verdict
- Quantity verdict
- Extra-item verdict
- Evidence-sufficiency verdict
- Overall operational verdict

Agreement should be calculated per check as:

agreement = matching labels / total labelled cases

The evaluation should report agreement separately for:

- Item presence
- Quantity
- Extra items
- Evidence sufficiency
- Overall verdict

No human agreement percentage is claimed here because a completed
two-labeller dataset has not been supplied.

## Per-Check False Positives and False Negatives

For each verification check, the evaluation should compare the automated
result with the agreed human reference label.

### Item Presence

False positive:
The system marks the expected item as present when the reference label
indicates that it is missing or cannot be reliably established.

False negative:
The system marks the expected item as missing when the reference label
confirms that it is present.

### Quantity

False positive:
The system marks quantity as correct when the reference label indicates
that the quantity is incorrect.

False negative:
The system marks quantity as incorrect when the reference label confirms
the expected quantity.

### Extra Items

False positive:
The system reports an extra item when the reference label confirms that
the item belongs to the expected contents.

False negative:
The system fails to report an extra item that the reference label confirms
is present.

### Evidence Sufficiency

False positive:
The system treats evidence as sufficient when human review determines
that the image or model evidence is inadequate.

False negative:
The system marks evidence as insufficient when human review determines
that the evidence is sufficient.

### Overall Verdict

The overall verdict should be evaluated against the agreed human reference
decision after the individual checks have been reviewed.

No numerical false-positive or false-negative rate is claimed until an
unseen labelled evaluation set is available.

## Current Software Test Coverage

The automated tests currently cover:

- Headless agent execution
- Model-client behaviour
- Verification runner behaviour
- Tenant isolation
- Existing verification logic
- Structured verification records
- Model-unavailable handling

Latest result:

11 passed.

## Known Failure Modes

### Model Provider Unavailable

If no model provider is configured, the system does not invent observations.
It returns an explicit model error and produces PENDING_REVIEW.

### Model/API Exception

If the model boundary raises an exception, the verification is converted
to PENDING_REVIEW rather than producing an unsupported PASS or FAIL.

### Insufficient Evidence

If evidence is marked insufficient, the individual verification checks
become UNCERTAIN and the workflow requires review.

### Ambiguous Image Evidence

Low-quality, obstructed, cropped, or otherwise ambiguous images may prevent
reliable identification or counting of package contents.

### SKU Recognition Errors

A vision model may confuse visually similar products or fail to identify a
SKU from an image.

### Quantity Estimation Errors

Occlusion, overlapping objects, packaging, or poor image quality may cause
incorrect quantity estimation.

### Extra-Item Detection Errors

An item may be missed or incorrectly classified as extra when visual
evidence is incomplete.

### Tenant Isolation Errors

A record must never be returned or treated as belonging to a different
organisation. Tenant-specific storage and validation are therefore part of
the tested workflow.

## Safety Behaviour

The system is intentionally conservative when automated evidence is
unavailable.

It does not fabricate observations, evidence, or successful verification.

When automated verification cannot be completed safely, the result is:

PENDING_REVIEW

This preserves a clear boundary between automated evidence and human
operational review.

## Evaluation Limitations

The current repository does not contain a completed labelled image benchmark
with independent labels from two human labellers.

Therefore this report does not claim:

- model accuracy
- precision
- recall
- F1 score
- human-labeller agreement percentage
- production readiness

Those measurements should be added after evaluation on an unseen,
representative dataset.

## Recommended Evaluation Dataset

The evaluation set should include:

- Correct packages
- Missing items
- Incorrect quantities
- Extra items
- Multiple expected SKUs
- Visually similar SKUs
- Occluded items
- Poor lighting
- Partial views
- Blurry images
- Empty or invalid image references
- Ambiguous evidence

The dataset should remain separate from development examples where possible
so that the evaluation measures performance on unseen cases.

## Release Gate

The system should not be treated as ready for autonomous sealing decisions
unless unseen-data evaluation demonstrates that common packing errors can be
distinguished reliably enough for the intended operational workflow.

Until then, uncertain or unavailable automated verification remains subject
to human review.
