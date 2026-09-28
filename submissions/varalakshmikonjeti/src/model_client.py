from typing import Any, Dict, List, Optional


class ModelClient:
    """
    Boundary for the image/model verification provider.

    The client is intentionally provider-neutral. A real model provider
    can be connected here without changing the downstream decision logic.
    """

    def __init__(self, model_name: str = "configured-model") -> None:
        self.model_name = model_name

    def verify_image(
        self,
        image_reference: str,
        expected_contents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Verify an image using the configured model provider.

        This default implementation does not invent observations.
        It returns an explicit unavailable status until a real provider
        is configured.
        """
        if not image_reference:
            return {
                "status": "error",
                "observed_contents": [],
                "evidence": [],
                "reasoning": "No image reference was provided.",
                "error": {
                    "type": "missing_image_reference",
                    "message": "An image reference is required.",
                },
            }

        return {
            "status": "error",
            "observed_contents": [],
            "evidence": [],
            "reasoning": (
                "No model provider is configured for image verification."
            ),
            "error": {
                "type": "model_not_configured",
                "message": (
                    "Configure a model provider before automated "
                    "image verification is enabled."
                ),
            },
        }
    