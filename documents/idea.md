# HackPlan AI — Complete Product Definition

## 1. Product Identity

- **Project Name**: HackPlan AI (Mind to Machine Hackathon Operations Engine)
- **Concept**: A high-efficiency, neuro-symbolic agentic planning and decision-support platform that transforms unstructured, multiformat, multilingual communication packs into an optimal, mathematically verified, constraint-abiding 4-hour hackathon operations plan.
- **One-Line Description**: Autonomous event planning engine combining LLM reading comprehension with deterministic constraint solvers to generate, audit, trace, and dynamically adapt hackathon plans under strict budget, venue, food, schedule, and judging constraints.
- **The Core Problem**: Event planners and hackathon leads receive noisy, conflicting, and fragmented messages (emails, WhatsApp chats, verbal quotes, Roman Urdu notices) from vendors, venues, deans, and coordinators. Manual synthesis leads to arithmetic errors, capacity violations, budget overruns, and overlooked constraints.
- **Target Users**:
  1. *Hackathon Organizing Committee*: Needs an instant, conflict-free, end-to-end plan covering venue, schedule, food, judging, and budget.
  2. *Volunteer Auditors & Judges*: Need a verifiable, transparent trace of every model call, token audit, and clear explanations for why invalid changes are rejected.
- **Value Proposition**:
  - **100% Deterministic Compliance**: Eliminates LLM arithmetic hallucination by delegating mathematical operations, capacity matching, and schedule geometry to deterministic verification code.
  - **Minimal Token Footprint**: Adheres to the principle: *"Use a model where language needs reading, and plain code where arithmetic will do"*, qualifying for maximum token-efficiency and small-model bonus scoring.
  - **Selective Incremental Adaptation**: When new messages arrive, HackPlan AI routes updates exclusively to the affected domain, avoiding redundant model calls (strictly <= 5 model calls, completing in under 1 minute).
  - **Rock-Solid Conflict Rejection**: Detects invalid or sabotage messages (e.g. caterer under-delivering meals), rejects them with precise logical justifications, and maintains the integrity of the verified plan.

---

## 2. Product Modules & System Capabilities

HackPlan AI comprises seven integrated functional modules:

### Module 1: Universal Message Ingestion & Reading (`reading`)
- **Purpose**: Reads raw message packs from text files or interactive feeds without manual intervention, flags, or hardcoded assumptions.
- **Capabilities**:
  - Accepts unstructured formats (emails, WhatsApp transcripts, administrative memos).
  - Handles multiformat and multilingual phrasing, specifically English and Roman Urdu (e.g., *"Salam bhai! Standard lunch box ab Rs 1,200 per head hoga..."*).
  - Extracts raw message metadata (Sender, Date/Timestamp, Medium, Text).
  - De-duplicates and resolves temporal ordering (e.g., superseding an older caterer quote from 20 Oct with an updated quote from 12 Nov).
  - Emits normalized structured facts tagged with domain routing keys.

### Module 2: Venue Planning Area (`venue`)
- **Purpose**: Evaluates venue options against total headcount requirements, electrical reliability, and budget allowances.
- **Capabilities**:
  - Calculates total event capacity requirements: 150 students (50 teams of 3) + 10 staff + 20 judges + organizers/volunteers = 177 to 180+ people.
  - Analyzes room options from quotes (e.g., Margalla Event Halls: Room D [80 seats @ Rs 40k], Hall A [200 seats @ Rs 120k], Hall B [200 seats @ Rs 150k + generator], Hall C [300 seats @ Rs 220k + generator]).
  - Evaluates operational resilience: In Islamabad, power reliability is critical; selects Hall B (200 seats with standby generator at Rs 150,000) as the optimal robust choice.

