# HackPlan AI — Mind to Machine Hackathon 2026

**HackPlan AI** is an intelligent, neuro-symbolic event operations and planning system designed for hackathon organizers. It parses unstructured, scattered communication (emails, WhatsApp messages, notices in English and Roman Urdu) and transforms them into a deterministic, constraint-validated, and demonstrable event plan.

The platform guarantees **0% mathematical hallucination** by strictly separating responsibilities: language models are used exclusively for unstructured reading and comprehension, while deterministic Python solvers execute all arithmetic, capacity checking, schedule geometry, budget accounting, and constraint validation.

---

## Architecture & Tech Stack

- **Frontend**: Next.js 16 (App Router), React 19, Tailwind CSS v4, TypeScript
- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2, SQLite3
- **AI & Workflow**: Groq Inference (`qwen/qwen3.8-27b`), finite LangGraph orchestration, deterministic fallback parser
- **Messaging Integration**: Custom WhatsApp REST API adapter with live send and safe dry-run preview modes
- **Design System**: High-contrast, custom executive palette (Onyx, Graphite, Ocean Twilight, Digital Blue, Tea Green, Soft Blossom, Sweet Peony)

---

## Core Capabilities

1. **Multi-Source Message Ingestion**:
   - Accepts raw, messy text packs (emails, WhatsApp group chats, broadcast notices, handwritten updates).
   - Extracts structured facts across 5 critical domains: Venue, Schedule, Teams & Judges, Food & Catering, and Budget.
   - Transparently handles multilingual inputs (English + Roman Urdu).

2. **Deterministic Constraint Engines**:
   - **Venue**: Evaluates room capacity, pricing, air conditioning, and power/generator constraints.
   - **Schedule**: Computes timeline geometry, mandatory opening/closing sessions, hack duration, and prayer breaks.
   - **Judging**: Optimizes judge-to-team assignments (capped at 3 teams per judge), ensuring 100% team evaluation coverage.
   - **Food & Catering**: Calculates exact headcount requirements across participants, mentors, and assigned judges, comparing caterer price tiers.
   - **Budget**: Sums all approved expenditures against strict budget caps, itemizing variances and surpluses/deficits.

3. **WhatsApp Notification Hub**:
   - **Dual Dispatch Modes**: Safe dry-run previews (default) and authorized live delivery to real WhatsApp recipients.
   - **Consent-Aware Management**: Organizer-controlled recipient opt-in/opt-out registry.
   - **Validation & Reliability**: International E.164 phone normalization, idempotency key deduplication, rate limiting (max 5/min), and cold-start timeout handling.

4. **Audit Trail & Governance**:
   - Versioned plan snapshots stored in SQLite.
   - Rejection diagnostics explaining conflicting or infeasible updates.
   - Real-time token usage and model execution tracing.
   - Full JSON submission export (`data/submission.json`).

---

## Custom Color Theme

The interface utilizes a purposeful, executive color system designed for clarity and focus:

| Color Name | Hex Code | Visual Identity & Role |
| :--- | :--- | :--- |
| **Onyx** | `#151515` | Jet-black foundation canvas (`--background`) |
| **Graphite** | `#373737` | Balanced dark borders and structural dividers (`--border`) |
| **Ocean Twilight** | `#314cb6` | Velvety twilight blue for primary actions (`.btn-primary`) |
| **Digital Blue** | `#0075f2` | Modern energizing blue for active navigation and links |
| **Deep Purple** | `#6b2d5c` | Rich indigo-violet brand gradient header |
| **Air Force Blue** | `#6494aa` | Composed neutral tone for secondary text and icons (`--muted`) |
| **Tea Green** | `#c5ebc3` | Gentle creamy green for positive status badges & pass checks |
| **Soft Blossom** | `#e8b4bc` | Delicate pink-lavender for warning badges and pending states |
| **Sweet Peony** | `#d282a6` | Rich airy mauve for danger alerts and unresolved conflicts |

---

## How to Run Locally (Frontend & Backend)

### Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18.18 or higher (Node 20+ recommended)
- **PowerShell** (Windows) or **Bash** (macOS/Linux)
- **Git**

---

### Step 1: Clone the Repository & Configure Environment

```bash
git clone https://github.com/AkifNaveed12/Mtm-hackathon.git
cd Mtm-hackathon
```

Copy the example environment configuration:

```bash
cp .env.example .env
```

Ensure your `.env` contains your API credentials:

```env
# LLM Provider
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b

# Backend Configuration
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
ENVIRONMENT=development
PLANNER_MODE=auto

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# WhatsApp REST Bot (Live Integration)
WHATSAPP_API_URL=https://whatapp-bot-xnb0.onrender.com
WHATSAPP_API_KEY=your_whatsapp_api_key_here
WHATSAPP_ALLOW_LIVE_SEND=true
```

---

### Option A: Quick Start (Single Command — Windows PowerShell)

A comprehensive PowerShell startup script is provided that automatically starts both the FastAPI backend and Next.js frontend in the background:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-local.ps1
```

To stop all local services started by the script:

```powershell
powershell -ExecutionPolicy Bypass -File .\stop-local.ps1
```

---

### Option B: Manual Execution (Two Separate Terminals)

If you prefer running services interactively in dedicated terminals:

#### Terminal 1 — Backend (FastAPI)

1. Create and activate a Python virtual environment:

   ```powershell
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install backend dependencies:

   ```bash
   pip install -r backend/requirements.txt
   ```

3. Start the FastAPI development server:

   ```bash
   uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

   The backend will be available at:
   - **API Base**: [http://localhost:8000](http://localhost:8000)
   - **Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)
   - **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Terminal 2 — Frontend (Next.js)

1. Navigate to the `frontend` directory:

   ```bash
   cd frontend
   ```

2. Install npm dependencies:

   ```bash
   npm install
   ```

3. Launch the Next.js development server:

   ```bash
   npm run dev
   ```

   The web dashboard will be available at:
   - **Dashboard**: [http://localhost:3000](http://localhost:3000)

---

## CLI Planning Harness

You can also run the full end-to-end planning pipeline directly via the command-line interface:

```powershell
# Run baseline planning on the official sample pack
python run.py sample_pack.txt

# Run an incremental update
python run.py tests/fixtures/printing_update.txt
```

Outputs the complete quality checks, model traces, cost breakdowns, and saves the final submission artifact to `data/submission.json`.

---

## Testing & Quality Verification

Run the automated test suite across backend logic, constraints, WhatsApp adapter, schemas, and security:

```powershell
# Run all 104 unit & integration tests
pytest tests

# Verify frontend production build & TypeScript
cd frontend
npm run build
```

---

## Repository Branches

- **`main`**: Primary branch containing core documentation, configuration, and project source.
- **`completed`**: Complete feature branch containing all latest tested modules, UI components, scripts, WhatsApp fixes, and test suites.

