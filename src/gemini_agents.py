from google import genai
from google.genai import types

from src.agents import (
    triage_ticket,
    draft_response as rule_draft_response,
    judge_response as rule_judge_response,
    create_escalation_note,
)
from src.schemas import DraftResult, JudgeResult
from src.config import settings
from src.skills import load_skill

_client = None

def _get_client():
    global _client
    if _client is not None:
        return _client
    api_key = getattr(settings, "gemini_api_key", None)
    if not api_key:
        return None
    _client = genai.Client(api_key=api_key)
    return _client


def gemini_triage_ticket(customer_message):
    return triage_ticket(customer_message)


DRAFT_SYSTEM_INSTRUCTION = (
    "You are a professional B2B SaaS customer support agent. "
    "Follow the policy strictly. Do not promise refunds, do not invent facts, "
    "do not claim actions were completed, be concise and professional, and if "
    "verification is required, say so. Write only the customer-facing response."
)


def gemini_draft_response(customer_message, triage, policy):
    client = _get_client()
    if client is None:
        return rule_draft_response(customer_message, triage, policy)




    skill = load_skill(triage.category)
    skill_section = f"\n\nAgent skill guidance:\n{skill}" if skill else ""

    prompt = (
        f"Customer Message:\n{customer_message}\n\n"
        f"Category: {triage.category}\n"
        f"Risk Level: {triage.risk_level}\n\n"
        f"Policy:\n{policy}\n"
    )
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=DRAFT_SYSTEM_INSTRUCTION,
                temperature=0.3,
            ),
        )
        return DraftResult(response=response.text.strip())
    except Exception as e:
        print(f"[gemini_draft_response] falling back to rule draft: {e}")
        return rule_draft_response(customer_message, triage, policy)


JUDGE_SYSTEM_INSTRUCTION = (
    "You are the Judge/QA agent in a trust-gated support system. "
    "Evaluate the DRAFT reply against the customer message and the retrieved policy. "
    "Be conservative: if the draft risks promising refunds, leaking secrets, confirming "
    "data deletion, or inventing account facts, lower the trust score. "
    "Ground every claim in the provided policy; never invent policy. "
    "Return structured data: helpfulness (0-10), policy_compliance (0-10), "
    "hallucination_risk (0-10), trust_score (0-100), decision "
    "('suggest_reply' | 'human_review' | 'escalate'), evidence (short bullets), reason."
)


def gemini_judge_response(customer_message, triage, draft, policy):
    client = _get_client()
    if client is None:
        return rule_judge_response(customer_message, triage, draft, policy)

    prompt = (
        f"CUSTOMER MESSAGE:\n{customer_message}\n\n"
        f"TRIAGE:\n- category: {triage.category}\n- risk_level: {triage.risk_level}\n\n"
        f"RETRIEVED POLICY:\n{policy}\n\n"
        f"DRAFT REPLY TO EVALUATE:\n{draft.response}\n"
    )
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=JUDGE_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=JudgeResult,
                temperature=0.2,
            ),
        )
        result: JudgeResult = response.parsed
    except Exception as e:
        print(f"[gemini_judge_response] falling back to rule judge: {e}")
        return rule_judge_response(customer_message, triage, draft, policy)

    result.risk_level = triage.risk_level
    result.trust_score = max(0, min(100, result.trust_score))
    if triage.category in ["security", "privacy"]:
        result.decision = "escalate"
        result.trust_score = min(result.trust_score, 45)
        result.evidence.append(f"{triage.category} policy escalation enforced (deterministic guardrail)")
        result.reason = "Security or privacy issue must be escalated according to policy."
    return result


def gemini_create_escalation_note(customer_message, triage, judge):
    return create_escalation_note(customer_message, triage, judge)