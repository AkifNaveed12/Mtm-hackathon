# HackPlan AI API contract

The existing FastAPI service runs locally at `http://localhost:8000`. The frontend runs at `http://localhost:3000`. All application endpoints use `/api`. This contract describes the implemented local completion, superseding the earlier sample-specific schemas.

## Access and safety

Bind services to loopback. Without `ORGANIZER_API_KEY`, private APIs accept loopback clients only. If the key is configured, send it in `X-Organizer-Key`; the dashboard accepts it through Organizer access and keeps it in memory. Health is public. The signed WhatsApp webhook has its own HMAC authentication. Allowed browser origins are exactly `http://localhost:3000` and `http://127.0.0.1:3000`. Host validation, upload limits, write rate limits, and non-caching responses are enabled.

Errors use `{"detail":"Human-readable reason"}`; Pydantic input errors use FastAPI's validation array. Typical statuses are 400 invalid operation, 401 missing organizer key/invalid signature, 403 unauthorized origin/client/live send, 404 missing version/recipient, 409 consent/idempotency conflict, 413 size limit, 422 schema validation, 429 rate limit, and 503 unavailable provider. Errors never include credentials or raw provider exceptions.

## Planning endpoints

| Method | Path | Request/result |
|---|---|---|
| GET | `/api/health` | Health, version, provider configuration boolean, actual configured model identifier, default mode, organizer-key requirement, storage/workflow names; no credentials |
| POST | `/api/run` | `{raw_text?:string,file_path?:"sample_pack.txt",mode?:"auto"\|"offline"\|"provider"}`; defaults to bundled sample. Arbitrary file paths are forbidden. |
| POST | `/api/message` | `{message:string,sender?:string,mode?:...}`; `message_text` is accepted as an alias. Requires an initial plan. |
| GET | `/api/plan` | `{plan:OperationalPlan,checks:CoreChecks}` |
| GET | `/api/overview` | Plan/checks plus execution, workflow_status, message_count, rejected_count, recent_messages |
| GET | `/api/messages` | Original message array: index, sender, date, source, text, exact raw block, status |
| GET | `/api/facts` | Validated facts, source references, source quote options and assumptions; excludes duplicate raw pack/messages |
| GET | `/api/constraints` | Effective structured constraints array |
| GET | `/api/venue`, `/api/schedule`, `/api/food`, `/api/judging`, `/api/budget` | Corresponding current plan domain |
| GET | `/api/trace` | TraceLog, including exact actual model calls and deterministic workflow/rejection events |
| GET | `/api/rejected` | Rejected messages with original content, sender, source_reference, target_area, rejection_reason, violated_constraints, timestamp |
| GET | `/api/history` | Newest-first `{version,timestamp,summary,affected_areas}[]`, up to 200 versions |
| GET | `/api/history/{version}` | Persisted snapshot for a version, or 404 |
| GET | `/api/executions` | Recent execution records, up to 100 |
| GET | `/api/predict?message=...` | Predicted affected_areas and maximum_model_calls; no model invocation |
| GET | `/api/export`, `/api/export/json` | Downloadable JSON snapshot, current plan/checks/facts/messages/trace/rejections/history |
| GET | `/api/export/markdown` | Human-readable report including all five domains, assumptions, checks, trace and rejection history |
| GET | `/api/export/trace` | Complete downloadable TraceLog JSON |

`POST /api/run` returns `{status,plan,checks,trace,rejected_messages,execution}`. `status` is `success` or `invalid`, including when an invalid candidate was discarded and a previous valid plan was preserved. `POST /api/message` returns `{accepted,rejection_reason,plan,checks,trace,rejected_messages,execution}`. An incompatible message returns HTTP 200 with `accepted:false`; it is an expected workflow outcome. Invalid updates create rejection/execution records but do not create an accepted plan version or overwrite the valid plan.

The pack limit is 200 KB and the update limit is 20 KB (UTF-8). The API request envelope has a 250 KB limit. `offline` uses a disclosed deterministic parser and zero model calls; unfamiliar constraints require review. `provider` requires a successful actual model response and validated extraction; it does not disguise failures as AI success. `auto` attempts the configured provider once, then explicitly reports offline fallback if required. No uncontrolled retries occur.

## OperationalPlan and domain records

The current Python schemas are `backend/app/schemas/plan.py`, `facts.py`, and `checks.py`; the frontend shares their public shapes through `frontend/lib/api.ts`.

