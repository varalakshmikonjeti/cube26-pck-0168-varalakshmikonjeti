from submissions.varalakshmikonjeti.src.model_client import ModelClient


def test_model_client_requires_image_reference():
    client = ModelClient()

    result = client.verify_image(
        image_reference="",
        expected_contents=[
            {
                "sku": "SKU-A",
                "quantity": 1,
            }
        ],
    )

    assert result["status"] == "error"
    assert result["observed_contents"] == []
    assert result["error"]["type"] == "missing_image_reference"


def test_model_client_does_not_invent_observations():
    client = ModelClient()

    result = client.verify_image(
        image_reference="examples/sample_packing_image.jpg",
        expected_contents=[
            {
                "sku": "SKU-A",
                "quantity": 2,
            }
        ],
    )

    assert result["status"] == "error"
    assert result["observed_contents"] == []
    assert result["error"]["type"] == "model_not_configured"