### Module 3: Schedule & Timeline Planning Area (`schedule`)
- **Purpose**: Synthesizes a friction-free 4-hour (240-minute) physical hackathon agenda respecting institutional mandates.
- **Capabilities**:
  - Incorporates mandatory 15-minute prayer break (mandated by Dean's Office).
  - Sequences opening orientation, build sprint, judging window, lunch/refreshments, and closing ceremony.
  - Coordinates judging phase geometry: 50 teams, 15 min per team, <= 3 teams per judge -> requires 45 minutes of concurrent judging across parallel judge tracks.
  - Ingests peripheral notifications (e.g. judge running 10 minutes late due to Srinagar Highway traffic) and assesses timeline impact deterministically.

### Module 4: Food & Catering Management (`food`)
- **Purpose**: Manages participant and staff nutrition within financial and dietary boundaries.
- **Capabilities**:
  - Reconciles conflicting or historical caterer quotes (Oct 20 vs Nov 12).
  - Accurately tracks headcount: 177-180 people.
  - Compares meal tiers (Standard @ Rs 1,200 vs Basic @ Rs 800 with free delivery).
  - Calculates total catering expense (180 x 1,200 = Rs 216,000 or 180 x 800 = Rs 144,000).
  - Enforces minimum-quantity constraints: Flags and rejects any attempt to cut food below headcount.

### Module 5: Judging System & Resource Allocation (`judging`)
- **Purpose**: Schedules and assigns judging resources based on team allocations and honorarium constraints.
- **Capabilities**:
  - Validates confirmed judge pool (20 confirmed judges).
  - Computes capacity: 20 judges x max 3 teams/judge = 60 team capacity (comfortably accommodates all 50 teams).
  - Calculates judge honoraria: 20 judges x Rs 5,000 = Rs 100,000.
  - Produces evaluation matrix ensuring each team gets 15 minutes of uninterrupted evaluation.

### Module 6: Budget & Financial Reconciliation (`budget`)
- **Purpose**: Real-time financial ledger auditing all event expenditures against the authorized ceiling.
- **Capabilities**:
  - Authorized cap: Rs 650,000 (Dean's approval).
  - Tracks committed pre-orders: Prizes (Rs 100,000), Backup Internet (Rs 20,000), Printing (Rs 10,000) = Rs 130,000.
  - Sums dynamic line items: Venue + Catering + Judging Honoraria + Committed Expenses.
  - Evaluates discretionary requests (e.g. Student Society DJ quote of Rs 50,000) against remaining surplus.
  - Arithmetic solver runs purely in deterministic code (zero token hallucination).

### Module 7: Incremental Change & Conflict Arbiter (Trace Engine)
- **Purpose**: Processes dynamic changes post-run, rejects invalid messages, and formats the execution trace.
- **Capabilities**:
  - Identifies which specific area is impacted by an incoming message.
  - Fires model calls *only* for affected areas (predictable call routing).
  - Applies 6-point verification gate before adopting any plan mutation:
    1. Correct figures & arithmetic consistency.
    2. Total cost <= authorized budget (Rs 650,000).
    3. Venue capacity >= total headcount (177-180 people).
    4. Schedule duration exactly 4 hours with prayer break and valid judging slots.
    5. Judge count sufficient (<= 3 teams/judge for 50 teams).
    6. All 5 operational areas fully specified.
  - Rejection Protocol: If a message fails any check, the plan remains untouched at the last valid state, and the conflict reason is recorded in the trace.

---

## 3. MVP Definition

### Mandatory MVP (P0 — Non-Negotiable for Hackathon Compliance)
1. **Single Command CLI Execution**: `python run.py <message_pack.txt>` runs the complete pipeline without human intervention.
2. **Text File Ingestion**: Reads the exact message pack text without typing facts or messages into source code.
3. **Trace Generation**:
   - Numbered model calls.
   - Model name reported explicitly.
   - Area tag strictly from: `reading`, `venue`, `schedule`, `food`, `judging`, `budget`.
   - Complete prompt input and generated output.
   - Input, output, and total token counts as reported by model provider.
   - Final summary showing aggregate token consumption.
4. **Post-Run Incremental Updates**: Accepts new single messages and updates the active plan in <= 5 model calls, completing in < 1 minute.
5. **Conflict & Sabotage Detection**: Rejects rule-breaking messages, preserves valid plan state, and outputs explicit rejection rationale in the trace.
6. **Six Core Quality Checks**: Plan passes all 6 verification checks (correct figures, within budget, venue fits, schedule valid, enough judges, all areas covered).
7. **Comprehensive User Interface**: A modern, responsive web dashboard (Next.js + FastAPI) presenting the complete plan, live trace, rejected messages log, interactive what-if message injector, and export functionality.

### Supporting Features (P1 — Demonstration & Scoring Multipliers)
- **Small-Model Bonus Optimization**: Engineered and tested using fast, lean models (such as `llama-3.1-8b-instant` on Groq or local Ollama) to qualify for the 10-point bonus.
- **Interactive Message Injector**: Allows judges and volunteers to paste new messages live into the UI and watch the trace and plan update in real-time.
- **One-Click Volunteer Export**: Instantly exports the finalized plan and complete execution trace to clean Markdown/JSON files for contest submission.
- **Detailed Area Inspector**: Interactive drill-down into each of the 5 areas showing formula breakdowns and constraint margins.

### Optional Enhancements (P2 — Post-Competition Scope)
- Multi-day schedule simulation.
- PDF export with stylized corporate branding.
- Vendor negotiation auto-drafting.

---

## 4. AI/ML Engineering & Model Governance

### Architecture Strategy: Minimal-Token Neuro-Symbolic Agents
- **Token Economy Principle**: LLMs are leveraged solely for unstructured language interpretation (multilingual nuance, Roman Urdu idioms, intent parsing). All calculations (addition, capacity inequality, timetable arithmetic) are performed by deterministic Python functions.
- **Model Selection**:
  - Primary Provider: **Groq API** with `llama-3.1-8b-instant` (sub-second latency, ultralow token footprint, qualifies for the Small-Model Bonus).
  - Alternative / Fallback Provider: **OpenAI API** (`gpt-4o-mini`) or **Local Ollama** (`llama3.2:3b` / `mistral`).
- **Standardized Area Tags**: Every model invocation strictly carries one tag:
  - `reading`: parsing incoming raw messages into structured event signals.
  - `venue`: resolving venue trade-offs and generator requirements.
  - `schedule`: sequencing agenda items and prayer break constraints.
  - `food`: resolving catering package and dietary logistics.
  - `judging`: assigning judge tracks and team evaluation capacity.
  - `budget`: evaluating complex discretionary expense allocation.

### Token Audit & Error Resilience
- Token usage is extracted directly from API response metadata (`usage.prompt_tokens`, `usage.completion_tokens`, `usage.total_tokens`).
- System implements fallback parsing in the event of provider rate-limits or transient network dropouts.
- Full run completes in ~15-25 seconds, well within the 2-minute cutoff. Incremental updates complete in ~2-4 seconds, well within the 1-minute cutoff.

---

## 5. User Workflows & Experience

### Workflow 1: Contest Test Run (Volunteer / Official Judging Flow)
1. Volunteer verifies clean git working tree and matching commit hash.
2. User executes the single command: `python run.py sample_pack.txt` (or opens Web Dashboard).
3. System ingests messages, performs reading extraction, executes area solvers, audits 6 checks, and outputs formatted trace to stdout and UI.
4. Volunteer issues incremental change message -> system ingests via command, updates affected area only, records trace.
5. Volunteer issues sabotage message -> system detects constraint violation, rejects change, preserves valid plan, documents reason in trace.
6. User clicks 'Export Plan & Trace' to produce the official submission artifact.

### Workflow 2: Oral Examination Preparation
- The system provides a transparent breakdown explaining what each module does and *what would break without it*:
  - *Without Reading Layer*: System cannot understand Roman Urdu or unstructured WhatsApp texts.
  - *Without Deterministic Arithmetic Solver*: LLM will hallucinate addition and exceed budget or miscalculate headcount.
  - *Without Selective Area Router*: Every new message would trigger full re-runs, wasting tokens and exceeding the 5-call update limit.
  - *Without Conflict Arbiter*: Invalid messages (like catering cuts) would corrupt the operational plan.

---

## 6. Scope Boundaries & Risk Management

- **Scope Limits**: The system focuses strictly on planning the 4-hour, 150-student, 50-team hackathon in Islamabad.
- **Key Risks & Mitigations**:
  - *Risk*: Groq or OpenAI API timeout during live evaluation.
    *Mitigation*: Deterministic mock/fallback mode and local Ollama support.
  - *Risk*: Roman Urdu idioms misclassified by standard prompts.
    *Mitigation*: Few-shot multilingual extraction prompt in the `reading` agent.
  - *Risk*: Over-calling models on incremental updates.
    *Mitigation*: Strict domain-diff filter; only areas whose inputs changed trigger LLM calls (maximum 1-2 calls per update).
