export type JsonRecord = Record<string, unknown>;

export interface Plan {
  status: string;
  last_updated: string;
  event?: {
    name?: string;
    date?: string | null;
    location?: string | null;
    students?: number;
    staff?: number;
    team_size?: number;
    required_headcount?: number;
  };
  venue: {
    selected_room: string;
    capacity: number;
    cost: number;
    generator_standby: boolean;
    rationale: string;
    options?: JsonRecord[];
    facilities?: string[];
  };
  schedule: {
    total_duration_hours: number;
    prayer_break_minutes: number;
    timeline: { time_slot: string; activity: string; duration_mins: number }[];
    conflicts?: string[];
  };
  food: {
    caterer_tier: string;
    unit_cost: number;
    headcount: number;
    total_cost: number;
    delivery_terms: string;
    delivery_cost?: number;
    options?: JsonRecord[];
    attendee_categories?: Record<string, number>;
  };
  judging: {
    confirmed_judges: number;
    selected_judges?: number;
    honorarium_per_judge: number;
    total_honoraria: number;
    teams_count: number;
    teams_per_judge: number;
    minutes_per_team: number;
    duration_minutes: number;
    assignments?: JsonRecord[];
    unassigned_teams?: string[];
    conflicts?: string[];
    availability?: JsonRecord[];
    max_teams_per_judge?: number;
  };
  budget: {
    cap: number;
    total_committed: number;
    total_variable: number;
    total_projected: number;
    surplus_deficit: number;
    line_items: {
      category: string;
      item: string;
      amount: number;
      status: string;
    }[];
  };
  raw_messages_count: number;
  constraints?: JsonRecord[];
  unresolved_constraints?: (string | JsonRecord)[];
}

export interface Checks {
  figures_valid: boolean;
  budget_valid: boolean;
  venue_fits: boolean;
  schedule_valid: boolean;
  enough_judges: boolean;
  all_areas_covered: boolean;
  all_passed: boolean;
  details: JsonRecord;
}

export interface TraceEntry {
  call_number: number;
  model_name: string;
  area_tag: string;
  input: string;
  output: string;
  prompt_tokens: number | null;
  completion_tokens: number | null;
  total_tokens: number | null;
  duration_seconds?: number;
  duration_ms?: number;
  status?: string;
  error?: string | null;
  retry?: number;
}
export interface TraceLog {
  entries: TraceEntry[];
  total_calls: number;
  total_prompt_tokens: number | null;
  total_completion_tokens: number | null;
  overall_total_tokens: number | null;
  events?: JsonRecord[];
  usage_complete?: boolean;
}
export interface Rejection {
  message_index?: number;
  sender: string;
  raw_text: string;
  target_area: string;
  attempted_action: string;
  rejection_reason: string;
  timestamp: string;
  source_reference?: string;
}
export interface PlanResponse {
  plan: Plan | null;
  checks: Checks | null;
}
export interface RunResponse extends PlanResponse {
  accepted?: boolean;
  rejection_reason?: string | null;
  affected_areas?: string[];
  execution_time_seconds?: number;
  status?: string;
  trace?: TraceLog;
}
export interface Recipient {
  id: number | string;
  name: string;
  phone: string;
  opted_in: boolean;
  created_at?: string;
}
export interface WhatsAppStatus {
  provider: string;
  configured: boolean;
  connected: boolean;
  connection_state: string;
  verified_at?: string | null;
  live_sending_enabled: boolean;
  missing_variables: string[];
  blockers: string[];
  features?: JsonRecord;
}

const API_ORIGIN = (
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
).replace(/\/$/, "");
let organizerKey = "";
export function setOrganizerKey(value: string) {
  organizerKey = value;
}

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (init.body && !(init.body instanceof FormData))
    headers.set("Content-Type", "application/json");
  if (organizerKey) headers.set("X-Organizer-Key", organizerKey);
  const timeout = AbortSignal.timeout(path === "/run" ? 125_000 : 65_000);
  let response: Response;
  try {
    response = await fetch(`${API_ORIGIN}/api${path}`, {
      ...init,
      headers,
      signal: init.signal ?? timeout,
      cache: "no-store",
    });
  } catch (error) {
    if (
      error instanceof Error &&
      (error.name === "TimeoutError" || error.name === "AbortError")
    )
      throw new Error(
        "The request timed out. Check the execution trace before retrying.",
      );
    throw new Error(
      "Cannot reach the backend. Start the local API on port 8000, then retry.",
    );
  }
  if (!response.ok) {
    const body: unknown = await response.json().catch(() => null);
    const detail =
      body && typeof body === "object" && "detail" in body
        ? (body as { detail: unknown }).detail
        : null;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail
              .map((item: { msg?: string }) => item.msg || "Invalid input")
              .join("; ")
          : `Request failed (${response.status}).`;
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export async function downloadExport(format: "json" | "markdown" | "trace") {
  const response = await fetch(`${API_ORIGIN}/api/export/${format}`, {
    headers: organizerKey ? { "X-Organizer-Key": organizerKey } : {},
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok)
    throw new Error(
      "Export failed. Generate a plan and check organizer access.",
    );
  const url = URL.createObjectURL(await response.blob());
  const link = document.createElement("a");
  link.href = url;
  link.download = `hackplan-${format}.${format === "markdown" ? "md" : "json"}`;
  link.click();
  URL.revokeObjectURL(url);
}

export const display = (value: unknown): string =>
  value == null
    ? "Not specified"
    : typeof value === "object"
      ? JSON.stringify(value)
      : String(value);
export const money = (value: number | null | undefined): string =>
  value == null
    ? "—"
    : `Rs ${Number(value).toLocaleString("en-PK", { maximumFractionDigits: 2 })}`;
export const number = (value: number | null | undefined): string =>
  value == null ? "—" : Number(value).toLocaleString("en-PK");
export const time = (value: unknown): string => {
  if (typeof value !== "string" || !value) return "Not recorded";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
};
