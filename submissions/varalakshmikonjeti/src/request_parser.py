from typing import Any, Dict, List

from .models import ExpectedContent, VerificationRequest


def parse_verification_request(
    payload: Dict[str, Any],
) -> VerificationRequest:
    """
    Convert a JSON-compatible request payload into a
    VerificationRequest object.
    """
    expected_contents: List[ExpectedContent] = []

    for item in payload.get("expected_contents", []):
        expected_contents.append(
            ExpectedContent(
                sku=str(item["sku"]),
                quantity=int(item["quantity"]),
            )
        )

    return VerificationRequest(
        unit_id=str(payload["unit_id"]),
        org_id=str(payload["org_id"]),
        expected_contents=expected_contents,
        image_reference=str(payload["image_reference"]),
        capture_timestamp=payload.get("capture_timestamp"),
        channel=payload.get("channel"),
        operator_id=payload.get("operator_id"),
    )


def request_to_payload(
    request: VerificationRequest,
) -> Dict[str, Any]:
    """
    Convert a VerificationRequest into a JSON-compatible dictionary.
    """
    return {
        "unit_id": request.unit_id,
        "org_id": request.org_id,
        "expected_contents": [
            {
                "sku": item.sku,
                "quantity": item.quantity,
            }
            for item in request.expected_contents
        ],
        "image_reference": request.image_reference,
        "capture_timestamp": request.capture_timestamp,
        "channel": request.channel,
        "operator_id": request.operator_id,
    }