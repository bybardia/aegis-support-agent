from src.agents import (
    triage_ticket,
    draft_response,
    judge_response,
    create_escalation_note,
)
def gemini_triage_ticket(customer_message):
     return triage_ticket(customer_message)
def gemini_draft_response(customer_message, triage, policy):
   return draft_response(customer_message, triage, policy)
def gemini_judge_response(customer_message, triage, draft, policy):
    return judge_response(customer_message, triage, draft, policy)
def gemini_create_escalation_note(customer_message, triage, judge):
    return create_escalation_note(customer_message, triage, judge)