- Plan fields: `status` (`EMPTY`, `VALID`, `INVALID`, `MUTATED`, `REJECTED_ROLLBACK`), `last_updated`, `version`, `event`, `venue`, `schedule`, `food`, `judging`, `budget`, `raw_messages_count`, `constraints`, `unresolved_constraints`, `affected_areas`, `extraction_mode`.
- Event: name/date/location when supplied, students/staff/team_size/required_headcount, disclosed judge attendance policy. Missing date/location remain unknown.
- Venue: selected_room, capacity, cost, generator_standby, rationale, required_seating, facilities, source options, valid, issues.
- Schedule: total_duration_hours, prayer_break_minutes, timeline (`time_slot`, `activity`, `duration_mins`, `start_minute`, `end_minute`, `source`), valid, conflicts. Generated allocation is labeled; source time requirements take precedence.
- Food: caterer_tier, unit_cost, headcount, total_cost, delivery_terms, delivery_cost, attendee_categories, source options, valid, issues.
- Judging: confirmed_judges (available pool), selected_judges (assigned attendance), honorarium_per_judge, total_honoraria, teams_count, teams_per_judge, minutes_per_team, max_teams_per_judge, duration_minutes, generated assignments, unassigned_teams, conflicts, availability, identifiers_generated, valid. No source student names are invented.
- Budget: cap, total_committed, total_variable, total_projected, surplus_deficit, line_items (`category`, `item`, `amount`, `status`), warnings, valid. Money uses Decimal arithmetic internally and numeric rupee fields in JSON.
- CoreChecks: figures_valid, budget_valid, venue_fits, schedule_valid, enough_judges, all_areas_covered, all_passed, details.
- Constraint: identifier, source_message, area, constraint_type, operator, value, unit, scope, conditions, authority, effective_status. Unsupported rules remain unresolved.

The sample's minimum workload-feasible staffing selects 17 judges from 20 available, producing 177 meals. This is a disclosed generated decision; explicit attendance and payment-for-all rules override it. A generator is mandatory only if the input requires one.

## Trace accounting

TraceLog: `{entries,total_calls,total_prompt_tokens,total_completion_tokens,overall_total_tokens,usage_complete,events}`.

Each entry records `call_number`, exact returned `model_name`, permitted `area_tag` (`reading`, `venue`, `schedule`, `food`, `judging`, `budget`), exact serialized `input` including messages and generation parameters, exact `output`, provider-reported `prompt_tokens`, `completion_tokens`, `total_tokens`, duration_ms, status, error, retry, timestamp. Unknown token counts are null. Aggregate totals include only reported usage and set usage_complete=false when incomplete. Offline processing never creates fabricated model entries. Full-run reading uses one call; updates use one predicted area call and deterministic dependent recalculation. Extraction failures remain distinguishable from successful provider transport in workflow events.

## WhatsApp endpoints

The configured provider is an existing custom REST bot, verified through authenticated `GET /api/whatsapp/status` upstream using an `x-api-key` server-side header. Configuration is never returned to the browser.

| Method | Local path | Request/result |
|---|---|---|
| GET | `/api/whatsapp/status` | provider, configured, connection_state, connected, verified_at, live_sending_enabled, missing_variables, last_error, features, blockers; no QR/account/secret data |
| POST | `/api/whatsapp/status/verify` | Read-only authenticated upstream connectivity check; sanitized whitelist result |
| GET/POST | `/api/whatsapp/recipients` | List/upsert `{name,phone,opted_in}`; phone must be international E.164-style `+` plus 8-15 digits. Stored result adds id/timestamps. |
| PATCH | `/api/whatsapp/recipients/{id}` | `{opted_in:boolean}` |
| GET | `/api/whatsapp/messages` | Private notification log, latest 500; statuses preview/dispatching/submitted/sent/delivered/read/failed/unknown |
| GET | `/api/whatsapp/templates` | `{templates:[],supported:false,reason}`; upstream does not advertise templates |
| POST | `/api/whatsapp/notifications` | See below |
| GET | `/api/whatsapp/webhooks` | Private verified webhook history, latest 500 |
| POST | `/api/whatsapp/webhook` | Signed inbound/delivery event; raw body max 64 KiB |

Notification request: `{recipient_ids:number[],kind:"event"|"schedule"|"venue"|"judging"|"team"|"reminder",message:string,idempotency_key:string,dry_run?:true,confirm_live_send?:false}`. Response: `{dry_run,notifications:[]}`. Select 1-20 distinct opted-in recipients; body is 1-4000 characters. Live sends are blocked unless `WHATSAPP_ALLOW_LIVE_SEND=true` AND the request confirms explicitly; maximum five live recipients and five notifications/minute. Previews never contact the provider. Upstream submit uses `{to,message}`; this request schema is mocked and remains unverified by a live send. Submission is not labeled delivery. Timeouts are unknown and never retried automatically. Reusing a key with different content is a conflict.

Webhook authentication: `X-WhatsApp-Signature: sha256=<HMAC-SHA256 exact raw body>` using `WHATSAPP_WEBHOOK_SECRET` (`X-Hub-Signature-256` accepted as an alternative). JSON fields: unique event_id, message_id, direction inbound/outbound, status, from/to, message/text. Supported status values: received/sent/delivered/read/failed/unknown. Duplicate events are ignored; delivery status does not regress. Inbound STOP/UNSUBSCRIBE/OPT OUT/CANCEL records opt-out. A public signature-capable relay is an external requirement; no relay is deployed by this local task.

## Persistence and execution

Planning state is in the local SQLite store, with atomic snapshots, plan versions, original messages, and execution records. Facts, constraints, assignments, budgets, and traces persist in validated version snapshots. WhatsApp uses its own local SQLite file for recipients, notification reservations, consent, and verified webhook events. Both files and generated artifacts are ignored by Git. Start instructions and actual verification evidence are in root `PROJECT_COMPLETION_REPORT.md`.
