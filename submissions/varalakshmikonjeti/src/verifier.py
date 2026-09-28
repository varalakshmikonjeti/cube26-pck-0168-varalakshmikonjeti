from typing import Any, Dict, List

from .models import (
    CheckResults,
    ObservedContent,
    VerificationDecision,
    VerificationRequest,
)


VALID_CHECK_RESULTS = {"PASS", "FAIL", "UNCERTAIN"}


def _normalise_observed_contents(
    observed_contents: List[ObservedContent],
) -> List[Dict[str, Any]]:
    """Convert observed model results into downstream-safe dictionaries."""
    return [
        {
            "description": item.description,
            "quantity": item.quantity,
            "sku": item.sku,
            "confidence": item.confidence,
        }
        for item in observed_contents
    ]


def evaluate_checks(
    request: VerificationRequest,
    observed_contents: List[ObservedContent],
    evidence_sufficient: bool,
) -> CheckResults:
    """
    Compare expected contents with observed image contents.

    The function deliberately does not assume that an expected item was
    observed merely because it exists in the order.
    """
    if not evidence_sufficient:
        return CheckResults(
            item_presence="UNCERTAIN",
            quantity="UNCERTAIN",
            extra_items="UNCERTAIN",
            evidence_sufficiency="UNCERTAIN",
        )

    expected_by_sku = {
        item.sku: item.quantity
        for item in request.expected_contents
    }

    observed_by_sku: Dict[str, int] = {}

    for item in observed_contents:
        if item.sku:
            observed_by_sku[item.sku] = (
                observed_by_sku.get(item.sku, 0) + item.quantity
            )

    expected_skus = set(expected_by_sku)
    observed_skus = set(observed_by_sku)

    missing_skus = expected_skus - observed_skus
    extra_skus = observed_skus - expected_skus

    item_presence = "PASS" if not missing_skus else "FAIL"

    quantity_correct = (
        not missing_skus
        and not extra_skus
        and all(
            observed_by_sku[sku] == expected_quantity
            for sku, expected_quantity in expected_by_sku.items()
        )
    )

    quantity = "PASS" if quantity_correct else "FAIL"

    extra_items = "PASS" if not extra_skus else "FAIL"

    return CheckResults(
        item_presence=item_presence,
        quantity=quantity,
        extra_items=extra_items,
        evidence_sufficiency="PASS",
    )


def determine_overall_verdict(
    checks: CheckResults,
    model_status: str = "completed",
) -> str:
    """
    Determine the overall Pack Manager verdict from check results.

    Model/API failures take precedence and produce PENDING_REVIEW.
    """
    if model_status in {"error", "timeout"}:
        return "PENDING_REVIEW"

    values = {
        checks.item_presence,
        checks.quantity,
        checks.extra_items,
        checks.evidence_sufficiency,
    }

    if "FAIL" in values:
        return "FAIL"

    if "UNCERTAIN" in values:
        return "UNCERTAIN"

    return "PASS"


def build_decision(
    request: VerificationRequest,
    observed_contents: List[ObservedContent],
    evidence: List[Dict[str, Any]],
    reasoning: str,
    evidence_sufficient: bool,
    model_status: str = "completed",
    error: str | None = None,
) -> VerificationDecision:
    """
    Build the structured decision returned by Pack Manager.

    This function keeps the output aligned with the documented contracts.
    """
    checks = evaluate_checks(
        request=request,
        observed_contents=observed_contents,
        evidence_sufficient=evidence_sufficient,
    )

    overall_verdict = determine_overall_verdict(
        checks=checks,
        model_status=model_status,
    )

    pending_review = overall_verdict == "PENDING_REVIEW"

    if pending_review and not reasoning:
        reasoning = (
            "Automated verification could not be completed because "
            "the model/API operation failed."
        )

    decision = VerificationDecision(
        record_id=request.record_id,
        unit_id=request.unit_id,
        org_id=request.org_id,
        created_at=request.created_at,
        expected_contents=request.expected_contents,
        observed_contents=observed_contents,
        checks=checks,
        overall_verdict=overall_verdict,
        evidence=evidence,
        reasoning=reasoning,
        model_status=model_status,
        pending_review=pending_review,
        error=error,
    )

    return decision