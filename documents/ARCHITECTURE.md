# HackPlan AI — Technical Architecture & System Design

## Local implementation correction (18 November 2026)

The official PDF and the latest local-only user request take precedence over the illustrative sample numbers below. No deployment, Git commits/pushes, voice, or live WhatsApp sends are authorized. The implemented architecture uses FastAPI, Pydantic extraction, a finite LangGraph workflow, deterministic domain engines, and SQLite transactions/versioned state. Only actual provider calls appear as model calls; offline parsing is explicitly identified and has no invented token usage. Domain arithmetic requires no model calls.

Generator backup is a constraint only when messages require it. Choose among feasible source-provided options rather than requiring Hall B. The sample's 177-meal statement is reconciled by assigning the minimum 17 judges needed for 50 teams at three teams per judge, from 20 available judges. Generated assignments and selected attendance are distinguished from source facts; explicit attendance/expense instructions override this staffing assumption. Unsupported constraints remain unresolved and prevent a valid-plan claim.

The custom WhatsApp bot is an existing separate REST service. The backend stores recipient consent, previews, notifications, and signed-webhook records in a private local SQLite file. Network verification is read-only; live sending requires explicit server configuration plus individual confirmation. Its upstream send schema and public webhook relay remain subject to external verification.

## 1. Architectural Philosophy: Neuro-Symbolic Agentic Architecture

HackPlan AI employs a **Neuro-Symbolic Architecture** that divides event planning responsibilities between two complementary paradigms:

1. **Neural Component (Language Models)**:
   - Reserved strictly for unstructured language comprehension, intent parsing, multilingual extraction (English + Roman Urdu), and ambiguous context resolution.
   - Tagged explicitly with one of six permitted area tags: `reading`, `venue`, `schedule`, `food`, `judging`, `budget`.
2. **Symbolic Component (Deterministic Python Solvers)**:
   - Executes all arithmetic, capacity checks, schedule slot geometry, budget sums, and hard invariant validations.
   - Enforces the golden competition rule: *"Use a model where language needs reading, and plain code where arithmetic will do."*

This guarantees 0% mathematical hallucination, minimal token consumption, sub-second arithmetic verification, and transparent explainability for oral examination.

---

## 2. High-Level System Architecture

