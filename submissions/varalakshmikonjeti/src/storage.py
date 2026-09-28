import json
from pathlib import Path
from typing import Any, Dict, Optional


class VerificationStorage:
    """
    Simple file-based storage for Pack Manager verification records.

    Records are stored under an organisation-specific directory so that
    records from different organisations remain separated.
    """

    def __init__(self, base_dir: str = "data/verification_records") -> None:
        self.base_dir = Path(base_dir)

    def _org_dir(self, org_id: str) -> Path:
        if not org_id or "/" in org_id or "\\" in org_id:
            raise ValueError("Invalid organisation identifier")

        path = self.base_dir / org_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _record_path(self, org_id: str, record_id: str) -> Path:
        if not record_id or "/" in record_id or "\\" in record_id:
            raise ValueError("Invalid record identifier")

        return self._org_dir(org_id) / f"{record_id}.json"

    def save(
        self,
        org_id: str,
        record_id: str,
        record: Dict[str, Any],
    ) -> Path:
        """
        Save a verification record under its organisation.

        The record's org_id must match the organisation supplied to save().
        """
        record_org_id = record.get("org_id")

        if record_org_id != org_id:
            raise ValueError(
                "Tenant mismatch: record organisation does not match "
                "storage organisation"
            )

        path = self._record_path(org_id, record_id)

        with path.open("w", encoding="utf-8") as file:
            json.dump(record, file, indent=2, ensure_ascii=False)

        return path

    def get(
        self,
        org_id: str,
        record_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a record only from the requested organisation's directory.
        """
        path = self._record_path(org_id, record_id)

        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as file:
            record = json.load(file)

        if record.get("org_id") != org_id:
            raise PermissionError(
                "Tenant isolation violation"
            )

        return record

    def exists(
        self,
        org_id: str,
        record_id: str,
    ) -> bool:
        """Return whether a record exists for the requested organisation."""
        return self._record_path(org_id, record_id).exists()