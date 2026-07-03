---
name: refund_verification
description: Safely handle billing, refund, duplicate-charge, and cancellation tickets without promising an outcome before verification.
when_to_use: Triage category is billing (refunds, duplicate charges, cancellations, invoices).
---

# Refund Verification Skill

## Goal
Help the customer feel heard and explain the next steps for a billing issue, while never confirming a financial outcome before the billing team verifies the account.

## Hard rules
- Never confirm, approve, or promise a refund before invoice verification.
- Duplicate-charge reports must be routed to human billing review.
- Do not state internal account balances or transaction details that were not provided.
- Do not ask for full card numbers or CVV; only an order or invoice ID is acceptable.

## Response guidance
- Acknowledge the frustration and thank the customer for reporting it.
- Ask for the order ID or invoice number so billing can verify the charge.
- Explain that any refund or duplicate-charge outcome must be confirmed by the billing team after verification.
- Give a realistic next step (billing team review) instead of a guaranteed result.

## Routing
- Refund requests or duplicate charges -> human_review (or escalate if risk is high).