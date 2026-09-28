import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_headless_agent_cli_returns_pending_review():
    payload = {
        "unit_id": "UNIT-CLI-001",
        "org_id": "org_cli_test",
        "expected_contents": [
            {
                "sku": "SKU-A",
                "quantity": 1,
            }
        ],
        "image_reference": "test-image.jpg",
    }

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "submissions.varalakshmikonjeti.src",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=PROJECT_ROOT,
    )

    assert process.returncode == 0

    result = json.loads(process.stdout)

    assert result["unit_id"] == "UNIT-CLI-001"
    assert result["org_id"] == "org_cli_test"
    assert result["overall_verdict"] == "PENDING_REVIEW"
    assert result["pending_review"] is True
    assert result["model_status"] == "error"