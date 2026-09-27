import json
import os

from dotenv import load_dotenv
from google import genai

from app.schemas import DetectedItem


load_dotenv()

MODEL_NAME = "gemini-3.6-flash"


def detect_items_from_image(
    image_path: str,
) -> tuple[list[DetectedItem], str]:
    """
    Detect products from a packing-box image using Gemini vision.

    Returns:
        (detected_items, status)

        status:
        - "success"   when products are detected reliably
        - "uncertain" when the image cannot be judged reliably
        - "pending"   when detection cannot be completed
    """

    if not image_path.strip():
        return [], "uncertain"

    api_key = os.getenv("AI_API_KEY")

    if not api_key:
        return [], "pending"

    if not os.path.exists(image_path):
        return [], "uncertain"

    try:
        client = genai.Client(api_key=api_key)

        image_file = client.files.upload(file=image_path)

        prompt = """
You are a packing verification vision system.

Look at the provided image of an open packing box.

Identify every distinct product visible in the box.

Return ONLY valid JSON in this exact format:

{
  "status": "success",
  "items": [
    {
      "sku": "product name",
      "quantity": 1,
      "evidence": "short visual evidence"
    }
  ]
}

If the image is too unclear, empty, badly framed, or the products
cannot be identified reliably, return:

{
  "status": "uncertain",
  "items": []
}

Rules:
- Include every visible product when identification is reliable.
- Estimate quantity only when the quantity is visually clear.
- If a product cannot be identified reliably, do not invent a SKU.
- Use a descriptive product name when no actual SKU is visible.
- Evidence must describe what is visibly present.
- Do not include markdown.
- Do not include explanations outside the JSON.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[image_file, prompt],
        )

        text = (response.text or "").strip()

        if not text:
            return [], "uncertain"

        data = json.loads(text)

        model_status = data.get("status", "success")

        if model_status == "uncertain":
            return [], "uncertain"

        items = [
            DetectedItem(**item)
            for item in data.get("items", [])
        ]

        if not items:
            return [], "uncertain"

        return items, "success"

    except Exception:
        return [], "pending"