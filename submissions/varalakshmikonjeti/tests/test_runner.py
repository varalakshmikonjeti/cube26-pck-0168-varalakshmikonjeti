import json
from pathlib import Path

from submissions.varalakshmikonjeti.src.models import VerificationRequest
from submissions.varalakshmikonjeti.src.runner import PackManagerRunner
from submissions.varalakshmikonjeti.src.storage import VerificationStorage


class FakePipeline:
    def run(self, request: VerificationRequest):
        from submissions.varalakshmikonjeti.src.models import (
            VerificationChecks,
            VerificationResult,
        )

        return VerificationResult(
            record_id=request.unit_id,
            unit_id=request.unit_id,
            org_id=request.org_id,
            created_at="2026-09-28T00:00:00+00:00",
            overall_verdict="PASS",
            expected_contents=request.expected_contents,
            observed_contents=[],
            checks=VerificationChecks(
                item_presence="PASS",
                quantity="PASS",
                extra_items="PASS",
                evidence_sufficiency="PASS",
            ),
            evidence=[
                {
                    "type": "test",
                    "message": "Synthetic test evidence",
                }
            ],
            reasoning="Test pipeline produced a structured result.",
            model_status="completed",
            pending_review=False,
        )


def test_runner_persists_tenant_scoped_record(tmp_path: Path):
    storage = VerificationStorage(
        base_dir=str(tmp_path / "verification_records")
    )

    runner = PackManagerRunner(
        pipeline=FakePipeline(),
        storage=storage,
    )

    request = VerificationRequest(
        unit_id="UNIT-TEST-001",
        org_id="org_test_alpha",
        expected_contents=[],
        image_reference="test-image.jpg",
    )

    result = runner.run(request)

    assert result["record_id"] == "UNIT-TEST-001"
    assert result["unit_id"] == "UNIT-TEST-001"
    assert result["org_id"] == "org_test_alpha"
    assert result["overall_verdict"] == "PASS"
    assert result["pending_review"] is False

    saved = storage.get(
        org_id="org_test_alpha",
        record_id="UNIT-TEST-001",
    )

    assert saved is not None
    assert saved["org_id"] == "org_test_alpha"


def test_runner_json_output(tmp_path: Path):
    storage = VerificationStorage(
        base_dir=str(tmp_path / "verification_records")
    )

    runner = PackManagerRunner(
        pipeline=FakePipeline(),
        storage=storage,
    )

    request = VerificationRequest(
        unit_id="UNIT-TEST-002",
        org_id="org_test_beta",
        expected_contents=[],
        image_reference="test-image.jpg",
    )

    result = runner.run_json(request)

    parsed = json.loads(result)

    assert parsed["record_id"] == "UNIT-TEST-002"
    assert parsed["org_id"] == "org_test_beta"
    assert parsed["overall_verdict"] == "PASS"