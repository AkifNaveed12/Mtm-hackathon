# HackPlan AI — Implementation Planning & Task Breakdown

## 1. Overview & Execution Rules

This planning document decomposes the approved product definition (`idea.md`) and technical architecture (`ARCHITECTURE.md`) into executable, verifiable tasks.

- **Execution Cadence**: 6 sequential phases.
- **Agent Ownership**: Explicitly mapped to specialist agents.
- **Rule of Operation**: P0 tasks take precedence over P1 tasks. No task is marked complete without concrete verification evidence.

---

## 2. Phase Breakdown & Task Matrix

### Phase 1: Environment, Scaffolding & Shared Contracts
- **Phase ID**: `PHASE-1`
- **Objective**: Establish unified workspace, dependencies, environment configs, and data schemas.
- **Exit Criteria**: Clean builds, dependencies installed, schemas verified.

| Task ID | Task Description | Agent | Dependencies | Files Affected | Output / Deliverable | Priority |
|---|---|---|---|---|---|---|
| **T1.1** | Initialize backend dependencies & requirements | Backend | None | `backend/requirements.txt` | Python packages installed & verified | P0 |
| **T1.2** | Initialize Next.js frontend scaffolding & Tailwind | Frontend | None | `frontend/package.json` | Next.js app builds with TS & Tailwind | P0 |
| **T1.3** | Define shared Pydantic data schemas | Architect / Backend | None | `backend/app/schemas/` | Typed schemas for Plan, Trace, Checks | P0 |
| **T1.4** | Configure environment & secret templates | Project Lead | None | `.env.example`, `.gitignore` | Safe template with no leaked keys | P0 |

---

### Phase 2: Core Planning Engine & Single-Command CLI
- **Phase ID**: `PHASE-2`
- **Objective**: Build the universal reading layer, area specialists, execution tracer, and `run.py` CLI runner.
- **Exit Criteria**: `python run.py sample_pack.txt` executes in < 30s and outputs a valid plan and numbered trace.

| Task ID | Task Description | Agent | Dependencies | Files Affected | Output / Deliverable | Priority |
|---|---|---|---|---|---|---|
| **T2.1** | Implement Universal Message Ingestor (`reading`) | AI Engineer | T1.1, T1.3 | `backend/app/engine/ingestor.py` | Parses raw text, Roman Urdu & metadata | P0 |
| **T2.2** | Implement 5 Domain Specialists (`venue`, `schedule`, `food`, `judging`, `budget`) | Backend | T1.3 | `backend/app/engine/areas/` | Domain evaluators computing plan areas | P0 |
| **T2.3** | Implement Global Execution Tracer & Token Counter | AI Engineer | T1.3 | `backend/app/engine/tracer.py` | Numbered calls, area tags, token tallies | P0 |
| **T2.4** | Implement Groq / Small-Model Provider Client | AI Engineer | T1.1 | `backend/app/engine/llm.py` | Fast small-model client with fallback | P0 |
| **T2.5** | Implement Single-Command CLI Entrypoint | Integration | T2.1-T2.4 | `run.py` | `python run.py <file>` runs end-to-end | P0 |

---

### Phase 3: Invariant Engine, Incremental Updates & Conflict Arbiter
- **Phase ID**: `PHASE-3`
- **Objective**: Implement 6-point verification gate, selective area routing, and conflict rejection protocol.
- **Exit Criteria**: Catches catering sabotage message, accepts printing change message, passes all 6 checks.

| Task ID | Task Description | Agent | Dependencies | Files Affected | Output / Deliverable | Priority |
|---|---|---|---|---|---|---|
| **T3.1** | Implement 6-Point Invariant Verification Gate | Backend | T2.2 | `backend/app/engine/verifier.py` | Deterministic validation for all 6 checks | P0 |
| **T3.2** | Implement Selective Domain Router for Updates | AI Engineer / Backend | T2.2 | `backend/app/engine/router.py` | Routes updates only to affected area | P0 |
| **T3.3** | Implement Conflict Arbiter & Rejection Logger | Backend | T3.1, T3.2 | `backend/app/engine/arbiter.py` | Rejects invalid messages with reasons | P0 |
| **T3.4** | Validate against Practice Messages (Change + Wrong) | QA/Security | T3.1-T3.3 | `tests/test_incremental.py` | Verified against sample practice messages | P0 |

