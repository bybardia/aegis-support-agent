# Submission Checklist

This checklist is for the Kaggle x Google Vibecoding Agents Capstone Project submission.

Project: **Aegis Support Agent**

Track: **Agents for Business**

---

## 1. Competition Fit

- [x] Project fits one of the official tracks.
- [x] Selected track is clearly stated: Agents for Business.
- [x] Project solves a business support workflow problem.
- [x] Project demonstrates practical agent design.
- [x] Project does not depend on private competition data.

---

## 2. Core Agent Functionality

- [x] Accepts a customer support ticket as input.
- [x] Classifies the ticket category.
- [x] Assigns a risk level.
- [x] Retrieves relevant policy context.
- [x] Drafts a customer response.
- [x] Judges the draft response.
- [x] Produces a trust score.
- [x] Routes the ticket to suggest_reply, human_review, or escalate.
- [x] Creates an escalation note when needed.

---

## 3. Agentic Concepts

- [x] Multi-agent workflow.
- [x] Tool use through policy lookup.
- [x] MCP-style tool interface documented.
- [x] A2A-style structured communication documented.
- [x] Evaluation harness included.
- [x] Human-in-the-loop escalation included.
- [x] Safety and trust gate included.

---

## 4. Reproducibility

- [x] `requirements.txt` included.
- [x] Setup instructions included in README.
- [x] Sample data included.
- [x] Policies included.
- [x] Commands for running one ticket included.
- [x] Commands for running sample data included.
- [x] Commands for running evaluation included.
- [x] No private competition data required.
- [x] Notebook demo included.
- [ ] Final repository link added.
- [ ] Screenshots or demo video added if required.

---

## 5. Documentation

- [x] README included.
- [x] Architecture document included.
- [x] MCP and A2A design notes included.
- [x] Submission checklist included.
- [x] Safety design explained.
- [x] Evaluation approach explained.
- [x] Final results summarized in README.
- [x] Known limitations summarized in README.
- [x] Future improvements summarized in README.

---

## 6. Licensing

- [x] LICENSE file included.
- [x] CC-BY 4.0 compatibility stated.
- [x] Attribution section included.
- [x] External data/tools are minimal and accessible.
- [ ] Final GitHub repository license confirmed.

---

## 7. Evaluation

- [x] Sample ticket labels included.
- [x] Evaluation script included.
- [x] Category accuracy measured.
- [x] Risk accuracy measured.
- [x] Decision accuracy measured.
- [x] Evaluation report saved as JSON.
- [x] Error analysis added.
- [x] Confusion matrix included.
- [x] LLM-as-judge listed as optional future work.

---

## 8. Safety Review

- [x] Refunds require human review.
- [x] Duplicate charges require human review.
- [x] Security reports are escalated.
- [x] Privacy/data deletion requests are escalated.
- [x] Account access changes require review.
- [x] The agent does not ask for passwords or secrets.
- [x] The agent avoids account-specific claims without verification.
- [x] The agent avoids promising refunds or deletion before verification.

---

## 9. Final Submission Readiness

Before final submission:

- [x] Run all sample tickets.
- [x] Run evaluation.
- [x] Confirm generated JSON files exist.
- [x] Review README.
- [x] Review architecture document.
- [x] Review MCP/A2A notes.
- [x] Add notebook demo.
- [ ] Add final screenshots or short demo if needed.
- [ ] Push code to repository.
- [x] Confirm only one Kaggle submission will be made.
- [x] Confirm team size is within the limit.
- [x] Confirm license is correct.

---

## Current Status

The project currently has a working rule-based MVP.

Next recommended improvements:

1. Add a notebook demo.
2. Add Gemini-powered agents.
3. Add a real or simulated MCP server version.
4. Improve evaluation and error analysis.
5. Polish README with final results.


---

## Demo Materials

- [x] Demo script included.
- [x] Billing ticket demo command included.
- [x] Security ticket demo command included.
- [x] Full pipeline demo command included.
