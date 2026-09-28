import pytest

from submissions.varalakshmikonjeti.src.storage import VerificationStorage


def test_tenant_cannot_read_another_tenants_record(tmp_path):
    storage = VerificationStorage(
        base_dir=str(tmp_path / "verification_records")
    )

    record = {
        "record_id": "RECORD-001",
        "unit_id": "UNIT-001",
        "org_id": "org_alpha",
        "overall_verdict": "PENDING_REVIEW",
    }

    storage.save(
        org_id="org_alpha",
        record_id="RECORD-001",
        record=record,
    )

    assert storage.get(
        org_id="org_alpha",
        record_id="RECORD-001",
    ) == record

    assert storage.get(
        org_id="org_beta",
        record_id="RECORD-001",
    ) is None


def test_storage_rejects_tenant_mismatch(tmp_path):
    storage = VerificationStorage(
        base_dir=str(tmp_path / "verification_records")
    )

    record = {
        "record_id": "RECORD-002",
        "unit_id": "UNIT-002",
        "org_id": "org_alpha",
    }

    with pytest.raises(ValueError, match="Tenant mismatch"):
        storage.save(
            org_id="org_beta",
            record_id="RECORD-002",
            record=record,
        )