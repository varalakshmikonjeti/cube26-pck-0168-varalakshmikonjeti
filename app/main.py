from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import shutil
import tempfile

from app.schemas import DetectedItem
from app.verification import compare_order, parse_order_lines, verify_image_order

app = FastAPI(title="Pack Manager")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/verify")
def verify_order(
    order_lines: str,
    detected_items: list[DetectedItem],
):
    expected = parse_order_lines(order_lines)

    result = compare_order(
        expected=expected,
        detected=detected_items,
    )

    return result


@app.post("/verify-image")
def verify_image(
    order_lines: str,
    image: UploadFile = File(...),
):
    suffix = Path(image.filename or "").suffix or ".png"

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp_file:
        shutil.copyfileobj(image.file, temp_file)
        image_path = temp_file.name

    try:
        result, status = verify_image_order(
            order_lines=order_lines,
            image_path=image_path,
        )

        if result is None:
            return {
                "status": status,
                "verdict": "uncertain",
                "expected_items": parse_order_lines(order_lines),
                "detected_items": [],
                "issues": [
                    {
                        "type": "uncertain",
                        "sku": None,
                        "expected_quantity": None,
                        "detected_quantity": None,
                        "evidence": (
                            "The image could not be reliably analyzed."
                        ),
                    }
                ],
            }

        return {
            "status": status,
            **result.model_dump(),
        }

    finally:
        Path(image_path).unlink(missing_ok=True)