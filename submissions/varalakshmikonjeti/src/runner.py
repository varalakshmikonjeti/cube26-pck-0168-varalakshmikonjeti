import json
from typing import Any, Dict

from .models import VerificationRequest
from .pipeline import VerificationPipeline
from .records import prepare_downstream_record
from .storage import VerificationStorage
from .tenant import validate_tenant


class PackManagerRunner:
    """
    Headless runner connecting verification, record preparation,
    and tenant-scoped persistence.
    """

    def __init__(
        self,
        pipeline: VerificationPipeline | None = None,
        storage: VerificationStorage | None = None,
    ) -> None:
        self.pipeline = pipeline or VerificationPipeline()
        self.storage = storage or VerificationStorage()

    def run(
        self,
        request: VerificationRequest,
    ) -> Dict[str, Any]:
        """
        Execute one verification and persist the structured result.
        """
        validate_tenant(
            expected_org_id=request.org_id,
            actual_org_id=request.org_id,
        )

        result = self.pipeline.run(request)

        record = prepare_downstream_record(result)

        self.storage.save(
            org_id=request.org_id,
            record_id=result.record_id,
            record=record,
        )

        return record

    def run_json(
        self,
        request: VerificationRequest,
    ) -> str:
        """
        Execute verification and return the result as JSON.
        """
        record = self.run(request)

        return json.dumps(
            record,
            indent=2,
            ensure_ascii=False,
        )