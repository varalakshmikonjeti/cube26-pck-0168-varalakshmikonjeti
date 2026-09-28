from datetime import datetime, timezone
from typing import Any, Dict, List

from .models import (
    ObservedContent,
    VerificationDecision,
    VerificationRequest,
)
from .validation import validate_request_or_raise
from .verifier import build_decision


class PackManagerService:
    """
    Application service coordinating Pack Manager verification.

    The service keeps validation, evidence handling, decision construction,
    and model/API failure handling in one downstream-facing workflow.
    """

    def verify(
        self,
        request: VerificationRequest,
        observed_contents: List[ObservedContent] | None = None,
        evidence: List[Dict[str, Any]] | None = None,
        evidence_sufficient: bool = False,
        reasoning: str = "",
        model_status: str = "completed",
        error: str | None = None,
    ) -> VerificationDecision:
        """
        Execute one Pack Manager verification.

        Model/API calls are intentionally supplied as inputs to this service
        so the core workflow remains testable without requiring a live model.
        """
        validate_request_or_raise(request)

        observed_contents = observed_contents or []
        evidence = evidence or []

        if model_status in {"error", "timeout"}:
            evidence_sufficient = False

        if not reasoning:
            reasoning = self._default_reasoning(
                evidence_sufficient=evidence_sufficient,
                model_status=model_status,
                error=error,
            )

        return build_decision(
            request=request,
            observed_contents=observed_contents,
            evidence=evidence,
            reasoning=reasoning,
            evidence_sufficient=evidence_sufficient,
            model_status=model_status,
            error=error,
        )

    @staticmethod
    def create_request_metadata() -> Dict[str, str]:
        """Return basic metadata for a verification execution."""
        return {
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def _default_reasoning(
        evidence_sufficient: bool,
        model_status: str,
        error: str | None,
    ) -> str:
        if model_status in {"error", "timeout"}:
            if error:
                return (
                    "Automated verification could not be completed because "
                    f"the model/API operation failed: {error}"
                )

            return (
                "Automated verification could not be completed because "
                "the model/API operation failed."
            )

        if not evidence_sufficient:
            return (
                "The available image evidence is insufficient for a "
                "reliable automated verification."
            )

        return (
            "The verification decision was produced from the available "
            "image evidence and expected order contents."
        )