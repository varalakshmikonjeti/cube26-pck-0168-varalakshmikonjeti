from typing import Any, Dict, List

from .config import settings
from .errors import ModelVerificationError
from .model_client import ModelClient
from .models import (
    ExpectedContent,
    ObservedContent,
    VerificationRequest,
    VerificationResult,
    VerificationChecks,
)
from .verifier import determine_overall_verdict


class VerificationPipeline:
    """
    Coordinates image verification and decision construction.

    The pipeline keeps model/provider concerns separate from the
    evidence and verdict rules used by Pack Manager.
    """

    def __init__(
        self,
        model_client: ModelClient | None = None,
    ) -> None:
        self.model_client = model_client or ModelClient(
            model_name=settings.model_name
        )

    def run(
        self,
        request: VerificationRequest,
    ) -> VerificationResult:
        expected_contents: List[ExpectedContent] = request.expected_contents

        expected_for_model: List[Dict[str, Any]] = [
            {
                "sku": item.sku,
                "quantity": item.quantity,
            }
            for item in expected_contents
        ]

        try:
            model_result = self.model_client.verify_image(
                image_reference=request.image_reference,
                expected_contents=expected_for_model,
            )
        except Exception as exc:
            return self._pending_review(
                request=request,
                error={
                    "type": "model_exception",
                    "message": str(exc),
                },
            )

        status = model_result.get("status", "error")

        if status in {"error", "timeout"}:
            return self._pending_review(
                request=request,
                reasoning=model_result.get(
                    "reasoning",
                    "Automated verification could not be completed.",
                ),
                evidence=model_result.get("evidence", []),
                error=model_result.get("error"),
                model_status=status,
            )

        observed_contents = self._parse_observed_contents(
            model_result.get("observed_contents", [])
        )

        evidence = model_result.get("evidence", [])
        reasoning = model_result.get("reasoning", "")

        evidence_sufficient = bool(
            model_result.get("evidence_sufficient", True)
        )

        checks = self._evaluate_checks(
            request=request,
            observed_contents=observed_contents,
            evidence_sufficient=evidence_sufficient,
        )

        verdict = determine_overall_verdict(
            checks=checks,
            model_status=status,
        )

        return VerificationResult(
            record_id=request.unit_id,
            unit_id=request.unit_id,
            org_id=request.org_id,
            created_at=request.capture_timestamp
            or request.unit_id,
            overall_verdict=verdict,
            expected_contents=expected_contents,
            observed_contents=observed_contents,
            checks=checks,
            evidence=evidence,
            reasoning=reasoning,
            model_status=status,
            pending_review=verdict == "PENDING_REVIEW",
        )

    def _parse_observed_contents(
        self,
        items: List[Dict[str, Any]],
    ) -> List[ObservedContent]:
        observed: List[ObservedContent] = []

        for item in items:
            observed.append(
                ObservedContent(
                    description=str(
                        item.get("description", "identified item")
                    ),
                    quantity=item.get("quantity"),
                    sku=item.get("sku"),
                    confidence=item.get("confidence"),
                )
            )

        return observed

    def _evaluate_checks(
        self,
        request: VerificationRequest,
        observed_contents: List[ObservedContent],
        evidence_sufficient: bool,
    ) -> VerificationChecks:
        if not evidence_sufficient:
            return VerificationChecks(
                item_presence="UNCERTAIN",
                quantity="UNCERTAIN",
                extra_items="UNCERTAIN",
                evidence_sufficiency="UNCERTAIN",
            )

        expected = {
            item.sku: item.quantity
            for item in request.expected_contents
        }

        observed: Dict[str, int] = {}

        for item in observed_contents:
            if item.sku and item.quantity is not None:
                observed[item.sku] = (
                    observed.get(item.sku, 0) + item.quantity
                )

        missing = set(expected) - set(observed)
        extra = set(observed) - set(expected)

        item_presence = "PASS" if not missing else "FAIL"
        extra_items = "PASS" if not extra else "FAIL"

        quantity_correct = (
            not missing
            and not extra
            and all(
                observed[sku] == quantity
                for sku, quantity in expected.items()
            )
        )

        quantity = "PASS" if quantity_correct else "FAIL"

        return VerificationChecks(
            item_presence=item_presence,
            quantity=quantity,
            extra_items=extra_items,
            evidence_sufficiency="PASS",
        )

    def _pending_review(
        self,
        request: VerificationRequest,
        reasoning: str = "",
        evidence: List[Dict[str, Any]] | None = None,
        error: Dict[str, Any] | None = None,
        model_status: str = "error",
    ) -> VerificationResult:
        return VerificationResult(
            record_id=request.unit_id,
            unit_id=request.unit_id,
            org_id=request.org_id,
            created_at=request.capture_timestamp
            or request.unit_id,
            overall_verdict="PENDING_REVIEW",
            expected_contents=request.expected_contents,
            observed_contents=[],
            checks=VerificationChecks(
                item_presence="UNCERTAIN",
                quantity="UNCERTAIN",
                extra_items="UNCERTAIN",
                evidence_sufficiency="UNCERTAIN",
            ),
            evidence=evidence or [],
            reasoning=reasoning
            or "Automated verification requires human review.",
            model_status=model_status,
            pending_review=True,
            error=error,
        )