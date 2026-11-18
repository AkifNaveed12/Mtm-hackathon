# Local QA verification report

Verified on 18 November 2026 in the existing Windows workspace. Changes stayed local. No commits, pushes, deployments, voice integrations, or real WhatsApp sends were performed by QA.

## Executed results

| Verification | Result | Evidence |
|---|---|---|
| Backend, API, schemas, deterministic planning, state, tracing, security, and mocked integration tests | **104 passed, 0 failed, 0 skipped** | `.venv\Scripts\python.exe -m pytest tests -q` (2.33 seconds in the final run) |
| Headless Chrome browser journeys against the running local frontend and backend | **12 passed, 0 failed** | `artifacts/browser/browser-report.json` |
| Browser JavaScript/console errors during the complete final journey | **0** | Browser report |
| Unexpected failed HTTP responses during the complete final journey | **0** | Browser report |
| Production frontend dependency advisory audit | **0 reported vulnerabilities** | `npm audit --omit=dev --json` executed successfully |
| Official PDF extraction and comparison | **Verified** | `artifacts/official-theme-extracted.txt` |

The browser used installed Google Chrome in headless mode through `playwright-core`. The Python Playwright download was canceled because it was unnecessarily large and slow; the completed Node browser suite is the executed evidence. All screenshots and exports are generated local artifacts.

## Verified user journeys

The browser suite exercised actual frontend requests and local SQLite-backed APIs, without replacing planning results with mocked UI data:

1. Rendered styling, sidebar dimensions, dashboard, dark colors, and empty-state behavior.
2. TXT upload, preservation of original CRLF file contents in the submitted request, processing-mode selection, confirmation dialog, and offline generation.
3. All eleven navigation sections on desktop and at a 390-pixel mobile viewport, including table containment and closing mobile navigation.
4. Search of persisted original messages.
5. Exact official Finance printing update: expenditure rises by Rs 5,000, with venue, schedule, food, and judging unchanged.
6. Exact official 100-box catering message: rejected with a reason; the complete prior plan remains unchanged.
7. Saved-version comparison and JSON, human-readable report, and full trace downloads.
8. WhatsApp recipient consent, safe preview creation, opt-out, and removal from the consented selection list. Every notification request had `dry_run: true`.
9. Accessible labels for form controls and names for icon buttons.
10. Simulated backend connection failure and successful recovery after restoring connectivity.

Screenshots of the dashboard, every management section, mobile dashboard, and mobile assignments were captured under `artifacts/browser/`; representative desktop and mobile screenshots were visually reviewed.

## Backend coverage

Tests use a fresh in-memory or temporary SQLite database, disable live AI credentials in the test process, and forbid live WhatsApp sending. No application database or configured credential is deleted or overwritten by pytest.

Covered behavior includes:

- All core and domain API routes, current facts and constraints, messages, history, executions, predictions, and exports.
- Six operational checks, derived teams and meals, unique generated team assignments, judge workload, and exact Decimal-based money calculations.
- A synthetic unseen-style pack with different participants, team size, staff, judges, honoraria, budget, venue options, catering rates, and event length.
- Latest dated quote precedence even when older and newer source blocks are reordered.
- Required generator selection, additional breaks, source-defined opening duration, infeasible breaks, and late-judge availability conflicts.
- Unsupported logical restrictions remain unresolved; a recognized rule in the same message cannot hide an unknown rule.
- Approved constraint statuses and comparison aliases are enforced; unknown effective statuses remain unresolved. Source-validation guards prevent a model from inventing a power requirement or treating a message-header date as the event date.
- Authorized participant changes recompute derived team totals, judge selection, meals, venue capacity, and budget.
- Explicit attendance and payment of every confirmed judge override the generated minimum-judge assumption.
- Valid updates, invalid updates, duplicate expense canonicalization, exact rollback, and persistence across new engine instances.
- Negative/NaN costs, invalid clocks, missing activity names, negative durations, unknown model-output fields, malformed requests, oversized inputs, and filesystem path traversal.
- Optional organizer-key enforcement, untrusted-Origin rejection, safe local CORS, source-authority rejection, and prompt-injection rejection.
- Mocked model SDK boundary: actual returned model identifier, exact request/output trace, reported usage, missing usage, missing total usage, no invented totals, bounded retries, failure recording, and sanitized diagnostics.
- Mocked WhatsApp transport: provider path/authentication, no-network previews, consent, dual live-send gates, idempotency, timeout ambiguity without retry, rate limits, atomic recipient validation, signed webhooks, duplicate events, delivery progression, STOP handling, safe malformed-provider responses, and persistence.

## Official competition requirements

| Official requirement | QA verification |
|---|---|
| Read original message files; no pack facts typed into application logic | File-upload request preserves original text; synthetic pack changes all primary figures; source-backed planners tested |
| One command for initial pack and subsequent messages | Root separately verified the CLI with three subprocesses; see completion report and `scripts/verify_cli.py` |
| Five planning areas and six validity checks | Official sample and synthetic pack pass all six checks |
| Numbered calls, exact model, permitted area tag, complete input/output, provider usage and totals | Trace and mocked-SDK tests pass; exact untruncated terminal trace tested |
| Accept new messages and recalculate affected areas | Printing update preserves four unaffected domain snapshots; participant-change dependency regression passes |
| Reject conflicting messages and preserve the valid plan | Official catering update and budget-overrun rollback tests pass |
| Initial run within 120 seconds; updates within 60 seconds and at most five calls | Deterministic tests pass within limits; real-provider benchmark belongs to the completion report |
| UI clearly shows plan, trace, and rejections | Actual browser journey covers all three and exports |
| Unseen restrictions cannot be silently discarded | Unknown and mixed known/unknown rule tests pass; unsupported restrictions are reported for review |
| Small-model bonus | Not certified: the organizers' approved model list has not been supplied |

The PDF and `documents/official-theme.md` agree in substantive content. Encoding artifacts and layout differ. The PDF says 177 people to feed, while its sample lists 150 students, 10 staff, and 20 confirmed judges. The implemented, disclosed planning interpretation selects the minimum 17 judges needed for 50 teams at three teams per judge; this produces 177 meals. Source requirements for full attendance or payment override that generated decision. Neither standby power nor a particular meal tier is mandated by the PDF.

## Findings fixed during QA

- A per-judge limit of three teams was incorrectly parsed as the total team count.
- The exact printing-bill sentence created a duplicate expense label and added Rs 20,000 instead of Rs 5,000.
- Derived team totals remained stale after a participant-count change.
- Model-output schemas accepted negative/NaN expenses, malformed clocks, and invalid activity records.
- The judge table omitted actual slot/start/end fields supplied by the backend.
- Malformed provider JSON arrays could escape safe WhatsApp error handling.
- Missing provider totals could be synthesized rather than remaining unavailable.

Each fixed behavior has a regression test or was rechecked through the browser. Early browser-run failures caused by CRLF textarea normalization, changing badge accessible names, asynchronous UI refresh, and animation timing were corrected in test synchronization; the final suite passes without weakening application validation.

## Boundaries and remaining verification

The automated AI adapter tests are explicitly mocked. They do not prove real-provider latency or extraction quality. Root's separately bounded real-provider benchmark and its actual trace/token results belong in `PROJECT_COMPLETION_REPORT.md`.

WhatsApp delivery is not verified. No live send was authorized or performed. An externally reachable signed webhook relay, provider event support, and any account-specific template or messaging-window requirements remain external dependencies. The configured custom provider does not advertise a template catalog.

The production dependency audit reported no advisories; that result is not a guarantee that all dependencies or application paths are vulnerability-free. Python dependency-audit findings and remediation are reported by root. This is a local organizer application; remote access requires explicit organizer-key configuration.

## Reproduce

```powershell
Set-Location 'D:\mtmm\Mtm-hackathon'
& .\.venv\Scripts\python.exe -m pytest tests -q

# With the local frontend and backend running:
node .\tests\browser\smoke.mjs

# If browser test dependencies need installation:
npm --prefix .\tests\browser install --ignore-scripts

# Optional Chrome path override:
$env:CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
```

The browser suite creates local sample plan versions, a clearly named test recipient, safe notification previews, and opt-out records. Run the final real-provider benchmark after the browser suite if the dashboard should finish with a real-provider trace.
