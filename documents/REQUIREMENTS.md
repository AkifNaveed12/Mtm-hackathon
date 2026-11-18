# HackPlan AI — System Requirements & Traceability

## Source correction and verification authority

The PDF was inspected in full on 18 November 2026. This document's earlier sample-specific figures are examples, not constraints for unseen packs. The official brief does not mandate a generator, a specific venue, or standard-tier meals. Required judges are calculated from workload; the sample can use 17 assigned of 20 available judges, producing the brief's 177 meals without hardcoding that number. Explicit source attendance and committed payments override generated staffing choices. Small-model bonus eligibility requires the organizers' list; it must never be assumed from a model name.

The current request requires local operation only: no commit, push, deployment, voice, or live WhatsApp send. The implementation and test mapping, actual performance, external blockers, and incomplete requirements are tracked in root `PROJECT_COMPLETION_REPORT.md`. The backend must identify unsupported constraints instead of silently passing them.

## 1. Requirement Priorities

- **P0 (Mandatory MVP)**: Strict hackathon competition requirements. Failure to satisfy any P0 results in point deduction or disqualification.
- **P1 (Important / Differentiators)**: High-impact features that maximize scoring (UI points, Small-Model Bonus, lean token usage, oral exam preparedness).
- **P2 (Optional / Refinements)**: Polishing, secondary visual aids, extended simulations.

---

## 2. Functional Requirements (P0 & P1)

### REQ-F01: Universal File-Based Message Ingestion
- **Priority**: P0
- **Theme Reference**: Brief Point 1: *"Read every message from a text file, exactly as given. Do not type facts into your code."*
- **Description**: The system must ingest raw message packs from any supplied text file path. Zero hardcoded facts, dates, prices, or room capacities are permitted in source code.
- **Acceptance Criteria**: Running against an unseen text file correctly parses all sender headers, timestamps, and message bodies without runtime errors or reliance on pre-baked constants.

### REQ-F02: Single-Command Execution Interface
- **Priority**: P0
- **Theme Reference**: Brief Point 2: *"Take every message in the same way, through the same command. No flags, hints, or edits from you."*
- **Description**: The system must execute from a single standardized shell command (`python run.py <filepath>`) requiring no manual parameters, interactive prompts, or developer hints.
- **Acceptance Criteria**: Command runs non-interactively from start to finish, generating the full plan and terminal trace.

### REQ-F03: Standardized Trace Generation & Token Accounting
- **Priority**: P0
- **Theme Reference**: Brief Point 3 & Points Scoring (30 pts output, 5 pts token use): *"Print a trace: every model call numbered, with the model name, one area tag... its input, its output, and its token counts... End the trace with total tokens."*
- **Description**: Every model call must be logged in a strict, uniform schema:
  1. Sequential Call Number (1, 2, ...).
  2. Model Name (e.g., `llama-3.1-8b-instant`).
  3. Single Area Tag chosen strictly from: `reading`, `venue`, `schedule`, `food`, `judging`, `budget`.
  4. Exact Model Input (prompt).
  5. Exact Model Output (response).
  6. Token Counts (Prompt Tokens, Completion Tokens, Total Tokens) as reported by the provider.
  7. Final Summary: Aggregate token tally across all calls.
- **Acceptance Criteria**: Trace displays completely in stdout and in the Web UI. A trace that misreports tokens, models, or area tags is grounds for disqualification.

### REQ-F04: Incremental Message Updates Under Tight Limits
- **Priority**: P0
- **Theme Reference**: Brief Point 4 & Limits: *"Accept new messages after the first run, and update the existing plan... at most 5 model calls and cut off after 1 minute."*
- **Description**: After the initial run, the system must accept individual new messages, determine affected domains, and update the existing plan using <= 5 model calls in < 60 seconds.
- **Acceptance Criteria**: Ingesting a change message (e.g. printing cost from 10k to 15k) updates the budget without re-evaluating venue, schedule, or judging, using <= 5 model calls and completing in < 10 seconds.

### REQ-F05: Conflict Detection & Sabotage Message Rejection
- **Priority**: P0
- **Theme Reference**: Brief Point 5 & Scoring (20 pts): *"When a message conflicts with a rule or with other facts, keep the plan valid and print the reason in the trace."*
- **Description**: When a new message contradicts physical, financial, or operational invariants, the system must reject the mutation, keep the plan at its last valid state, and print a clear justification in the trace.
- **Acceptance Criteria**: When presented with a message reducing food boxes to 100 for 177 people, the system rejects it, preserves the previous catering order, and logs: *"REJECTED: Catering boxes (100) below required headcount (177). Rule violated: Every attendee and staff member must be fed."*

