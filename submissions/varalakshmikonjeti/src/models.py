from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


VERDICTS = {"PASS", "FAIL", "UNCERTAIN", "PENDING_REVIEW"}
CHECK_VERDICTS = {"PASS", "FAIL", "UNCERTAIN"}


@dataclass
class ExpectedContent:
    sku: str
    quantity: int


@dataclass
class ObservedContent:
    description: str
    quantity: Optional[int] = None
    sku: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class CheckResults:
    item_presence: str
    quantity: str
    extra_items: str
    evidence_sufficiency: str

    def __post_init__(self) -> None:
        values = {
            "item_presence": self.item_presence,
            "quantity": self.quantity,
            "extra_items": self.extra_items,
            "evidence_sufficiency": self.evidence_sufficiency,
        }

        invalid = {
            name: value
            for name, value in values.items()
            if value not in CHECK_VERDICTS
        }

        if invalid:
            raise ValueError(f"Invalid check verdicts: {invalid}")


VerificationChecks = CheckResults


@dataclass
class VerificationRequest:
    unit_id: str
    org_id: str
    expected_contents: List[ExpectedContent]
    image_reference: str
    capture_timestamp: Optional[str] = None
    channel: Optional[str] = None
    operator_id: Optional[str] = None


@dataclass
class VerificationDecision:
    record_id: str
    unit_id: str
    org_id: str
    created_at: str
    overall_verdict: str
    expected_contents: List[ExpectedContent]
    observed_contents: List[ObservedContent]
    checks: CheckResults
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    reasoning: str = ""
    model_status: str = "completed"
    pending_review: bool = False
    error: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        if self.overall_verdict not in VERDICTS:
            raise ValueError(
                f"Invalid overall verdict: {self.overall_verdict}"
            )

        if self.overall_verdict == "PENDING_REVIEW":
            self.pending_review = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "unit_id": self.unit_id,
            "org_id": self.org_id,
            "created_at": self.created_at,
            "overall_verdict": self.overall_verdict,
            "expected_contents": [
                {
                    "sku": item.sku,
                    "quantity": item.quantity,
                }
                for item in self.expected_contents
            ],
            "observed_contents": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "sku": item.sku,
                    "confidence": item.confidence,
                }
                for item in self.observed_contents
            ],
            "checks": {
                "item_presence": self.checks.item_presence,
                "quantity": self.checks.quantity,
                "extra_items": self.checks.extra_items,
                "evidence_sufficiency": self.checks.evidence_sufficiency,
            },
            "evidence": self.evidence,
            "reasoning": self.reasoning,
            "model_status": self.model_status,
            "pending_review": self.pending_review,
            "error": self.error,
        }


VerificationResult = VerificationDecision


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()