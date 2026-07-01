# Aegis: Trust-Gated Support Agent

Aegis is a trust-gated customer support agent for B2B SaaS teams.

Instead of directly sending AI-generated replies, Aegis uses a multi-agent workflow to read a customer ticket, retrieve policy context, draft a response, judge the response, assign a trust score, and escalate risky cases to humans.

---

## Track

**Kaggle x Google Vibecoding Agents Capstone Project**

Selected track: **Agents for Business**

---

## Problem

Customer support teams often receive tickets involving billing, refunds, account access, privacy, security vulnerabilities, technical bugs, and feature requests.

AI can help draft support replies, but direct automation can be risky when the issue involves:

- money
- security
- privacy
- account access
- cancellation
- data deletion

Aegis solves this by adding a trust gate before any response is considered safe.

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
Reflection Agent
        ↓
Judge Agent (Re-evaluation)
        ↓
Trust Gate
        ↓
Final Decision
├── suggest_reply
├── human_review
└── escalate

Responses below the trust threshold are automatically revised and re-evaluated before final routing.

---

## Agent Roles

### Triage Agent

Classifies the customer ticket into a category and risk level.

Categories include:

- billing
- security
- privacy
- account_access
- technical_bug
- feature_request
- general

### Policy Lookup Tool

Retrieves the relevant policy from the `policies/` folder.

This is the project’s MCP-style tool interface.

### Draft Response Agent

Creates a safe draft response using:

- the customer message
- triage result
- retrieved policy

### Judge Agent

Evaluates the draft response and produces:

- helpfulness score
- policy compliance score
- hallucination risk score
- trust score
- evidence list
- final routing decision
- reason

The Judge Agent also performs:

- policy-grounded evaluation
- evidence generation
- trust re-scoring after reflection
- explainable routing decisions

### Reflection Agent

Revises low-trust draft responses before final routing.

The Reflection Agent:

- improves response safety
- adds verification language when needed
- tracks revision count
- enables self-correction workflows

Revised responses are sent back to the Judge Agent for re-evaluation.

### Escalation Agent

Creates an internal note for a human support agent when the ticket requires review or escalation.

---


## Key Agentic Concepts

- multi-agent workflow
- MCP-style tool use
- A2A-style structured message passing
- policy grounding
- reflection and self-correction
- evidence-based judging
- trust re-scoring
- explainable trust scoring
- human-in-the-loop escalation
- evaluation harness
- error analysis
- confusion matrix reporting
---

## MCP-style Tool Use

Aegis includes a local MCP-style tool:

policy_lookup(category)

Input:

support category

Output:

relevant policy text

In a production system, this could be replaced with a real MCP server connected to a knowledge base, CRM, billing system, or ticketing platform.

---

## A2A-style Structured Communication

Aegis passes structured messages between agents using Pydantic schemas:

TriageResult → DraftResult → JudgeResult → FinalResult

This makes the workflow easier to debug, evaluate, and extend.

---

## Project Structure

aegis-support-agent/
├── README.md
├── README_CLEAN.md
├── PROJECT_SUMMARY.md
├── LICENSE
├── requirements.txt
├── run_all.sh
├── data/
├── docs/
├── notebooks/
├── policies/
└── src/

---

## Setup

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

---

## Run One Ticket

python -m src.main --message "I was charged twice this month. Please refund me now." --mode rule

---

## Run Full Pipeline

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

## Evaluation

Aegis includes an evaluation harness that compares predicted labels against expected labels in:

data/sample_tickets.csv

Metrics include:

- category accuracy
- risk accuracy
- decision accuracy

The evaluation report is saved to:

data/evaluation_report.json

---

## Final MVP Results

The current rule-based MVP was evaluated on the included synthetic support-ticket dataset.
Recent improvements include:

- reflection-based self-correction
- policy-grounded evidence generation
- trust re-scoring after revision
- explainable decision traces

See:

data/evaluation_report.json

The dataset is intentionally small and synthetic, so the metrics should be interpreted as a functional validation of the workflow rather than a production benchmark.

---

## Safety Design

High-risk security and privacy cases bypass reflection and are always escalated according to policy.

Aegis routes risky cases to human review or escalation.

It escalates or reviews tickets involving:

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
- confirming vulnerabilities before security review
- inventing account-specific facts

---

## Agent Modes

Aegis supports two modes:

rule
gemini

### Rule mode

The stable MVP mode. It uses deterministic Python logic.

### Gemini mode

A compatibility path for future Gemini-powered agents.

In the current MVP, Gemini mode uses a safe stub that calls the same stable rule-based pipeline. This keeps the project reproducible without requiring an API key.

---

## Limitations

The current version is a rule-based MVP.

Known limitations:

- sample dataset is small and synthetic
- triage uses deterministic keyword logic
- draft responses are template-based
- judge scoring is heuristic-based and not yet LLM-powered
- Gemini mode is currently a stub
- policy lookup is local file retrieval, not a production MCP server
- there is no real CRM, billing, or ticketing integration yet

---

## Documentation

Additional documentation:

PROJECT_SUMMARY.md
docs/architecture.md
docs/mcp_a2a.md
docs/demo_script.md
docs/submission_checklist.md

---

## Example Decision Trace

Billing Ticket

Input:
"I was charged twice this month. Please refund me."

Output:

- category=billing
- risk_level=medium
- policy_loaded=billing
- refund request detected
- duplicate charge detected
- billing policy requires invoice verification before refund
- response revised 1 time(s)
- policy grounding successful
- human review required
- response revised 1 time(s)

Final Decision:
human_review

Trust Score:
87

## License

This project is intended to be compatible with the Kaggle x Google Vibecoding Agents Capstone Project winner license requirement: **CC-BY 4.0**.

Full license text:

