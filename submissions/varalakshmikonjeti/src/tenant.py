from typing import Any, Dict

from .errors import TenantIsolationError


def validate_tenant(
    expected_org_id: str,
    actual_org_id: str,
) -> None:
    """
    Ensure that an operation stays within the requested organisation.
    """
    if not expected_org_id:
        raise TenantIsolationError(
            "Organisation identifier is required"
        )

    if not actual_org_id:
        raise TenantIsolationError(
            "Organisation context is missing"
        )

    if expected_org_id != actual_org_id:
        raise TenantIsolationError(
            "Cross-tenant access is not permitted"
        )


def validate_record_tenant(
    org_id: str,
    record: Dict[str, Any],
) -> None:
    """
    Verify that a stored record belongs to the requested organisation.
    """
    record_org_id = record.get("org_id")

    validate_tenant(
        expected_org_id=org_id,
        actual_org_id=record_org_id,
    )