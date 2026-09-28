from typing import Any, Dict

from .models import VerificationResult


def decision_to_record(
    result: VerificationResult,
) -> Dict[str, Any]:
    """
    Convert a verification result into the downstream record format.
    """
    return result.to_dict()


def validate_record_shape(
    record: Dict[str, Any],
) -> None:
    """
    Validate that the downstream record contains the required fields.
    """
    required_fields = {
        "record_id",
        "unit_id",
        "org_id",
        "created_at",
        "overall_verdict",
        "expected_contents",
        "observed_contents",
        "checks",
        "evidence",
        "reasoning",
        "model_status",
        "pending_review",
    }

    missing = required_fields - set(record)

    if missing:
        raise ValueError(
            f"Decision record is missing required fields: "
            f"{sorted(missing)}"
        )


def prepare_downstream_record(
    result: VerificationResult,
) -> Dict[str, Any]:
    """
    Build and validate the structured record returned downstream.
    """
    record = decision_to_record(result)

    validate_record_shape(record)

    return record