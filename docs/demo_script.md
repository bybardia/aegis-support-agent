# Demo Script

Project: **Aegis Support Agent**

Track: **Agents for Business**

---

## 1. Opening

Aegis is a trust-gated customer support agent for B2B SaaS teams.

The goal is to make AI-assisted support safer. Instead of directly sending AI-generated replies, Aegis separates the workflow into multiple agent roles and uses a judge agent to decide whether the response is safe enough to suggest.

---

## 2. Problem

Customer support teams often receive tickets about:

- billing
- refunds
- account access
- privacy
- security vulnerabilities
- technical bugs
- feature requests

AI can help draft responses, but direct automation can be risky when the issue involves money, security, privacy, or account changes.

Aegis solves this with a trust gate.

---

## 3. Architecture

The workflow is:

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

suggest_reply
human_review
escalate

---

## 4. Concepts Demonstrated

Aegis demonstrates:

- multi-agent workflow
- MCP-style tool use
- A2A-style structured message passing
- policy grounding
- judge agent evaluation
- trust scoring
- human-in-the-loop escalation
- evaluation harness
- error analysis

---

## 5. Live Demo Command: Billing Ticket

Run:

python -m src.main --message "I was charged twice this month. Please refund me now." --mode rule

Expected behavior:

- Category: billing
- Risk level: medium
- Decision: human_review
- Reason: refund or duplicate charge needs verification

Explain:

The agent does not promise a refund. It drafts a safe response and routes the ticket to human review.

---

## 6. Live Demo Command: Security Ticket

Run:

python -m src.main --message "I found a security bug that exposes customer emails." --mode rule

Expected behavior:

- Category: security
- Risk level: high
- Decision: escalate

Explain:

Security reports are automatically escalated. The response avoids asking for secrets and avoids confirming the vulnerability before review.

---

## 7. Run Full Pipeline

Run:

./run_all.sh rule

This runs:

- support-agent pipeline
- evaluation
- error analysis
- confusion matrix

Generated files:

data/aegis_results.json
data/evaluation_report.json
data/error_analysis.json
data/confusion_matrix.json

---

## 8. Evaluation

Aegis evaluates predictions against the included synthetic dataset.

Metrics:

- category accuracy
- risk accuracy
- decision accuracy

Evaluation report:

data/evaluation_report.json

Explain:

The dataset is small and synthetic, so the metrics validate the workflow rather than claiming production-level performance.

---

## 9. Safety Design

Aegis escalates or routes to human review for:

- refunds
- duplicate charges
- cancellations
- security vulnerabilities
- privacy requests
- data deletion
- account access changes

The agent avoids:

- promising refunds before verification
- asking for passwords or API keys
- confirming data deletion before verification
- confirming security vulnerabilities before review
- inventing account-specific facts

---

## 10. Closing Pitch

Aegis is not just a chatbot. It is a trust-gated support workflow.

It shows how a business agent can:

- read a customer ticket
- retrieve policy context
- draft a response
- judge its own output
- assign a trust score
- escalate risky cases to humans

This makes the agent safer, more explainable, and more suitable for real business workflows.

---

## 11. Future Work

Future improvements:

- Replace rule-based agents with live Gemini-powered agents.
- Convert local policy lookup into a real MCP server.
- Add a larger public support-ticket dataset.
- Add LLM-as-judge evaluation.
- Connect to a real ticketing system or CRM.
- Add a web UI or interactive notebook demo.
