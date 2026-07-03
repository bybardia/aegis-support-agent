# Aegis: Trust-Gated Support Agent

Aegis is a trust-gated customer support agent for B2B SaaS teams.

Instead of directly sending AI-generated replies, Aegis uses a multi-agent workflow to read a customer ticket, retrieve policy context through a real MCP server, draft a response with Gemini, judge the response with Gemini, assign a trust score, and escalate risky cases to humans. A deterministic trust gate always has the final say on high-risk cases.

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
  -> Triage Agent
  -> Policy Lookup (MCP server)
  -> Draft Response Agent (Gemini)
  -> Judge Agent (Gemini)
  -> Reflection Agent
  -> Judge Agent (Re-evaluation)
  -> Trust Gate (deterministic)
  -> Final Decision: suggest_reply | human_review | escalate

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

### Policy Lookup (MCP server)

Retrieves the relevant policy from the `policies/` folder and exposes it as a real MCP tool (`policy_lookup`) through `src/mcp_server.py` (stdio transport).

### Draft Response Agent

Drafts a safe response with Google Gemini using the customer message, triage result, and retrieved policy. Falls back to a deterministic template draft when no API key is configured.

### Judge Agent

Evaluates the draft with Google Gemini using structured JSON output and produces:

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

A deterministic trust gate is enforced on top of the model output: high-risk security and privacy tickets are always escalated regardless of the model's decision.

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
- real MCP server (stdio) exposing a policy_lookup tool
- Gemini-powered drafting and judging with structured output
- agent skills (modular SKILL.md capabilities loaded per ticket category)
- A2A-inspired structured communication using Pydantic schemas
- reflection and self-correction
- evidence-based judging
- deterministic trust gate and trust re-scoring
- explainable trust scoring
- human-in-the-loop escalation
- evaluation harness
- error analysis
- confusion matrix reporting

---

## MCP Server

Aegis exposes its policy tool through a real MCP server:

- `src/mcp_server.py` - a FastMCP server exposing `policy_lookup(category)` over stdio.
- `src/mcp_client_demo.py` - a sample MCP client that launches the server and calls the tool.

Install and run the demo:

    pip install mcp
    python -m src.mcp_client_demo

Expected output:

    Available tools: ['policy_lookup']
    policy_lookup('billing') ->
    # Billing Policy ...

For reproducibility, the main pipeline calls `policy_lookup` directly, while the MCP server exposes the same tool as a standards-compliant MCP interface. In a production system this server could be connected to a knowledge base, CRM, billing system, or ticketing platform.

---

## A2A-inspired Structured Communication

Aegis passes typed Pydantic messages between workflow stages:

TriageResult -> DraftResult -> JudgeResult -> FinalResult

This makes the workflow easier to debug, evaluate, and extend while maintaining clear contracts between agents.

---

## Project Structure

    aegis-support-agent/
    ├── README.md
    ├── PROJECT_SUMMARY.md
    ├── LICENSE
    ├── requirements.txt
    ├── run_all.sh
    ├── .env.example
    ├── data/
    ├── docs/
    ├── notebooks/
    ├── policies/
    ├── skills/
    └── src/
        ├── main.py
        ├── agents.py
        ├── gemini_agents.py
        ├── mcp_server.py
        ├── mcp_client_demo.py
        ├── skills.py
        ├── tools.py
        ├── schemas.py
        └── config.py

---

## Setup

Create a virtual environment and install dependencies.

macOS / Linux:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Windows (PowerShell):

    python -m venv .venv
    .venv\Scripts\Activate
    pip install -r requirements.txt

### API key (for Gemini mode)

Gemini mode requires a Google Gemini API key. Provide it via an environment variable or a local `.env` file (never commit it):

    # .env
    GEMINI_API_KEY=your_key_here

On Kaggle, use Kaggle Secrets to provide `GEMINI_API_KEY`.

If no key is set, Gemini mode automatically falls back to the deterministic rule pipeline, so the project stays fully reproducible.

---

## Run One Ticket

Rule mode:

    python -m src.main --message "I was charged twice this month. Please refund me now." --mode rule

Gemini mode:

    python -m src.main --message "I was charged twice this month. Please refund me now." --mode gemini

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

## Results

Aegis supports a deterministic rule mode and a Gemini-powered mode, evaluated on the included synthetic support-ticket dataset. Recent improvements include:

- Gemini-powered drafting and judging
- reflection-based self-correction
- policy-grounded evidence generation
- trust re-scoring after revision
- explainable decision traces

See `data/evaluation_report.json`.

The dataset is intentionally small and synthetic, so the metrics should be interpreted as a functional validation of the workflow rather than a production benchmark.

---

## Safety Design

High-risk security and privacy cases bypass reflection and are always escalated according to policy.

Aegis routes risky cases to human review or escalation. It escalates or reviews tickets involving:

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

- rule
- gemini

### Rule mode

Deterministic Python logic. Fully reproducible and requires no API key.

### Gemini mode

Uses Google Gemini for drafting and judging responses, with structured JSON output for the Judge. If no API key is configured (or an API call fails), Gemini mode safely falls back to the rule pipeline, keeping the project reproducible.

In all modes, the trust gate remains deterministic: high-risk security and privacy tickets are always escalated regardless of model output.

---

## Limitations

Known limitations:

- sample dataset is small and synthetic
- triage uses deterministic keyword logic (not yet LLM-powered)
- rule mode uses template-based drafts and heuristic judging by design
- the MCP server is backed by local policy files, not yet a production knowledge base or CRM
- there is no real CRM, billing, or ticketing integration yet

---

## Documentation

Additional documentation:

- PROJECT_SUMMARY.md
- docs/architecture.md
- docs/mcp_a2a.md
- docs/demo_script.md
- docs/submission_checklist.md

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

Final Decision: human_review
Trust Score: 87

---

## License

This project is licensed under the **Creative Commons Attribution 4.0 International (CC-BY 4.0)** license, as required by the Kaggle x Google Vibecoding Agents Capstone Project.

See the `LICENSE` file for the full legal text, or visit https://creativecommons.org/licenses/by/4.0/