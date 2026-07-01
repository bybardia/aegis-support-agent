from google import genai

from src.agents import (
    triage_ticket,
    judge_response,
    create_escalation_note,
)

from src.schemas import DraftResult
from src.config import settings


client = genai.Client(
    api_key=settings.gemini_api_key
)


def gemini_triage_ticket(customer_message):
    return triage_ticket(customer_message)


def gemini_draft_response(customer_message, triage, policy):

    prompt = f"""
You are a professional B2B SaaS customer support agent.

Customer Message:
{customer_message}

Category:
{triage.category}

Risk Level:
{triage.risk_level}

Policy:
{policy}

Rules:
- Follow the policy strictly
- Do not promise refunds
- Do not invent facts
- Do not claim actions were completed
- Be concise and professional
- If verification is required, mention it

Write only the customer response.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    return DraftResult(
        response=response.text.strip()
    )


def gemini_judge_response(customer_message, triage, draft, policy):

    return judge_response(
        customer_message,
        triage,
        draft,
        policy,
    )


def gemini_create_escalation_note(customer_message, triage, judge):

    return create_escalation_note(
        customer_message,
        triage,
        judge,
    )