---

### Phase 4: FastAPI REST Services
- **Phase ID**: `PHASE-4`
- **Objective**: Expose core engine capabilities through clean REST endpoints for UI and automated testing.
- **Exit Criteria**: All REST endpoints respond with correct status codes and schema-validated payloads.

| Task ID | Task Description | Agent | Dependencies | Files Affected | Output / Deliverable | Priority |
|---|---|---|---|---|---|---|
| **T4.1** | Implement `/api/run` and `/api/message` endpoints | Backend | T2.5, T3.3 | `backend/app/api/routes.py` | Execution and update REST endpoints | P0 |
| **T4.2** | Implement `/api/plan`, `/api/trace`, `/api/rejected` | Backend | T4.1 | `backend/app/api/routes.py` | State inspection endpoints | P0 |
| **T4.3** | Implement `/api/export` artifact generator | Backend | T4.2 | `backend/app/api/export.py` | Official submission file download | P1 |
| **T4.4** | Implement `/api/health` and telemetry | Backend | T4.1 | `backend/app/api/health.py` | System health and model diagnostics | P1 |

---

### Phase 5: Next.js Interactive Dashboard UI
- **Phase ID**: `PHASE-5`
- **Objective**: Build an intuitive, high-density web interface presenting plan, trace, rejected messages, and what-if console.
- **Exit Criteria**: Web dashboard renders correctly, connects to backend, and displays live traces.

| Task ID | Task Description | Agent | Dependencies | Files Affected | Output / Deliverable | Priority |
|---|---|---|---|---|---|---|
| **T5.1** | Build 6-Check Compliance Banner Component | Frontend | T1.2 | `frontend/components/ChecksBanner.tsx` | Visual pass/fail status ribbons | P0 |
| **T5.2** | Build 5-Area Overview Cards & Line-Item Tables | Frontend | T1.2 | `frontend/components/AreaCards.tsx` | Venue, Schedule, Food, Judging, Budget | P0 |
| **T5.3** | Build Searchable Execution Trace Viewer | Frontend | T1.2 | `frontend/components/TraceViewer.tsx` | Numbered calls, tags, tokens, drawers | P0 |
| **T5.4** | Build Rejected Messages Audit Ledger | Frontend | T1.2 | `frontend/components/RejectedLog.tsx` | Conflict alerts with exact reasons | P0 |
| **T5.5** | Build Interactive Message Injector & Prediction Aid | Frontend | T5.1-T5.4 | `frontend/components/MessageConsole.tsx`| Live testing console with prediction slip | P1 |

---

### Phase 6: End-to-End Testing, Polish & Competition Freeze
- **Phase ID**: `PHASE-6`
- **Objective**: Comprehensive testing across CLI and UI, timing benchmarks, oral defense dry run, and code freeze.
- **Exit Criteria**: Git working tree clean, commit submitted, full run < 25s, oral exam questions rehearsed.

| Task ID | Task Description | Agent | Dependencies | Files Affected | Output / Deliverable | Priority |
|---|---|---|---|---|---|---|
| **T6.1** | End-to-end regression & benchmark tests | QA/Security | T4.1-T5.5 | `tests/test_e2e.py` | Benchmark logs confirming <2m & <1m | P0 |
| **T6.2** | UI accessibility, responsive & browser audit | QA/Security | T5.1-T5.5 | Frontend build | Browser-verified UI, 0 console errors | P1 |
| **T6.3** | Oral defense question & answer preparation sheet | Project Lead | All | `documents/idea.md` | Team rehearsed on module dependencies | P0 |
| **T6.4** | Final git verification & deployment readiness | Deployment | All | Git repository | Clean tree, pushed commit hash verified | P0 |
