from collections import Counter
import re

from app.schemas import (
    DetectedItem,
    OrderItem,
    VerificationIssue,
    VerificationResult,
)


def parse_order_lines(order_lines: str) -> dict[str, int]:
    """Convert SKU:quantity;SKU:quantity into a quantity map."""
    quantities = Counter()

    if not order_lines.strip():
        return {}

    for entry in order_lines.split(";"):
        entry = entry.strip()

        if not entry:
            continue

        sku, quantity = entry.rsplit(":", 1)
        sku = sku.strip()
        quantity = int(quantity)

        if not sku:
            raise ValueError("SKU cannot be empty")

        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        quantities[sku] += quantity

    return dict(quantities)


def product_names_match(expected: str, detected: str) -> bool:
    """Check whether expected and detected names refer to the same product."""

    def normalize(name: str) -> str:
        name = name.lower()

        # Normalize common wording variations.
        replacements = {
            "moisturiser": "moisturising",
            "moisturizer": "moisturising",
            "t shirt": "tshirt",
            "t-shirt": "tshirt",
            "tshirt": "tshirt",
        }

        for old, new in replacements.items():
            name = name.replace(old, new)

        # Remove size information.
        name = re.sub(r"\(\s*size\s+[a-z0-9]+\s*\)", " ", name)
        name = re.sub(r"\bsize\s+[a-z0-9]+\b", " ", name)

        # Remove color descriptors.
        name = re.sub(
            r"\b(dark blue|navy blue|blue|black|white|green|purple|red)\b",
            " ",
            name,
        )

        # Remove generic clothing descriptors.
        name = re.sub(
            r"\b(apparel|garment|clothing)\b",
            " ",
            name,
        )

        # Remove common pack-size information.
        name = re.sub(
            r"\b\d+\s*(ml|g|kg|l|pcs|pieces|tea bags)\b",
            " ",
            name,
        )

        # Keep only letters and numbers.
        name = re.sub(r"[^a-z0-9]+", " ", name)

        return " ".join(name.split())

    expected_normalized = normalize(expected)
    detected_normalized = normalize(detected)

    if expected_normalized == detected_normalized:
        return True

    return (
        expected_normalized in detected_normalized
        or detected_normalized in expected_normalized
    )


def compare_order(
    expected: dict[str, int],
    detected: list[DetectedItem],
) -> VerificationResult:
    """Compare expected order quantities with visually detected items."""

    detected_quantities: dict[str, int] = {}

    for item in detected:
        matched_sku = None

        for expected_sku in expected:
            if product_names_match(expected_sku, item.sku):
                matched_sku = expected_sku
                break

        if matched_sku:
            detected_quantities[matched_sku] = (
                detected_quantities.get(matched_sku, 0)
                + item.quantity
            )
        else:
            detected_quantities[item.sku] = (
                detected_quantities.get(item.sku, 0)
                + item.quantity
            )

    expected_items = [
        OrderItem(sku=sku, quantity=quantity)
        for sku, quantity in expected.items()
    ]

    issues: list[VerificationIssue] = []

    # Check expected items.
    for sku, expected_quantity in expected.items():
        detected_quantity = detected_quantities.get(sku, 0)

        if detected_quantity == 0:
            issues.append(
                VerificationIssue(
                    type="missing_item",
                    sku=sku,
                    expected_quantity=expected_quantity,
                    detected_quantity=0,
                    evidence=(
                        f"Expected {expected_quantity} x {sku}, "
                        "but none was detected."
                    ),
                )
            )

        elif detected_quantity != expected_quantity:
            issues.append(
                VerificationIssue(
                    type="quantity_mismatch",
                    sku=sku,
                    expected_quantity=expected_quantity,
                    detected_quantity=detected_quantity,
                    evidence=(
                        f"Expected {expected_quantity} x {sku}, "
                        f"but detected {detected_quantity}."
                    ),
                )
            )

    # Check unexpected items.
    for item in detected:
        matched = any(
            product_names_match(expected_sku, item.sku)
            for expected_sku in expected
        )

        if not matched:
            issues.append(
                VerificationIssue(
                    type="extra_item",
                    sku=item.sku,
                    expected_quantity=0,
                    detected_quantity=item.quantity,
                    evidence=(
                        f"{item.quantity} x {item.sku} was detected "
                        "but was not expected in the order."
                    ),
                )
            )

    # Detect a direct wrong-item substitution.
    missing_issues = [
        issue for issue in issues if issue.type == "missing_item"
    ]

    extra_issues = [
        issue for issue in issues if issue.type == "extra_item"
    ]

    if len(missing_issues) == 1 and len(extra_issues) == 1:
        missing = missing_issues[0]
        extra = extra_issues[0]

        issues = [
            issue
            for issue in issues
            if issue not in (missing, extra)
        ]

        issues.append(
            VerificationIssue(
                type="wrong_item",
                sku=extra.sku,
                expected_quantity=missing.expected_quantity,
                detected_quantity=extra.detected_quantity,
                evidence=(
                    f"Expected {missing.expected_quantity} x {missing.sku}, "
                    f"but detected {extra.detected_quantity} x {extra.sku}."
                ),
            )
        )

    verdict = "seal" if not issues else "stop_and_fix"

    return VerificationResult(
        verdict=verdict,
        expected_items=expected_items,
        detected_items=detected,
        issues=issues,
    )


def verify_image_order(
    order_lines: str,
    image_path: str,
) -> tuple[VerificationResult | None, str]:
    """
    Detect products from an image and compare them with the expected order.

    Returns:
        A tuple containing:
        - VerificationResult when detection succeeds
        - status from the vision detector
    """
    from app.vision import detect_items_from_image

    expected = parse_order_lines(order_lines)

    detected, status = detect_items_from_image(image_path)

    if status != "success":
        return None, status

    result = compare_order(
        expected=expected,
        detected=detected,
    )

    return result, status