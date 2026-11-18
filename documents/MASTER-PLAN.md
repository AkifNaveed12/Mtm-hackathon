# HackPlan AI — Master Execution Plan & Strategy

## Current execution override

The active user request is local-only completion and verification. Do not commit, push, merge, or deploy. Earlier submission/deployment instructions below do not apply to this session. Model bonus eligibility is unverified until checked against the organizers' list; no score is guaranteed. Actual progress and quality gates are recorded in root `PROJECT_COMPLETION_REPORT.md`.

## 1. High-Level Strategy & Winning Formula

To achieve a winning score at the Mind to Machine Hackathon, HackPlan AI optimizes across all evaluation dimensions:

| Evaluation Dimension | Points Available | HackPlan AI Strategy |
|---|---|---|
| **1. Output Quality** | 30 Points | Passes all 6 verification checks with mathematically validated figures and optimal venue/food decisions. |
| **2. Catching Wrong Messages** | 20 Points | Rejects invalid messages (e.g. food cuts, budget busts) with explicit, logical justifications in the trace. |
| **3. Understanding (Oral Exam)** | 20 Points | Clear, modular neuro-symbolic architecture where every team member can articulate what each module does and *what would break without it*. |
| **4. Handling Change** | 10 Points | Dynamic message ingestion calls *only* the affected area (<= 5 model calls, < 1 min). |
| **5. User Interface (UI)** | 10 Points | High-density, professional Next.js dashboard clearly visualizing plan, trace, and rejected messages. |
| **6. Predicting a Change** | 5 Points | Deterministic domain routing allows 100% accurate prediction slips before running messages. |
| **7. Token Use** | 5 Points | Minimal prompt engineering and deterministic arithmetic makes our full run the leanest in the room. |
| **8. Small-Model Bonus** | 10 Points (Bonus) | Primary pipeline runs on Groq `llama-3.1-8b-instant`, earning the full 10-point small model bonus. |
| **Total Target** | **110 / 100** | Decisive competitive advantage. |

---

## 2. Major Development Milestones

```
[M1: Theme & Architecture Freeze] ---> [M2: Core Engine & CLI Runner] ---> [M3: Constraint & Conflict Arbiter]
                                                                                        |
[M6: Code Freeze & Submission] <--- [M5: End-to-End Integration] <--- [M4: FastAPI & Next.js UI Build]
```

### Milestone 1: Theme Analysis & Architecture Freeze (Current Milestone)
- Faithful extraction of `theme.pdf` using MarkItDown -> `official-theme.md`.
- Complete Product Definition -> `idea.md`.
- Formal Requirements & Traceability -> `REQUIREMENTS.md`.
- Technical & System Architecture -> `ARCHITECTURE.md`.
- API Specification -> `API-CONTRACT.md`.
- Design System & Component Selection -> `DESIGN.md`.
- Master Strategy & Planning -> `MASTER-PLAN.md` & `PLANNING.md`.

### Milestone 2: Core Engine & Single-Command CLI Runner
- Implement `UniversalMessageIngestor` (`reading`).
- Implement the 5 Area Solvers (`venue`, `schedule`, `food`, `judging`, `budget`).
- Implement `GlobalExecutionTracer` with provider token reporting.
- Build `run.py` single command CLI interface for volunteer testing.

### Milestone 3: 6-Point Invariant Solver & Conflict Arbiter
- Implement deterministic 6-point verification gate.
- Implement incremental change handler (`POST /api/message`).
- Implement sabotage detection & conflict rejection logging.
- Verify against practice messages (printing cost change & catering cut).

### Milestone 4: FastAPI Backend & Tracing API
- Package core engine as FastAPI REST services.
- Implement `/api/run`, `/api/message`, `/api/plan`, `/api/trace`, `/api/export`.
- Add local fallback provider and health telemetry.

### Milestone 5: Next.js Frontend Command Dashboard
- Implement 6-check status ribbon.
- Implement 5-area workspace views.
- Implement searchable, expandable execution trace viewer.
- Implement rejected messages audit ledger.
- Implement interactive message injection console.

### Milestone 6: End-to-End Verification, Code Freeze & Rehearsal
- Test run on sample pack and unseen synthetic packs.
- Benchmark full run (< 25s) and update runs (< 5s).
- Verify git status clean, zero untracked secrets, commit hash recorded.
- Conduct oral defense dry run for all team members.

---

## 3. Parallel Development Workstreams

```
+-------------------------------------------------------------+
| Parallel Track A (Backend & AI Specialists)                 |
| - T2.1 to T2.5: Ingestion, Area Solvers, Tracing Engine     |
| - T3.1 to T3.4: Invariant Gate, Conflict Arbiter, CLI       |
+-------------------------------------------------------------+
                               |
                               +---> Joint Integration & Smoke Tests
                               |
+-------------------------------------------------------------+
| Parallel Track B (Frontend Specialist)                      |
| - T4.1 to T4.4: Next.js Scaffolding, Design Tokens, Layout  |
| - T5.1 to T5.4: Plan Cards, Trace Viewer, Rejection Table   |
+-------------------------------------------------------------+
```

---

## 4. Judging & Oral Defense Preparation Strategy

The competition draws one team member by lot to answer two questions:
1. *"What is each part of your system for?"*
2. *"What would break without it?"*

### Prepared Defense Matrix:
- **Part 1: Ingestion & Reading Layer (`reading`)**
  - *Purpose*: Understands unstructured English and Roman Urdu without manual flags or hardcoded text.
  - *What breaks without it*: The system cannot extract facts from WhatsApp or Pakistani colloquial messages.
- **Part 2: Domain-Specific Evaluators (`venue`, `schedule`, `food`, `judging`, `budget`)**
  - *Purpose*: Isolates domain logic so that updates only affect relevant components.
  - *What breaks without it*: Any change would require a complete re-run of the entire system, blowing past the 5-model-call limit.
- **Part 3: Deterministic Arithmetic & Invariant Engine**
  - *Purpose*: Performs all math and rule checking in deterministic Python code.
  - *What breaks without it*: LLMs will hallucinate sums, leading to budget overruns and capacity mismatches.
- **Part 4: Conflict Arbiter & Trace Engine**
  - *Purpose*: Detects invalid/sabotage messages, preserves the valid plan, and records the exact rejection reason.
  - *What breaks without it*: Bad messages (like catering cuts) would corrupt the operational plan.
