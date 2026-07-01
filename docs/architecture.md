# Aegis Support Agent Architecture

## Overview

Aegis is a trust-gated customer support agent for B2B SaaS teams.

The system is designed as a multi-agent workflow. Each agent has a narrow role, and the final response is not automatically trusted. Instead, a judge agent evaluates the draft response and routes the ticket through a trust gate.

---

## High-Level Flow

Customer Ticket
↓
Triage Agent
↓
Policy Lookup Tool
↓
Draft Response Agent
↓
Judge Agent
↓
Trust Gate
↓
Final Decision
├── suggest_reply
├── human_review
└── escalate

---

## Components

### 1. Triage Agent

The Triage Agent receives the raw customer message.

It produces a structured `TriageResult`:

summary
category
risk_level
needs_policy_lookup

Example categories:

- billing
- security
- privacy
- account_access
- technical_bug
- feature_request
- general

The goal is to determine what kind of support issue the customer has and whether the issue may be risky.

---

### 2. Policy Lookup Tool

The Policy Lookup Tool retrieves a policy document from the `policies/` folder.

Example:

policy_lookup("billing")

returns:

policies/billing.md

This gives the system a grounding layer. The agent does not rely only on generated knowledge; it retrieves the relevant policy before drafting a response.

---

### 3. Draft Response Agent

The Draft Response Agent receives:

customer_message
triage_result
policy_text

It produces a structured `DraftResult`:


The draft response should be polite, concise, and safe. It should not promise actions that require verification.

---

### 4. Judge Agent

The Judge Agent receives:

customer_message
triage_result
draft_response
policy_text

It produces a structured `JudgeResult`:

helpfulness
policy_compliance
hallucination_risk
risk_level
trust_score
decision
reason

The Judge Agent is responsible for deciding whether the draft is safe enough to suggest directly.

---

### 5. Trust Gate

The Trust Gate uses the judge output to make the final routing decision.

Current decisions:

suggest_reply
human_review
escalate

Current MVP behavior:

- low risk → suggest_reply
- medium risk → human_review
- high risk → escalate
- security/privacy → always escalate

This can be extended later with more nuanced scoring.

---

### 6. Escalation Agent

The Escalation Agent creates an internal note for a human support specialist.

It includes:

- original customer message
- summary
- category
- risk level
- reason for escalation or review
- reminder to verify account-specific facts

---

## Structured A2A Message Passing

Aegis uses structured objects as messages between agents.

Triage Agent → TriageResult
Draft Agent → DraftResult
Judge Agent → JudgeResult
Pipeline → FinalResult

This is an A2A-style pattern because each agent communicates with the next through explicit structured outputs.

Benefits:

- easier debugging
- easier evaluation
- easier extension
- safer handoffs between agents
- better reproducibility

---

## MCP-style Tool Interface

Aegis includes a simple MCP-style tool:

policy_lookup(category)

The tool has:

Input: support category
Output: relevant policy text

In the current MVP, this is implemented as a local Python function that reads files from `policies/`.

In a production version, this could become a real MCP server connected to:

- a knowledge base
- support docs
- billing system
- CRM
- ticketing system
- security reporting workflow

---

## Safety and Human-in-the-Loop Design

Aegis avoids unsafe automation by routing risky tickets to humans.

Escalation or review is triggered for:

- refunds
- duplicate charges
- cancellations
- security reports
- privacy or data deletion requests
- account access changes
- suspected compromise
- unresolved technical failures

The system avoids:

- promising refunds before verification
- confirming deletion before verification
- confirming vulnerabilities before security review
- requesting passwords, API keys, tokens, or secrets
- inventing account-specific facts

---

## Evaluation Design

Aegis includes an evaluation harness in:

src/evaluator.py

It compares predictions against expected labels in:

data/sample_tickets.csv

Current metrics:

- category accuracy
- risk accuracy
- decision accuracy

The evaluation output is saved to:

data/evaluation_report.json

---

## Current MVP Limitations

The current MVP is rule-based.

Limitations:

- classification is based on simple keyword matching
- draft responses are template-based
- judge scoring is deterministic
- policy retrieval is local file lookup
- no real CRM or support system integration yet
- no live Gemini agent reasoning yet

---

## Planned Improvements

Possible next improvements:

- Gemini-powered triage, drafting, and judging
- LLM-as-judge evaluation
- real MCP server for policy lookup
- richer ticket dataset
- confusion matrix and error analysis
- notebook demo for Kaggle
- web or CLI demo interface
- GitHub repository with reproducible setup instructions

