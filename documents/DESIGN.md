# HackPlan AI — Design System & Visual Specification

## Implementation clarification

All numerical dashboard examples below are illustrative and must be replaced by backend state. Empty workspaces show empty states. Actual provider configuration and execution mode replace any static model/bonus claims. The completed local interface includes message import, five domain views, actual traces, rejections, version comparisons/exports, and consent-aware WhatsApp previews. Generator backup is displayed as a facility and enforced only when source messages require it. Confirmed/available judges and generated assignments are displayed separately. Live WhatsApp sends are disabled by default.

## 1. Visual Identity & Art Direction

- **Design Philosophy**: *Command Terminal / Operational Flight Deck*.
  - Clean, high-density, authoritative, and focused on information hierarchy.
  - Zero frivolous animations, zero distracting glassmorphism, zero generic AI placeholders.
  - Optimized for judges and volunteer auditors who need instant visibility into plan status, 6-check compliance, and execution traces.
- **Theme Modes**: Modern Dark Theme (Default) with High-Contrast Light Mode toggle.
- **Color Palette**:
  - **Background**: Deep Slate (`#0B0F17`)
  - **Surface / Card Background**: Charcoal Slate (`#151D2C`)
  - **Border / Divider**: Subdued Steel (`#232F46`)
  - **Primary Brand / Accent**: Indigo / Cobalt (`#3B82F6` / `#6366F1`)
  - **Success / Passed Check**: Emerald Green (`#10B981`)
  - **Rejected / Warning**: Amber / Coral Red (`#F59E0B` / `#EF4444`)
  - **Text Primary**: Crisp White (`#F8FAFC`)
  - **Text Secondary / Muted**: Steel Gray (`#94A3B8`)

---

## 2. Typography

- **Primary Display & Interface**: `Inter`, `Geist Sans`, or system sans-serif (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`).
  - Clear hierarchy with distinct weights:
    - Display Headings: 24px - 30px, Bold (700)
    - Section Titles: 16px - 20px, Semi-Bold (600)
    - Body Text: 14px, Regular (400)
    - Small Labels: 12px, Medium (500)
- **Monospace / Technical Font**: `JetBrains Mono`, `Fira Code`, or `Courier New`.
  - Used for model call prompts, outputs, token tallies, currency calculations, and timestamps.

---

## 3. UI Component Mapping (From `ui-library/README.md`)

HackPlan AI adapts proven components from the curated `ui-library` catalog:

| Component Category | Catalog Reference | Implementation in HackPlan AI |
|---|---|---|
| **Data Tables** | `dashboards/data-showcase/data-table-shadcn-ui` | Area line-item breakdowns (Budget ledger, Schedule timeline, Catering options) |
| **Data Density Table** | `dashboards/data-showcase/data-table-with-search-shadcn-ui` | Filterable and searchable Execution Trace view |
| **Drawer / Sheet** | `dashboards/drawers/scrollable-content-drawer-shadcn-ui` | Expandable Model Call Inspector (view full prompt/response & token payload) |
| **Metric Indicators** | `reusable/cards/decent-plain-card-shadcn-ui` | 6 Core Checks compliance cards (Pass/Fail status ribbons) |
| **Alert & Badge** | `reusable/buttons/notifications-button-shadcn-ui` | Rejection alerts showing constraint conflict rationale |
| **Simple Navigation** | `navigation/navbars/simple-nav-bar-shadcn-ui` | Top control bar with Run trigger, Model selector, and Export CTA |

---

## 4. Screen Architecture & Layout

### Screen 1: Top Operational Bar (Header)
- HackPlan AI logo & status badge (*"Live Operations Engine - Mind to Machine 2026"*).
- Model Access Indicator (*"Groq Llama-3.1-8B-Instant - Small Model Bonus Active"*).
- Run Stopwatch (*"Full Run: 18.2s | Tokens: 1,845"*).
- Action Controls: Run Sample Pack, Inject Message, Export Official Artifact.

### Screen 2: 6 Core Quality Checks (Hero Banner)
- A prominent 6-card status ribbon displaying real-time pass/fail status:
  1. **Figures Valid**: All arithmetic and rates verified.
  2. **Within Budget**: Spent Rs 596,000 / Rs 650,000 cap.
  3. **Venue Fits**: Hall B (200 seats >= 180 required) + Generator.
  4. **Schedule Valid**: Exactly 240 mins + 15m prayer break.
  5. **Enough Judges**: 20 judges (2.5 teams/judge <= 3.0 cap).
  6. **All Areas Covered**: Venue, Schedule, Food, Judging, Budget.

### Screen 3: The 5-Area Command Center (Tabbed / Grid Workspace)
- **Venue Area**: Card showing room options matrix, capacity math, power generator justification.
- **Schedule Area**: Interactive timeline with prayer break and concurrent judging blocks.
- **Food Area**: Meal tiers, per-head calculation (180 x Rs 1,200), delivery guarantee.
- **Judging Area**: Judge list, team assignments (50 teams across 20 judges), honorarium ledger.
- **Budget Area**: Visual progress bar against Rs 650,000 cap with committed vs variable spend.

### Screen 4: Live Execution Trace & Token Ledger (Scored Requirement)
- Numbered list of every model call:
  - Header: Call #, Model Name, Area Tag (`reading`, `venue`, `schedule`, etc.), Token count badge.
  - Expandable drawer: Full model input and model output.
  - Bottom summary: Total prompt tokens, completion tokens, and overall total tokens.

### Screen 5: Rejected Messages & Conflict Log (20 Points Scored)
- Dedicated card table recording all rejected messages:
  - Message Text & Sender.
  - Attempted Mutation.
  - Broken Rule & Logical Justification.
  - Confirmation that active plan was preserved.

### Screen 6: Interactive Message Injector (Testing Console)
- Textarea to paste new messages live during judging.
- "Dispatch Update" button.
- Prediction slip assistant displaying anticipated model calls prior to execution.
