from typing import Any, Dict, List

from .models import VerificationRequest


class ValidationError(ValueError):
    """Raised when a verification request does not satisfy the input contract."""


def validate_verification_request(
    request: VerificationRequest,
) -> List[str]:
    """
    Validate the required fields for a Pack Manager verification request.

    Returns a list of validation errors. An empty list means the request
    satisfies the basic input requirements.
    """
    errors: List[str] = []

    if not request.unit_id or not request.unit_id.strip():
        errors.append("unit_id is required")

    if not request.org_id or not request.org_id.strip():
        errors.append("org_id is required")

    if not request.image_reference or not request.image_reference.strip():
        errors.append("image_reference is required")

    if not request.expected_contents:
        errors.append("expected_contents must contain at least one item")

    for index, item in enumerate(request.expected_contents):
        if not item.sku or not item.sku.strip():
            errors.append(f"expected_contents[{index}].sku is required")

        if not isinstance(item.quantity, int):
            errors.append(
                f"expected_contents[{index}].quantity must be an integer"
            )
        elif item.quantity <= 0:
            errors.append(
                f"expected_contents[{index}].quantity must be greater than zero"
            )

    return errors


def validate_request_or_raise(
    request: VerificationRequest,
) -> None:
    """Validate a request and raise ValidationError when invalid."""
    errors = validate_verification_request(request)

    if errors:
        raise ValidationError("; ".join(errors))


def validate_raw_request(data: Dict[str, Any]) -> List[str]:
    """
    Validate a raw request dictionary before constructing a
    VerificationRequest object.
    """
    errors: List[str] = []

    if not isinstance(data, dict):
        return ["verification request must be an object"]

    if not data.get("unit_id"):
        errors.append("unit_id is required")

    if not data.get("org_id"):
        errors.append("org_id is required")

    if not data.get("image_reference"):
        errors.append("image_reference is required")

    expected_contents = data.get("expected_contents")

    if not isinstance(expected_contents, list) or not expected_contents:
        errors.append("expected_contents must be a non-empty list")
        return errors

    for index, item in enumerate(expected_contents):
        if not isinstance(item, dict):
            errors.append(
                f"expected_contents[{index}] must be an object"
            )
            continue

        sku = item.get("sku")
        quantity = item.get("quantity")

        if not isinstance(sku, str) or not sku.strip():
            errors.append(
                f"expected_contents[{index}].sku is required"
            )

        if not isinstance(quantity, int) or isinstance(quantity, bool):
            errors.append(
                f"expected_contents[{index}].quantity must be an integer"
            )
        elif quantity <= 0:
            errors.append(
                f"expected_contents[{index}].quantity must be greater than zero"
            )

    return errors