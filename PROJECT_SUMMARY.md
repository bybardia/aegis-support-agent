# Project Summary: Aegis Support Agent

## One-line Summary

Aegis is a trust-gated customer support agent that drafts SaaS support replies, evaluates its own response quality, assigns a trust score, and escalates risky cases to humans.

---

## Track

**Agents for Business**

---

## Problem

Customer support teams handle many repetitive tickets, but direct AI automation can be risky when tickets involve:

- refunds
- duplicate charges
- account access
- privacy requests
- data deletion
- security vulnerabilities
- cancellations

Aegis addresses this by adding a trust gate between AI-generated drafts and final support actions.

---

## Solution

Aegis uses a multi-agent workflow:

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

The final decision can be:

- `suggest_reply`
- `human_review`
- `escalate`

---

## Agentic Concepts Demonstrated

Aegis demonstrates:

- Multi-agent design
- MCP-style tool use
- A2A-style structured message passing
- Policy grounding
- Judge agent evaluation
- Trust scoring
- Human-in-the-loop escalation
- Evaluation harness
- Error analysis
- Confusion matrix reporting

---

## Why It Matters

Aegis shows how a business AI agent can be useful without being reckless.

Instead of automatically sending generated replies, it:

1. reads the customer ticket,
2. retrieves policy context,
3. drafts a response,
4. evaluates the draft,
5. assigns a trust score,
6. routes risky issues to human review or escalation.

This pattern is useful for enterprise workflows where safety, explainability, and accountability matter.

---

## Current MVP

The current MVP is rule-based and fully reproducible without private data or paid APIs.

It includes:

- sample synthetic support tickets
- policy files
- structured schemas
- command-line pipeline
- evaluation script
- error analysis
- confusion matrices
- notebook demo
- documentation
- CC-BY 4.0 compatible license

---

## How to Run

Run one ticket:

cat > PROJECT_SUMMARY.md << 'EOF'
# Project Summary: Aegis Support Agent

## One-line Summary

Aegis is a trust-gated customer support agent that drafts SaaS support replies, evaluates its own response quality, assigns a trust score, and escalates risky cases to humans.

---

## Track

**Agents for Business**

---

## Problem

Customer support teams handle many repetitive tickets, but direct AI automation can be risky when tickets involve:

- refunds
- duplicate charges
- account access
- privacy requests
- data deletion
- security vulnerabilities
- cancellations

Aegis addresses this by adding a trust gate between AI-generated drafts and final support actions.

---

## Solution

Aegis uses a multi-agent workflow:

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

The final decision can be:

- `suggest_reply`
- `human_review`
- `escalate`

---

## Agentic Concepts Demonstrated

Aegis demonstrates:

- Multi-agent design
- MCP-style tool use
- A2A-style structured message passing
- Policy grounding
- Judge agent evaluation
- Trust scoring
- Human-in-the-loop escalation
- Evaluation harness
- Error analysis
- Confusion matrix reporting

---

## Why It Matters

Aegis shows how a business AI agent can be useful without being reckless.

Instead of automatically sending generated replies, it:

1. reads the customer ticket,
2. retrieves policy context,
3. drafts a response,
4. evaluates the draft,
5. assigns a trust score,
6. routes risky issues to human review or escalation.

This pattern is useful for enterprise workflows where safety, explainability, and accountability matter.

---

## Current MVP

The current MVP is rule-based and fully reproducible without private data or paid APIs.

It includes:

- sample synthetic support tickets
- policy files
- structured schemas
- command-line pipeline
- evaluation script
- error analysis
- confusion matrices
- notebook demo
- documentation
- CC-BY 4.0 compatible license

---

## How to Run

Run one ticket:

python -m src.main --message "I was charged twice this month. Please refund me now." --mode rule

Run the full pipeline:

./run_all.sh rule
./run_all.sh rule

Run evaluation:

python -m src.evaluator --sample data/sample_tickets.csv --mode rule

---

## Key Output

For each ticket, Aegis produces:

- summary
- category
- risk level
- draft response
- trust score
- routing decision
- reason
- escalation note when needed

---

## Future Work

Planned improvements:

- live Gemini-powered agents
- real MCP server for policy lookup
- larger public support-ticket dataset
- LLM-as-judge evaluation
- web UI or richer notebook demo
- integration with a ticketing system or CRM
