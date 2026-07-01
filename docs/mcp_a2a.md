# MCP and A2A Design Notes

## Overview

Aegis Support Agent demonstrates two important agentic AI concepts:

1. MCP-style tool use
2. A2A-style agent communication

The current MVP does not require a full external MCP server. Instead, it implements a local MCP-style tool interface that can later be upgraded into a real MCP server.

---

## What is MCP?

MCP stands for Model Context Protocol.

In simple terms, MCP gives an AI agent a standard way to connect to external tools and resources.

Instead of expecting the model to know everything, MCP lets the agent call tools such as:

- knowledge bases
- file systems
- databases
- ticketing systems
- CRMs
- calendars
- support documentation
- billing systems

---

## MCP-style Tool in Aegis

Aegis includes a policy lookup tool:

policy_lookup(category)

Input:

support category

Output:

relevant policy text

Example:

policy_lookup("billing")

returns the content of:

policies/billing.md

---

## Why This Counts as Tool Use

The support agent does not rely only on model memory.

Before drafting a response, the pipeline retrieves a policy document:


​
Triage Agent
↓
Policy Lookup Tool
↓
Draft Response Agent

This makes the response more grounded and easier to audit.

---

## Future MCP Server Version

In a future version, the local `policy_lookup` function could be replaced by a real MCP server.

Example MCP tools:

policy_lookup
ticket_lookup
customer_plan_lookup
billing_status_lookup
security_escalation_create

Potential production integrations:

- support knowledge base
- customer ticket database
- billing system
- CRM
- security intake workflow

---

## What is A2A?

A2A means Agent-to-Agent communication.

In an agentic workflow, one agent can produce structured output that another agent uses as input.

A2A is useful because different agents can have different roles.

For example:

Triage Agent → Draft Response Agent → Judge Agent → Escalation Agent

---

## A2A-style Communication in Aegis

Aegis uses structured schemas between each agent.

The schemas are defined in:

src/schemas.py
TriageResult
DraftResult
JudgeResult
EscalationResult
FinalResult

---

## Message Flow

Customer message
↓
Triage Agent
↓ TriageResult
Policy Lookup Tool
↓ policy text
Draft Response Agent
↓ DraftResult
Judge Agent
↓ JudgeResult
Trust Gate
↓ decision
Escalation Agent if needed
↓ EscalationResult
FinalResult

---

## Example TriageResult

{
"summary": "Customer issue categorized as billing with medium risk.",
"category": "billing",
"risk_level": "medium",
"needs_policy_lookup": true
}


---

## Example JudgeResult

{
"helpfulness": 8,
"policy_compliance": 8,
"hallucination_risk": 2,
"risk_level": "medium",
"trust_score": 72,
"decision": "human_review",
"reason": "Medium-risk issue should be reviewed before final customer action."
}

---

## Why Structured A2A Matters

Structured handoffs make the system:

- easier to debug
- easier to test
- easier to evaluate
- easier to extend
- safer than passing unstructured text only

This also makes the project more reproducible.

---

## Trust-Gated A2A Pattern

Aegis uses a trust-gated pattern:

Draft Agent output is not final.
Judge Agent evaluates it.
Trust Gate decides the route.

The final decision can be:

suggest_reply
human_review
escalate

This pattern is useful for business agents because many enterprise workflows require human review before action.

---

## Current MVP vs Future Version

### Current MVP

- local Python tool for policy lookup
- structured Pydantic schemas
- rule-based agents
- deterministic trust gate
- JSON output
- evaluation harness

### Future Version

- Gemini-powered agents
- real MCP server
- external ticketing system integration
- richer A2A orchestration
- LLM-as-judge evaluation
- human approval workflow

---

## Summary

Aegis demonstrates MCP and A2A concepts in a practical support-agent workflow.

MCP-style concept:

The agent retrieves external policy context using a tool.

A2A-style concept:

Specialized agents exchange structured messages through the support pipeline.

Together, these make Aegis safer, more explainable, and more useful than a single generic chatbot.

