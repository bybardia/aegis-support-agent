# Aegis Support Agent

Aegis is a trust-gated customer support agent for B2B SaaS teams.

Instead of directly sending AI-generated replies to customers, Aegis separates the support workflow into multiple agent roles:

1. Triage Agent
2. Policy Lookup Tool
3. Draft Response Agent
4. Judge Agent
5. Escalation Agent

The goal is to make AI support safer by adding evaluation, policy grounding, trust scoring, and human-in-the-loop escalation.

---

## Project Track

**Kaggle x Google Vibecoding Agents Capstone Project**

Track: **Agents for Business**

---

## Problem

Customer support teams often receive repetitive tickets about billing, account access, privacy, security, bugs, and feature requests.

AI can help draft responses, but direct automation can be risky when the issue involves:

- refunds
- account access
- security vulnerabilities
- privacy or data deletion
- customer anger or cancellation

Aegis solves this by using a trust gate. The system drafts a response, evaluates it, assigns a trust score, and decides whether the response should be suggested, reviewed by a human, or escalated.

---

## How It Works

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

## Agent Roles

### 1. Triage Agent

Classifies the customer ticket into a support category and risk level.

Example categories:

- billing
- security
- privacy
- account_access
- technical_bug
- feature_request
- general

### 2. Policy Lookup Tool

Retrieves the relevant internal policy from the `policies/` folder.

This gives the system a simple tool-use layer and prevents the response from relying only on model memory.

### 3. Draft Response Agent

Creates a safe draft response for the customer using the ticket, category, risk level, and policy.

### 4. Judge Agent

Evaluates the draft response and produces:

- helpfulness score
- policy compliance score
- hallucination risk score
- trust score
- final routing decision
- reason

### 5. Escalation Agent

Creates an internal note for a human support specialist when the ticket requires review or escalation.

---

## Key Concepts Demonstrated

This project demonstrates several agentic AI concepts:

- Multi-agent workflow
- Agent-to-agent structured message passing
- Tool use
- Policy grounding
- Evaluation harness
- Trust scoring
- Human-in-the-loop escalation
- Safe response generation

---

## MCP-style Tool Use

Aegis includes a simple MCP-style tool interface:

policy_lookup(category)

The tool accepts a support category and returns the relevant policy document.

In a production version, this could be replaced with a real MCP server connected to:

- a knowledge base
- support documentation
- CRM
- ticketing system
- billing system

---

## A2A-style Agent Communication

Aegis uses structured outputs between agents.

Example:

Triage Agent → TriageResult
Draft Agent → DraftResult
Judge Agent → JudgeResult
Final Pipeline → FinalResult

This makes the agent workflow easier to debug, evaluate, and extend.

---

## Project Structure

aegis-support-agent/
├── README.md
├── LICENSE
├── requirements.txt
├── .env.example
├── data/
│   ├── sample_tickets.csv
│   ├── aegis_results.json
│   └── evaluation_report.json
├── policies/
│   ├── account_access.md
│   ├── billing.md
│   ├── feature_request.md
│   ├── general.md
│   ├── privacy.md
│   ├── security.md
│   └── technical_bug.md
├── src/
│   ├── agents.py
│   ├── config.py
│   ├── evaluator.py
│   ├── main.py
│   ├── schemas.py
│   └── tools.py
├── docs/
├── notebooks/
└── prompts/

---

## Setup

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

---

## Run One Ticket

python -m src.main --message "I was charged twice this month. Please refund me now."

---

## Run Sample Tickets

python -m src.main --sample data/sample_tickets.csv

This saves results to:

data/aegis_results.json

---

## Run Evaluation

python -m src.evaluator --sample data/sample_tickets.csv

This saves the evaluation report to:

data/evaluation_report.json

---

## Example Output

{
"ticket_id": "manual",
"summary": "Customer issue categorized as billing with medium risk.",
"category": "billing",
"risk_level": "medium",
"trust_score": 72,
"decision": "human_review",
"reason": "Medium-risk issue should be reviewed before final customer action."
}

---

## Evaluation

Aegis includes a simple evaluation harness that compares predicted labels against expected labels in `data/sample_tickets.csv`.

Current metrics include:

- category accuracy
- risk accuracy
- decision accuracy

This is intentionally simple for the MVP, but it can be extended with LLM-as-judge scoring, confusion matrices, and qualitative review.

---

## Safety Design

Aegis is designed to avoid unsafe automation.

It escalates or routes to human review when tickets involve:

- security vulnerabilities
- privacy requests
- data deletion
- refunds
- duplicate charges
- account access changes
- cancellations
- unresolved technical failures

The agent avoids:

- promising refunds without verification
- confirming security vulnerabilities before review
- asking for passwords or secrets
- confirming data deletion before verification
- inventing account-specific facts

---

## Current MVP Status

The current version is a rule-based MVP. This means the pipeline works without requiring an LLM API key.

