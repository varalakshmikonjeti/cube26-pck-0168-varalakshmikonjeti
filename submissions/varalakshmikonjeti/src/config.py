import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """
    Runtime configuration for Pack Manager.

    Values are read from environment variables so that credentials,
    model configuration, and storage locations are not hard-coded.
    """

    storage_dir: str = os.getenv(
        "PACK_MANAGER_STORAGE_DIR",
        "data/verification_records",
    )

    image_storage_dir: str = os.getenv(
        "PACK_MANAGER_IMAGE_DIR",
        "data/images",
    )

    model_name: str = os.getenv(
        "PACK_MANAGER_MODEL",
        "configured-model",
    )

    model_timeout_seconds: int = int(
        os.getenv(
            "PACK_MANAGER_MODEL_TIMEOUT",
            "30",
        )
    )

    require_evidence: bool = os.getenv(
        "PACK_MANAGER_REQUIRE_EVIDENCE",
        "true",
    ).lower() in {"1", "true", "yes"}

    environment: str = os.getenv(
        "PACK_MANAGER_ENV",
        "development",
    )


settings = Settings()