# HackPlan AI — API Contract Specification

## 1. Overview

The HackPlan AI backend provides a high-speed RESTful interface enabling both the single-command CLI runner (`run.py`) and the interactive Next.js web application to execute plan generations, submit incremental messages, inspect execution traces, and audit rejected messages.

Base URL: `http://localhost:8000/api`

---

## 2. Endpoints Summary

| Method | Endpoint | Purpose | Consumer |
|---|---|---|---|
| `POST` | `/api/run` | Ingests full message pack file or raw text; generates baseline plan and trace | CLI, Frontend |
| `POST` | `/api/message` | Ingests a single incremental message; updates plan or rejects with reason | CLI, Frontend |
| `GET` | `/api/plan` | Returns the current active operational plan and 6-check status | Frontend |
| `GET` | `/api/trace` | Returns the complete chronological trace log and token summary | Frontend, Volunteer |
| `GET` | `/api/rejected` | Returns all rejected messages with failure diagnostics | Frontend, Volunteer |
| `GET` | `/api/export` | Downloads the official plan and trace artifact for competition submission | Frontend, Volunteer |
| `GET` | `/api/health` | Returns backend health, model provider status, and active configuration | System Monitor |

---

## 3. Data Schemas (Pydantic / TypeScript)

### TraceEntry Schema
```typescript
interface TraceEntry {
  call_number: number;
  model_name: string;
  area_tag: "reading" | "venue" | "schedule" | "food" | "judging" | "budget";
  input: string;
  output: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}
```

### CoreChecks Schema
```typescript
interface CoreChecks {
  figures_valid: boolean;
  budget_valid: boolean;
  venue_fits: boolean;
  schedule_valid: boolean;
  enough_judges: boolean;
  all_areas_covered: boolean;
  all_passed: boolean;
  details: {
    figures_note?: string;
    budget_spend: number;
    budget_cap: number;
    venue_capacity: number;
    venue_generator: boolean;
    headcount_required: number;
    schedule_duration_mins: number;
    prayer_break_mins: number;
    judges_confirmed: number;
    teams_per_judge: number;
    areas_present: string[];
  };
}
```

### OperationalPlan Schema
```typescript
interface OperationalPlan {
  status: "VALID" | "MUTATED" | "REJECTED_ROLLBACK";
  last_updated: string;
  venue: {
    selected_room: string;
    capacity: number;
    cost: number;
    generator_standby: boolean;
    rationale: string;
  };
  schedule: {
    total_duration_hours: number;
    prayer_break_minutes: number;
    timeline: Array<{
      time_slot: string;
      activity: string;
      duration_mins: number;
    }>;
  };
  food: {
    caterer_tier: string;
    unit_cost: number;
    headcount: number;
    total_cost: number;
    delivery_terms: string;
  };
  judging: {
    confirmed_judges: number;
    honorarium_per_judge: number;
    total_honoraria: number;
    teams_count: number;
    teams_per_judge: number;
    time_per_team_mins: number;
  };
  budget: {
    approved_cap: number;
    committed_expenses: {
      prizes: number;
      backup_internet: number;
      printing: number;
    };
    variable_expenses: {
      venue: number;
      food: number;
      judging: number;
      discretionary_items: Array<{ name: string; cost: number }>;
    };
    total_spent: number;
    remaining_balance: number;
  };
  checks: CoreChecks;
}
```

---

## 4. Endpoint Specifications

### 4.1 POST `/api/run`
- **Request Body**:
  ```json
  {
    "file_path": "sample_pack.txt",
    "raw_text": null
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "execution_time_seconds": 18.4,
    "plan": { /* OperationalPlan */ },
    "trace": [ /* Array of TraceEntry */ ],
    "total_tokens": 1845,
    "checks": { /* CoreChecks */ }
  }
  ```

### 4.2 POST `/api/message`
- **Request Body**:
  ```json
  {
    "message_text": "Caterer: I have rounded your order down to 100 boxes to keep the cost low.",
    "sender": "Caterer",
    "timestamp": "14 Nov 15:00"
  }
  ```
- **Response (200 OK - Rejected Example)**:
  ```json
  {
    "status": "REJECTED",
    "message_accepted": false,
    "affected_areas": ["food"],
    "model_calls_made": 1,
    "rejection_reason": "Catering order of 100 boxes is below verified headcount of 177. Rule violation: Every participant, staff member, and judge must receive a meal.",
    "active_plan": { /* Unmutated OperationalPlan */ },
    "incremental_trace": [ /* TraceEntry */ ]
  }
  ```

### 4.3 GET `/api/export`
- **Response (200 OK)**:
  - Content-Type: `text/markdown` or `application/json`
  - Returns finalized formatted event plan, 6-check verification table, and complete numbered trace with token summary.
