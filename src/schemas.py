from typing import Literal, Optional
from pydantic import BaseModel, Field


Category = Literal[
    "billing",
    "security",
    "privacy",
    "account_access",
    "technical_bug",
    "feature_request",
    "general",
]

RiskLevel = Literal["low", "medium", "high"]

Decision = Literal["suggest_reply", "human_review", "escalate"]


class TriageResult(BaseModel):
    summary: str = Field(..., description="Short summary of the customer issue.")
    category: Category = Field(..., description="Support category for the ticket.")
    risk_level: RiskLevel = Field(..., description="Risk level of the issue.")
    needs_policy_lookup: bool = Field(True, description="Whether to retrieve policy before drafting.")


class DraftResult(BaseModel):
    response: str = Field(
        ...,
        description="Draft response to the customer."
    )

    revision_count: int = Field(
        default=0,
        description="Number of revisions made by the reflection loop."
    )

class JudgeResult(BaseModel):
    helpfulness: int = Field(..., ge=1, le=10, description="How helpful the draft is.")
    policy_compliance: int = Field(..., ge=1, le=10, description="How well the draft follows policy.")
    hallucination_risk: int = Field(..., ge=1, le=10, description="Risk that the draft invents facts.")
    risk_level: RiskLevel = Field(..., description="Final risk level after judging.")
    trust_score: int = Field(..., ge=0, le=100, description="Overall confidence score.")
    decision: Decision = Field(..., description="Final routing decision.")
    evidence: list[str] = Field(
    default_factory=list,
    description="Evidence used to justify the judge decision."
)
    reason: str = Field(..., description="Reason for the decision.")


class EscalationResult(BaseModel):
    escalation_note: str = Field(..., description="Internal note for a human support agent.")


class FinalResult(BaseModel):
    ticket_id: str
    customer_message: str
    summary: str
    category: Category
    risk_level: RiskLevel
    policy: str
    draft_response: str
    trust_score: int
    decision: Decision
    reason: str
    escalation_note: Optional[str] = None
