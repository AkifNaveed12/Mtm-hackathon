# HackPlan AI - Mind to Machine

Local Next.js event operations dashboard with FastAPI, finite LangGraph orchestration, validated Groq extraction, deterministic planning, SQLite history, and consent-aware WhatsApp previews.

The official source is `theme.pdf`. Decisions and schemas are maintained in the existing `documents/` files. Actual verification and remaining external blockers are in [PROJECT_COMPLETION_REPORT.md](PROJECT_COMPLETION_REPORT.md).

## Start locally in Windows PowerShell

From `D:\mtmm\Mtm-hackathon`, reuse the existing environment:

```powershell
rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -File .\start-local.ps1
```

Open `http://localhost:3000`. The API is `http://localhost:8000/api/health`, with interactive documentation at `http://localhost:8000/docs`. Services bind to loopback. Logs are under ignored `.local-logs/`. The startup script reuses occupied service ports and does not enable live messaging.

Use `-Offline` for a server whose default parser makes no model calls. The dashboard also offers explicit Automatic, Provider required, and Offline modes. Automatic tries Groq once and identifies any fallback; Provider required reports failure instead of claiming an offline result is AI-generated. No retries run invisibly.

For a production frontend build:

```powershell
rtk proxy npm --prefix frontend run build
rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -File .\stop-local.ps1
rtk proxy powershell -NoProfile -ExecutionPolicy Bypass -File .\start-local.ps1 -Production
```

The stop script verifies recorded process identities before stopping only its own services. To restart only the backend, use `stop-local.ps1 -BackendOnly`, followed by `start-local.ps1`.

## Install when needed

Keep the existing `.env`; never paste or commit credentials. `.env.example` documents safe variable names.

```powershell
rtk proxy python -m venv .venv
rtk proxy .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
rtk proxy npm --prefix frontend ci
rtk proxy npm --prefix tests/browser ci
```

`GROQ_API_KEY` and optional `GROQ_MODEL` stay server-side; the tested model is `qwen/qwen3.8-27b`. The existing custom WhatsApp service uses `WHATSAPP_API_URL` and `WHATSAPP_API_KEY`. `WHATSAPP_ALLOW_LIVE_SEND` defaults false. An optional `ORGANIZER_API_KEY` protects local API records and can be entered through Organizer access without putting it in the browser bundle. `WHATSAPP_WEBHOOK_SECRET` is needed only for a signature-capable inbound relay.

## Competition command and updates

```powershell
rtk proxy .\.venv\Scripts\python.exe run.py sample_pack.txt
rtk proxy .\.venv\Scripts\python.exe run.py tests\fixtures\printing_update.txt
rtk proxy .\.venv\Scripts\python.exe run.py tests\fixtures\catering_invalid.txt
```

The same command reads every UTF-8 file without editing its content. A multi-message pack generates a baseline; one message updates persisted state. Six checks, exact model trace, provider token totals, rejections and a plan summary are printed. The full artifact is saved to ignored `data/submission.json`. Use one writer at a time: CLI changes are visible to a running backend after restarting it. Normal dashboard/API use does not require restarts.

## Verification

```powershell
rtk proxy .\.venv\Scripts\python.exe -m pytest tests -q
rtk proxy npm --prefix frontend run lint
rtk proxy npm --prefix frontend run build
rtk proxy npm --prefix tests/browser test
rtk proxy .\.venv\Scripts\python.exe scripts\verify_cli.py
rtk proxy .\.venv\Scripts\python.exe scripts\benchmark.py offline
rtk proxy .\.venv\Scripts\python.exe scripts\security_audit.py
rtk proxy .\.venv\Scripts\python.exe scripts\audit_python_dependencies.py
```

Browser tests require running local services and installed Chrome; override `CHROME_PATH` if necessary. They use offline planning and mocked/previews-only WhatsApp behavior. `benchmark.py provider` intentionally makes at most three actual model calls: a full sample run and the two practice updates. It requires network access and configured Groq credentials. `provider workspace` writes those results into the application's local state; stop the backend first to avoid concurrent writers. No verification script sends live WhatsApp messages.

## Planning and safety

All five engines derive figures from source messages. Source attendance, duration, venue/facility, catering, judging and financial constraints are validated before accepting a version. Unsupported constraints remain unresolved; a previous valid plan is preserved when an update fails. The sample assigns the minimum 17 judges from 20 available, yielding 177 meals; this disclosed staffing decision is overridden by explicit attendance/payment instructions. Team and judge assignment identifiers are generated and labeled, without inventing student identities.

WhatsApp supports read-only connection verification, private recipient/consent records, notification previews, idempotency, rate limits, sanitized failures, signed delivery/inbound events and opt-outs. Real sends require both explicit server enablement and per-request confirmation; they were not authorized or performed. Template catalogs, the upstream send schema, signature-capable webhook relay and actual delivery remain external verification requirements.

All changes remain local. No commits, pushes, deployment, Vapi, voice agent or telephony are part of this task.
