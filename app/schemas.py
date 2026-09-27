from typing import Literal

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    sku: str
    quantity: int = Field(ge=1)


class DetectedItem(BaseModel):
    sku: str
    quantity: int = Field(ge=0)
    evidence: str


class VerificationIssue(BaseModel):
    type: Literal[
        "missing_item",
        "wrong_item",
        "extra_item",
        "quantity_mismatch",
        "uncertain",
    ]
    sku: str | None = None
    expected_quantity: int | None = None
    detected_quantity: int | None = None
    evidence: str


class VerificationResult(BaseModel):
    verdict: Literal["seal", "stop_and_fix", "uncertain"]
    expected_items: list[OrderItem]
    detected_items: list[DetectedItem]
    issues: list[VerificationIssue] = []