### REQ-F06: Six Core Operational Quality Checks
- **Priority**: P0
- **Theme Reference**: Scoring Table (30 pts): *"Your plan from the unseen pack passes six checks: correct figures, within budget, venue fits, schedule valid, enough judges, all areas covered."*
- **Description**: The final plan must strictly satisfy:
  1. *Check 1 (Figures)*: All arithmetic is mathematically sound (sums, unit rates, quantities).
  2. *Check 2 (Budget)*: Total event expenditure <= approved budget (Rs 650,000).
  3. *Check 3 (Venue)*: Selected venue capacity >= total attendees (150 students + 10 staff + 20 judges = 180 seats), with backup power.
  4. *Check 4 (Schedule)*: Exactly 4 hours, incorporates mandatory 15-minute prayer break, allocates valid judging intervals.
  5. *Check 5 (Judges)*: Number of confirmed judges satisfies team evaluation load (<= 3 teams per judge for 50 teams -> at least 17 judges; 20 available).
  6. *Check 6 (Coverage)*: All five operational areas (`venue`, `schedule`, `food`, `judging`, `budget`) fully planned and populated.
- **Acceptance Criteria**: System output explicitly reports status (PASS/FAIL) for all 6 checks.

### REQ-F07: Interactive Web Dashboard & Trace Visualizer
- **Priority**: P1 (10 Points UI Score)
- **Theme Reference**: Brief UI section: *"A user interface is now scored. Show your plan, your trace and any rejected messages clearly. A web page, an app, or well-formatted terminal output can all score well."*
- **Description**: A responsive Next.js web application offering:
  - 5-Area Overview Cards.
  - 6-Check Compliance Banner.
  - Live Model Call Trace Viewer with collapsible prompt/response cards.
  - Rejected Messages Log with highlighted rationale.
  - Interactive What-If Message Injector.
  - Plan & Trace Export button.
- **Acceptance Criteria**: Evaluators can inspect the plan, explore model traces, and test new messages via an intuitive, professional UI.

### REQ-F08: Small-Model Optimization & Bonus Compliance
- **Priority**: P1 (10 Points Bonus Score)
- **Theme Reference**: Brief Bonus section: *"10 points. You earn it if every model call in your runs uses a model on the organizers' small-model list, which includes any model running on your own laptop."*
- **Description**: Configure primary pipeline to utilize lightweight models (e.g. `llama-3.1-8b-instant` via Groq or local Ollama), minimizing token overhead while maintaining 100% extraction accuracy.
- **Acceptance Criteria**: Model name in all trace calls corresponds to a verified small model.

### REQ-F09: Predictable Area-Call Routing
- **Priority**: P1 (5 Points Prediction Score + 10 Points Handling Change)
- **Theme Reference**: Brief Scoring: *"Before one of them, write down which areas will make model calls and hand the slip to the volunteer... only the affected areas made model calls."*
- **Description**: The system must follow a deterministic, documentable dispatch logic so team members can accurately predict which areas will make model calls before a message is executed.
- **Acceptance Criteria**: Message regarding venue only calls `reading` + `venue`; message regarding printing only calls `reading` + `budget`.

---

## 3. Non-Functional Requirements (P0 & P1)

### REQ-NF01: Execution Speed & Cutoff Limits
- **Priority**: P0
- **Description**:
  - Full run execution must terminate in < 120 seconds (target: < 25 seconds).
  - Incremental update execution must terminate in < 60 seconds (target: < 5 seconds).
- **Verification**: Built-in stopwatch benchmark logged in trace.

### REQ-NF02: Token Efficiency
- **Priority**: P0
- **Description**: Total tokens consumed must be among the lowest in the competition by avoiding conversational boilerplate and computing math deterministically.
- **Target**: Full run < 2,500 total tokens; incremental update < 500 tokens.

### REQ-NF03: Robust Multilingual & Roman Urdu Understanding
- **Priority**: P0
- **Description**: Ingest and accurately extract facts from Pakistani colloquial English and Roman Urdu (e.g., *"Salam bhai! Standard lunch box ab Rs 1,200 per head hoga, basic wala Rs 800. Delivery free hai."*).
- **Verification**: Automated test suite with Roman Urdu fixtures.

### REQ-NF04: Fault Tolerance & Graceful Degradation
- **Priority**: P0
- **Description**: If a primary LLM provider drops or times out, the system automatically falls back to an alternate provider or local model without crashing.

### REQ-NF05: Zero Secret Leakage
- **Priority**: P0
- **Description**: API keys, credentials, and internal tokens must never be logged, printed in traces, or bundled into frontend artifacts.

---

## 4. Traceability Matrix

| Official Theme Requirement | System Requirement ID | Architecture Module | Verification Method |
|---|---|---|---|
| Read text file, no facts in code | REQ-F01 | `reading` Engine | Test with alternate text files |
| Single command execution | REQ-F02 | CLI Harness (`run.py`) | Volunteer test execution |
| Numbered trace, model, area tag, tokens | REQ-F03 | Global Execution Tracer | Automated trace schema validator |
| Incremental updates (<=5 calls, <1m) | REQ-F04 | Domain Dispatcher | Dynamic message test suite |
| Conflict rejection & valid plan | REQ-F05 | Constraint Solver | Sabotage message unit tests |
| 6 Operational Checks | REQ-F06 | 6-Point Verification Gate | Automated compliance suite |
| User Interface scored | REQ-F07 | Next.js Dashboard | UI evaluation & browser testing |
| Small-Model Bonus | REQ-F08 | Groq Llama-3.1-8B Client | Trace inspection by judges |
| Selective Area Calling | REQ-F09 | Semantic Router | Volunteer prediction slip test |
