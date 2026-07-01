from src.schemas import TriageResult, DraftResult, JudgeResult, EscalationResult


def triage_ticket(customer_message: str) -> TriageResult:
    """Classify a support ticket into category and risk level."""
    text = customer_message.lower()

    if any(word in text for word in ["security", "vulnerability", "exposes", "breach", "token", "api key"]):
        category = "security"
        risk_level = "high"
    elif any(word in text for word in ["delete my data", "delete all", "privacy", "gdpr", "personal data"]):
        category = "privacy"
        risk_level = "high"
    elif any(word in text for word in ["charged", "refund", "invoice", "billing", "cancel"]):
        category = "billing"
        if any(word in text for word in ["charged twice", "refund", "cancel"]):
            risk_level = "medium"
        else:
            risk_level = "low"
    elif any(word in text for word in ["password", "login", "log in", "access", "remove their access"]):
        category = "account_access"
        risk_level = "medium"
    elif any(word in text for word in ["crash", "crashing", "bug", "error", "broken"]):
        category = "technical_bug"
        risk_level = "medium"
    elif any(word in text for word in ["feature", "add", "dark mode", "request"]):
        category = "feature_request"
        risk_level = "low"
    else:
        category = "general"
        risk_level = "low"

    summary = f"Customer issue categorized as {category} with {risk_level} risk."

    return TriageResult(
        summary=summary,
        category=category,
        risk_level=risk_level,
        needs_policy_lookup=True,
    )


def draft_response(customer_message: str, triage: TriageResult, policy: str) -> DraftResult:
    """Create a safe draft response using the ticket, triage result, and policy."""
    category = triage.category

    if category == "billing":
        response = (
            "Thanks for reaching out. I understand this is frustrating. "
            "I can help explain the next steps, but any refund or duplicate charge request "
            "needs invoice verification by our billing team before we can confirm an outcome."
        )
    elif category == "security":
        response = (
            "Thank you for reporting this. We take security reports seriously. "
            "I will escalate this to the security team for review. Please do not share passwords, "
            "API keys, tokens, or other secrets in this conversation."
        )
    elif category == "privacy":
        response = (
            "Thanks for contacting us. Data deletion requests need to go through our verified "
            "privacy process before we can confirm any action. I will route this for human review."
        )
    elif category == "account_access":
        response = (
            "I can help with safe account access steps. Please do not share passwords or one-time codes. "
            "If this involves changing team access or removing a user, a verified admin or human review is required."
        )
    elif category == "technical_bug":
        response = (
            "Thanks for reporting this issue. To help investigate, please share the steps that reproduce the problem, "
            "what you expected to happen, and any non-sensitive error message you saw."
        )
    elif category == "feature_request":
        response = (
            "Thanks for the suggestion. We appreciate product feedback and may share this with the product team. "
            "I cannot promise a specific feature timeline, but your input is helpful."
        )
    else:
        response = (
            "Thanks for reaching out. I will help with safe next steps and avoid making promises "
            "that require account or internal verification."
        )

    return DraftResult(response=response)


def judge_response(customer_message: str, triage: TriageResult, draft: DraftResult, policy: str) -> JudgeResult:
    """Evaluate the draft response and decide whether to suggest, review, or escalate."""
    category = triage.category
    risk_level = triage.risk_level

    helpfulness = 8
    policy_compliance = 8
    hallucination_risk = 2
    revision_bonus = 0

    if getattr(draft, "revision_count", 0) > 0:
        revision_bonus = 15   
    evidence = []

    if risk_level == "high":
        trust_score = min(100, 45 + revision_bonus)
        decision = "escalate"
        reason = "High-risk issue requires human specialist review."

    elif risk_level == "medium":
        trust_score = min(100, 72 + revision_bonus)
        decision = "human_review"
        reason = "Medium-risk issue should be reviewed before final customer action."

    else:
        trust_score = min(100, 88 + revision_bonus)
        decision = "suggest_reply"
        reason = "Low-risk issue can receive a suggested support reply."

    if category in ["security", "privacy"]:
        decision = "escalate"
        trust_score = min(trust_score, 45)
        reason = "Security or privacy issue must be escalated according to policy."

    # Evidence collection

    evidence.append(f"category={category}")
    evidence.append(f"risk_level={risk_level}")

    if "refund" in customer_message.lower():
        evidence.append("refund request detected")

    if "charged twice" in customer_message.lower():
        evidence.append("duplicate charge detected")

    if category == "security":
        evidence.append("security policy escalation triggered")

    if category == "privacy":
        evidence.append("privacy policy escalation triggered")

    if decision == "human_review":
        evidence.append("human review required")

    if decision == "escalate":
        evidence.append("escalation required")

    if decision == "suggest_reply":
        evidence.append("safe suggested reply allowed")    
        
    if getattr(draft, "revision_count", 0) > 0:
        evidence.append(
            f"response revised {draft.revision_count} time(s)"
        )
    return JudgeResult(
        helpfulness=helpfulness,
        policy_compliance=policy_compliance,
        hallucination_risk=hallucination_risk,
        risk_level=risk_level,
        trust_score=trust_score,
        decision=decision,
        evidence=evidence,
        reason=reason,
    )


def create_escalation_note(customer_message: str, triage: TriageResult, judge: JudgeResult) -> EscalationResult:
    """Create an internal note for a human support agent."""
    note = (
        f"Customer message: {customer_message}\n"
        f"Summary: {triage.summary}\n"
        f"Category: {triage.category}\n"
        f"Risk level: {judge.risk_level}\n"
        f"Reason for escalation/review: {judge.reason}\n"
        "Human agent should verify account-specific facts before promising any action."
    )
    return EscalationResult(escalation_note=note)

def revise_response(
    customer_message: str,
    triage: TriageResult,
    draft: DraftResult,
    judge: JudgeResult,
    policy: str,
) -> DraftResult:
    """
    Reflection agent that revises a draft response when
    trust score is below the acceptable threshold.
    """

    revised_response = draft.response

    if judge.trust_score < 70:

        revised_response += (
            "\n\nBefore any action can be confirmed, "
            "additional verification may be required."
        )

    return DraftResult(
        response=revised_response,
        revision_count=draft.revision_count + 1,
    )