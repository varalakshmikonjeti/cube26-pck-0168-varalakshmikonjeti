from typing import Any, Dict, Optional

from .models import VerificationRequest, VerificationResult
from .service import PackManagerService
from .storage import VerificationStorage


class PackManagerAPI:
    """
    Small application boundary for the Pack Manager workflow.

    It connects request handling, verification, and tenant-scoped storage.
    """

    def __init__(
        self,
        service: Optional[PackManagerService] = None,
        storage: Optional[VerificationStorage] = None,
    ) -> None:
        self.service = service or PackManagerService()
        self.storage = storage or VerificationStorage()

    def verify(
        self,
        request: VerificationRequest,
    ) -> Dict[str, Any]:
        """
        Process one verification request and persist its result.
        """
        result: VerificationResult = self.service.verify(request)

        record = result.to_dict()

        self.storage.save(
            org_id=request.org_id,
            record_id=result.record_id,
            record=record,
        )

        return record

    def get_result(
        self,
        org_id: str,
        record_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a verification result within the requested tenant.
        """
        return self.storage.get(
            org_id=org_id,
            record_id=record_id,
        )