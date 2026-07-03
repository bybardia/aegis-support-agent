---
name: security_incident_response
description: Safely handle security-vulnerability and privacy/data-deletion tickets by acknowledging, protecting secrets, and always escalating.
when_to_use: Triage category is security or privacy (vulnerabilities, leaked secrets, GDPR/data-deletion, personal-data requests).
---

# Security & Privacy Incident Response Skill

## Goal
Respond to sensitive security and privacy reports in a way that protects the user and the company, and always hand the case to a human specialist.

## Hard rules
- Never ask for or accept passwords, API keys, tokens, or other secrets in the conversation.
- Never confirm a vulnerability, a breach, or a data deletion before specialist review.
- Do not invent account-specific facts or promise remediation timelines.
- Security and privacy tickets are ALWAYS escalated, regardless of model confidence.

## Response guidance
- Thank the reporter and confirm the report is taken seriously.
- Ask them to stop sharing any secrets, and to use the official security channel if one exists.
- State that the case is being escalated to the security/privacy team for review.

## Routing
- Always -> escalate. The deterministic trust gate enforces this even if the model disagrees.