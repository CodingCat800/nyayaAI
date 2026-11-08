# NyayaAI — Kuku AI Generalist Assignment (Problem 2)

A narrow prototype for people in India who have not received a refund for an online purchase/service.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Optional LLM
The app works without credentials using a deterministic fallback. To connect an OpenAI-compatible Chat Completions endpoint, copy `.env.example` to `.env` and set `NYAYAI_LLM_BASE_URL`, `NYAYAI_LLM_API_KEY`, and `NYAYAI_LLM_MODEL`. The LLM structures user facts; official guidance remains separate and static. Avoid sending sensitive identifiers to external models.

## Scope and assumptions
- Problem 2 from the Kuku brief; online purchase/service refund not received after cancellation/return.
- English text-only MVP. No voice, OCR, uploads, court filing, legal representation, or general Indian-law coverage.
- The 7-day response request in the draft is a proposed communication deadline, not a statutory deadline.
- No conclusion about liability is made without document review and full facts.

## Architecture
Streamlit intake → optional swappable LLM JSON extraction → deterministic fallback if unavailable → fixed source-backed guidance → user-editable complaint draft.

## Quality checks
`python -m unittest discover -s tests -v`. Test cases are in `tests/test_cases.json`; unedited sample outputs are in `raw_outputs/`.

## Official sources
- Consumer Protection Act, 2019: https://www.indiacode.nic.in/bitstream/123456789/15256/1/eng201935.pdf
- Consumer Protection (E-Commerce) Rules, 2020: https://consumeraffairs.nic.in/sites/default/files/E%20commerce%20rules_0.pdf
- National Consumer Helpline process: https://consumerhelpline.gov.in/public/index.php/about
- NCH contact: https://consumerhelpline.gov.in/public/contact

## AI use and known failure
ChatGPT assisted with scope, code, and test design. A likely model failure is confidently filling missing dates, legal provisions, or entitlement from incomplete facts. Mitigations: constrained JSON, static guidance separated from generated output, missing-fact prompts, placeholders, and disclaimer. The optional LLM path still needs adversarial testing and legal review.

## Before production
Add reviewed multilingual intake, OCR with consent, a versioned legal knowledge base tagged by jurisdiction/effective date, citations at claim level, privacy controls, advocate escalation, and lawyer-led evaluation.
