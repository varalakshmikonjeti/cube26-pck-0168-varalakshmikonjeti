from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImageEvidence:
    """
    Represents the submitted packing image and basic evidence status.
    """

    reference: str
    available: bool
    usable: bool
    limitation: str | None = None


def inspect_image_reference(reference: str) -> ImageEvidence:
    """
    Inspect a local image reference when possible.

    Remote/object-storage references are treated as references that require
    an external storage layer to resolve them. This function does not claim
    that such an image was successfully accessed.
    """
    if not reference or not reference.strip():
        return ImageEvidence(
            reference=reference,
            available=False,
            usable=False,
            limitation="Image reference is missing.",
        )

    reference = reference.strip()
    path = Path(reference)

    if path.exists() and path.is_file():
        if path.stat().st_size == 0:
            return ImageEvidence(
                reference=reference,
                available=True,
                usable=False,
                limitation="Image file is empty.",
            )

        return ImageEvidence(
            reference=reference,
            available=True,
            usable=True,
        )

    if reference.startswith(("http://", "https://", "s3://")):
        return ImageEvidence(
            reference=reference,
            available=True,
            usable=False,
            limitation=(
                "Image reference requires an external storage or HTTP "
                "access layer before it can be inspected."
            ),
        )

    return ImageEvidence(
        reference=reference,
        available=False,
        usable=False,
        limitation="Referenced image was not found.",
    )