```
+-----------------------------------------------------------------------------------+
|                                 USER INTERFACES                                   |
|  +-------------------------------------+   +-----------------------------------+  |
|  |     CLI Harness: run.py             |   |     Next.js Web Dashboard         |  |
|  |     (Single Command for Judges)     |   |     (Interactive Live Console)    |  |
|  +-------------------------------------+   +-----------------------------------+  |
+------------------------------------------+----------------------------------------+
                                           | HTTP / CLI Bridge
                                           v
+-----------------------------------------------------------------------------------+
|                           FASTAPI CORE BACKEND ENGINE                             |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Module 1: Ingestion & Reading Agent (Area: 'reading')                       |  |
|  | - Parses raw text pack (Emails, WhatsApp, Notices, English & Roman Urdu)    |  |
|  | - Extracts Normalized Fact Deltas with Sender, Timestamp, and Domain Tags   |  |
|  +-----------------------------------------------------------------------------+  |
|                                          |                                        |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  | Module 7: Selective Domain Router & Conflict Arbiter                        |  |
|  | - Evaluates incoming facts against active plan                              |  |
|  | - Routes updates ONLY to affected domains (Predictable Dispatch)            |  |
|  +-----------------------------------------------------------------------------+  |
|           |                   |                  |               |                |
|           v                   v                  v               v                v
|  +----------------+  +----------------+  +---------------+  +----------+  +------------+
|  | Area: 'venue'  |  | Area:'schedule'|  |  Area: 'food' |  | 'judging'|  |  'budget'  |
|  | Capacity & Gen |  | 4h & Prayer Brk|  | 177+ Headcount|  | 20 Judges|  | Cap 650k   |
|  +----------------+  +----------------+  +---------------+  +----------+  +------------+
|           |                   |                  |               |                |
|           +-------------------+------------------+---------------+----------------+
|                                          |
|                                          v
|  +-----------------------------------------------------------------------------+  |
|  | Symbolic Invariant & 6-Point Verification Gate                              |  |
|  | [1] Figures Sound  [2] Budget <= 650k  [3] Venue >= 180  [4] Schedule = 4h  |  |
|  | [5] Judges >= 17   [6] All Areas Covered                                    |  |
|  |                                                                             |  |
|  | Outcome A: All Pass -> Update Active Plan                                   |  |
|  | Outcome B: Any Fail -> REJECT Message, Log Reason in Trace, Keep Plan Valid |  |
|  +-----------------------------------------------------------------------------+  |
|                                          |                                        |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  | Global Execution Tracer & Token Audit Engine                               |  |
|  | Logs: Call # | Model Name | Area Tag | Input | Output | In/Out/Total Tokens |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Core Modules & Responsibilities

### Module 1: Universal Message Ingestor (`reading`)
- Ingests raw text files without flags, hints, or pre-processing.
- Invokes a lightweight LLM tagged with `reading` to extract normalized operational claims:
  - Subject/Entity (Venue, Catering, Honorarium, Schedule, Miscellaneous).
  - Numerical parameters (Seats, Rates, Quantities, Timestamps).
  - Status (Firm approval, Proposed quote, Superseded quote, Informational chatter).
- Resolves temporal precedence (e.g. 12 Nov caterer message supersedes 20 Oct message).

### Module 2: Venue Specialist (`venue`)
- Validates room choices against required occupancy:
  - Participants (150) + Staff (10) + Judges (20) = 180 seats needed.
  - Room D (80 seats) -> REJECTED (Insufficient capacity).
  - Hall A (200 seats @ Rs 120,000) -> Plausible, but lacks backup power.
  - Hall B (200 seats @ Rs 150,000 + standby generator) -> SELECTED for Islamabad power resilience.
  - Hall C (300 seats @ Rs 220,000) -> Viable but wastes Rs 70,000 budget.

### Module 3: Schedule Specialist (`schedule`)
- Coordinates 240-minute (4-hour) physical event agenda:
  - 00:00 - 00:30 (30m): Check-in, opening address, problem briefing.
  - 00:30 - 02:45 (135m): Core build sprint.
  - 02:45 - 03:00 (15m): **Mandatory Prayer Break** (Dean's condition).
  - 03:00 - 03:45 (45m): **Judging Phase** (Concurrent evaluation: 50 teams / 20 judges = 2.5 teams/judge; 3 teams x 15m = 45m).
  - 03:45 - 04:00 (15m): Results tabulation, closing ceremony & awards.

### Module 4: Food & Catering Specialist (`food`)
- Manages catering orders:
  - Headcount = 177 confirmed (up to 180).
  - Standard lunch box @ Rs 1,200 = Rs 212,400 (or basic @ Rs 800 = Rs 141,600).
  - Rule Check: Any order < 177 is rejected outright.

### Module 5: Judging Resource Specialist (`judging`)
- Coordinates judge evaluation:
  - Confirmed judges = 20.
  - Honorarium: 20 x Rs 5,000 = Rs 100,000.
  - Evaluation ratio: 50 teams / 20 judges = 2.5 teams/judge (strictly <= 3 teams per judge).
  - Time per team: 15 minutes.

### Module 6: Budget & Financial Ledger (`budget`)
- Computes comprehensive ledger:
  - Approved Ceiling: Rs 650,000.
  - Committed Expenses: Prizes (Rs 100,000) + Backup Internet (Rs 20,000) + Printing (Rs 10,000) = Rs 130,000.
  - Venue (Hall B): Rs 150,000.
  - Food (Standard 180 boxes): Rs 216,000.
  - Judging Honoraria: Rs 100,000.
  - Total Base Spend: 130,000 + 150,000 + 216,000 + 100,000 = Rs 596,000.
  - Remaining Contingency: Rs 54,000.
  - Student DJ Request (Rs 50,000): Evaluated against surplus. Total with DJ = Rs 646,000 (Within budget!).

### Module 7: Conflict Arbiter & Invariant Engine
- Evaluates any proposed update against the 6 Checks:
  1. `check_figures`: Math is accurate.
  2. `check_budget`: Total <= Rs 650,000.
  3. `check_venue`: Capacity >= 180 with power backup.
  4. `check_schedule`: Total time = 240m with 15m prayer break.
  5. `check_judges`: Judges >= 17, teams/judge <= 3.
  6. `check_coverage`: All 5 areas present.
- If any check fails, the message is marked REJECTED, the previous valid plan is preserved, and a detailed diagnostic is written to the trace.

---

## 4. Execution Flow & State Machine

```
               [Raw Message Pack File]
                         |
                         v
                (run.py Entrypoint)
                         |
                         v
             [Universal Reading Agent]
                         |
          (Extracts Fact Stream + Deltas)
                         |
                         v
       [Domain Dispatcher: Selective Router]
        /        |          |         |            (venue) (schedule)   (food)   (judging) (budget)
        \        |          |         |        /
                         v
           [Synthesize Candidate Plan]
                         |
                         v
        <6-Point Invariant Verification Gate>
           /                                     [All Pass]                       [Any Fail]
          |                                 |
          v                                 v
   [Apply Mutation]                [REJECT Mutation]
   [Update Plan State]             [Preserve Last Valid Plan]
          |                        [Log Reason in Trace]
          \                                 /
           +---------------+---------------+
                           |
                           v
               [Append to Trace Log]
               [Tally Token Usage]
                           |
                           v
              [Output Trace & Summary]
              [Render Web Dashboard]
```

---

## 5. Technology Stack Decisions

| Layer | Technology | Rationale |
|---|---|---|
| **Frontend** | Next.js 14/15 (App Router), TypeScript, Tailwind CSS | High performance, instant rendering, production-ready UI for judges |
| **UI Components** | shadcn/ui + curated `ui-library` components | Consistent design system, zero bloat, accessibility built-in |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2 | Sub-millisecond routing, strict type safety, asynchronous processing |
| **Primary LLM** | Groq API (`llama-3.1-8b-instant`) | Ultra-fast (<1s response), small-model bonus compliant, lean tokens |
| **Fallback LLM** | OpenAI API (`gpt-4o-mini`) / Local Ollama | Resilience against network interruptions or provider rate limits |
| **Constraint Solver** | Deterministic Python (Standard Library) | 100% mathematical accuracy, zero hallucination, zero extra token cost |
| **Tracing** | Custom High-Fidelity Execution Logger | Full audit compliance with competition rules |
