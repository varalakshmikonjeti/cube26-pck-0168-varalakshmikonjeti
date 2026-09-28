from datetime import datetime, timezone
from typing import Any, Dict


VALID_VERDICTS = {"PASS", "FAIL", "UNCERTAIN"}


def create_override(
    record_id: str,
    unit_id: str,
    org_id: str,
    original_verdict: str,
    new_verdict: str,
    override_reason: str,
    operator_id: str,
) -> Dict[str, Any]:
    """
    Create an auditable operator override record.

    The original automated verdict is preserved and is never silently
    replaced.
    """
    if original_verdict not in {
        "PASS",
        "FAIL",
        "UNCERTAIN",
        "PENDING_REVIEW",
    }:
        raise ValueError(
            f"Invalid original verdict: {original_verdict}"
        )

    if new_verdict not in VALID_VERDICTS:
        raise ValueError(
            f"Invalid new verdict: {new_verdict}"
        )

    if not override_reason.strip():
        raise ValueError("Override reason is required")

    if not operator_id.strip():
        raise ValueError("Operator identifier is required")

    if not org_id.strip():
        raise ValueError("Organisation identifier is required")

    return {
        "record_id": record_id,
        "unit_id": unit_id,
        "org_id": org_id,
        "original_verdict": original_verdict,
        "new_verdict": new_verdict,
        "override_reason": override_reason,
        "operator_id": operator_id,
        "override_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }