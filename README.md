📘 Clara Onboarding Automation Engine
Overview

This project implements a structured automation pipeline that converts real-world customer conversations into production-ready AI voice agent configurations.

It simulates Clara Answers’ real onboarding workflow:

Human Conversation
        ↓
Structured Account Memo
        ↓
Versioned Agent Configuration
        ↓
Deployable Prompt

The system cleanly separates:

v1 → Demo-derived assumptions

v2 → Onboarding-confirmed operational rules

The goal is to safely transition from exploratory information to production configuration without hallucination or silent assumptions.

🧠 Problem Statement

Service-trade businesses (electrical, HVAC, fire protection, etc.) have:

Emergency routing logic

Business hour constraints

After-hours escalation rules

Pricing policies

CRM integrations

Transfer fallback logic

Demo calls provide directional understanding.
Onboarding calls provide operational precision.

This system ensures:

No configuration is invented.

Demo assumptions are preserved.

Onboarding overrides are explicit.

Version history is maintained.

Missing data is tracked responsibly.

🏗 Architecture
dataset/
  demo_calls/
  onboarding_calls/

scripts/
  schema.py
  extract.py
  extract_onboarding.py
  patch.py
  pipeline_demo.py
  pipeline_onboarding.py
  prompt_generator.py
  run_all.py

outputs/
  accounts/
    account_XXX/
      v1/
      v2/
🔹 Stage 1 — Demo Processing (v1)

The demo transcript is parsed to generate:

account_memo.json

agent_spec.json

Constraints:

Only explicitly stated information is extracted.

Missing operational details are added to questions_or_unknowns.

No assumptions are made.

Example unknowns tracked:

Business hours

Transfer timeout rules

Timezone

Pricing structure

🔹 Stage 2 — Onboarding Processing (v2)

The onboarding transcript:

Confirms exact business hours

Defines emergency routing

Clarifies after-hours logic

Introduces pricing policies

Adds transfer fallback rules

The system:

Loads v1 memo

Extracts onboarding updates

Applies field-level patching

Generates a structured changelog

Removes resolved unknowns

Regenerates agent prompt

Saves v2 output

🔄 Patch Logic (Safe Override System)

The patch engine:

Updates only fields with new confirmed values

Preserves unrelated demo data

Logs every change

Supports nested dictionaries (e.g., business_hours)

Supports list overrides (e.g., emergency_routing_rules)

This ensures:

No silent overwriting

Clear version diff visibility

Deterministic updates

📝 Changelog Example
{
  "field": "business_hours.start",
  "old": "",
  "new": "8:30 AM",
  "reason": "Updated from onboarding"
}

This makes configuration evolution auditable.

🎙 Agent Prompt Discipline

The generated agent prompt enforces:

Business Hours Flow

Greeting

Purpose capture

Name & number collection

Routing / transfer

Transfer fallback

Close

After-Hours Flow

Greeting

Emergency confirmation

Emergency detail capture

Conditional patch-through

Non-emergency logging

Close

The prompt:

Does not invent pricing

Does not auto-confirm bookings

Does not guarantee availability

Follows onboarding-confirmed constraints

🛡 Handling Uncertainty

The system explicitly tracks unresolved configuration fields in:

"questions_or_unknowns"

Resolved unknowns are removed during onboarding.

Remaining unknowns reflect real operational ambiguity.

This prevents hallucination and ensures safe deployment behavior.

⚙️ How to Run

From project root:

python -m scripts.run_all

Outputs will be generated in:

outputs/accounts/account_XXX/
📈 Engineering Properties

This system is:

Repeatable

Batch-capable

Idempotent

Version-controlled

Deterministic

Auditable

Extendable to structured onboarding forms

🔮 Future Improvements

Timezone detection

Transfer timeout configuration

Structured onboarding form ingestion

Validation layer for incomplete configuration

Diff visualization UI

🧪 What This Demonstrates

This project demonstrates:

Schema design for operational logic

Safe configuration merging

Version discipline

Controlled override handling

Responsible uncertainty management

Prompt generation based on structured state

It is designed as a reusable internal onboarding automation engine, not a one-off script.

🎯 Final Result

For the Ben’s Electric case:

v1 reflects demo-level assumptions.

v2 reflects onboarding-confirmed precision.

Emergency logic is refined.

Business hours are confirmed.

Pricing policy is conditional.

Only unresolved fields remain in unknowns.