Implemented:

- sample ticket dataset
- support policy files
- structured schemas
- policy lookup tool
- triage logic
- draft response logic
- judge logic
- escalation note generation
- command-line pipeline
- evaluation script
- JSON output reports

Next planned improvements:

- Gemini-powered agents
- stronger prompts
- MCP server version of policy lookup
- richer evaluation metrics
- notebook demo
- architecture documentation

---

## Reproducibility

To reproduce the current MVP:

git clone <your-repo-url>
cd aegis-support-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --sample data/sample_tickets.csv
python -m src.evaluator --sample data/sample_tickets.csv


The project does not require private competition data.

The sample dataset is included in:

data/sample_tickets.csv

---

## License

This project is intended to be compatible with the Kaggle x Google Vibecoding Agents Capstone Project winner license requirement: **CC-BY 4.0**.


---

## Attribution

This project was created for the Kaggle x Google Vibecoding Agents Capstone Project.

License: Creative Commons Attribution 4.0 International

Full license text: https://creativecommons.org/licenses/by/4.0/

---

## Agent Modes

Aegis currently supports two agent modes:

rule
gemini


### Rule mode

Rule mode is the stable MVP mode.

It uses deterministic Python logic for:

- triage
- draft response generation
- judging
- escalation notes

Run with:

python -m src.main --message "I was charged twice this month. Please refund me now." --mode rule

Or:

python -m src.main --sample data/sample_tickets.csv --mode rule

### Gemini mode

Gemini mode is included as a compatibility path for future Gemini-powered agents.

In the current MVP, `gemini` mode uses a safe stub that calls the same stable rule-based pipeline. This keeps the project reproducible without requiring an API key.

Run with:

python -m src.main --message "I found a security bug that exposes customer emails." --mode gemini

Or:

python -m src.main --sample data/sample_tickets.csv --mode gemini

### Evaluation by mode

The evaluator also supports mode selection:

python -m src.evaluator --sample data/sample_tickets.csv --mode rule
python -m src.evaluator --sample data/sample_tickets.csv --mode gemini

This makes it possible to compare the stable rule-based MVP with future Gemini-powered behavior.

---

## Error Analysis

Aegis includes a simple error analysis script:

python -m src.error_analysis --sample data/sample_tickets.csv --mode rule

It identifies tickets where the predicted category, risk level, or routing decision does not match the expected label.

The report is saved to:

data/error_analysis.json

---

## Confusion Matrix

Aegis includes a simple confusion matrix script:

python -m src.confusion_matrix --sample data/sample_tickets.csv --mode rule

It creates confusion matrices for:

- category prediction
- risk prediction
- decision prediction

The report is saved to:

data/confusion_matrix.json

---

## Run the Full Pipeline

To run the full MVP pipeline, evaluation, error analysis, and confusion matrix:

./run_all.sh rule

To run the Gemini-compatible mode:

./run_all.sh gemini

Generated files:

data/aegis_results.json
data/evaluation_report.json
data/error_analysis.json
data/confusion_matrix.json

---

## Repository Hygiene

The project includes a `.gitignore` file to avoid committing:

- local virtual environments
- `.env` files
- Python cache files
- Jupyter checkpoints
- editor files
- temporary files

Do not commit API keys or private credentials.


---

## Final MVP Results

The current rule-based MVP was evaluated on the included synthetic support-ticket dataset.

Evaluation file:

data/evaluation_report.json

Results:

| Metric | Value |
|---|---:|
| Total tickets | 10 |
| Category accuracy | 100.00% |
| Risk accuracy | 100.00% |
| Decision accuracy | 100.00% |

These results are from the local MVP evaluation harness.

The dataset is intentionally small and synthetic, so these metrics should be interpreted as a functional validation of the pipeline rather than a production benchmark.

---

## Limitations

The current version of Aegis is a rule-based MVP.

Known limitations:

- The sample dataset is small and synthetic.
- Triage is based on deterministic keyword logic.
- Draft responses are template-based.
- The Judge Agent currently uses fixed scoring rules.
- Gemini mode is currently a compatibility stub, not a live Gemini-powered implementation.
- Policy lookup is implemented as local file retrieval, not a production MCP server.
- The project does not connect to a real CRM, billing system, or ticketing platform.
- Evaluation labels are manually defined for the included sample dataset.

These limitations are intentional for the MVP. The goal of this version is to demonstrate the full agentic workflow in a reproducible way before adding external systems or live model calls.

---

## Demo Script

A demo script for presenting the project is included at:

docs/demo_script.md

---

## Project Summary

A shorter project summary is available at:

PROJECT_SUMMARY.md
PROJECT_SUMMARY.md
cat >> docs/submission_checklist.md << 'EOF'

---

## Project Summary

- [x] Short project summary included.
- [x] One-line summary included.
- [x] Track stated clearly.
- [x] Key agentic concepts listed.
