"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type FormEvent,
} from "react";
import dynamic from "next/dynamic";
import { Badge, Empty, Icon, Modal, Panel, Stat, Table } from "@/components/ui";
import {
  api,
  display,
  downloadExport,
  money,
  number,
  setOrganizerKey,
  time,
  type Checks,
  type JsonRecord,
  type Plan,
  type PlanResponse,
  type Recipient,
  type Rejection,
  type RunResponse,
  type TraceLog,
  type WhatsAppStatus,
} from "@/lib/api";

// Retain the existing development annotation tool as an explicit local opt-in.
const Agentation = dynamic(
  () => import("agentation").then((module) => module.Agentation),
  { ssr: false },
);

const navigation = [
  ["dashboard", "Overview"],
  ["messages", "Message center"],
  ["venue", "Venue"],
  ["schedule", "Event schedule"],
  ["judging", "Teams & judges"],
  ["food", "Food & catering"],
  ["budget", "Budget"],
  ["trace", "Agent activity"],
  ["rejected", "Rejected messages"],
  ["history", "History & exports"],
  ["whatsapp", "WhatsApp"],
] as const;
type Section = (typeof navigation)[number][0];
type Toast = { kind: "success" | "error" | "info"; text: string };
const descriptions: Record<Section, string> = {
  dashboard: "Your event, validated across every planning area.",
  messages: "Turn source messages into traceable facts and event decisions.",
  venue: "Compare capacity, cost, and the facilities your event requires.",
  schedule: "A complete timeline with the right time for every activity.",
  judging: "Feasible workloads, clear assignments, and complete team coverage.",
  food: "The right meal quantities, current quotes, and delivery costs.",
  budget: "Every authorized expense, calculated and validated by the backend.",
  trace: "Inspect actual model calls, provider usage, and workflow decisions.",
  rejected:
    "Understand conflicting updates and see why the valid plan was preserved.",
  history:
    "Compare saved plan versions and download your complete audit trail.",
  whatsapp:
    "Manage consent, prepare event notifications, and inspect delivery history.",
};

function asArray(value: unknown): JsonRecord[] {
  if (Array.isArray(value))
    return value.filter(
      (item): item is JsonRecord => !!item && typeof item === "object",
    );
  if (value && typeof value === "object") {
    const record = value as JsonRecord;
    for (const key of [
      "messages",
      "items",
      "entries",
      "versions",
      "notifications",
      "events",
    ])
      if (Array.isArray(record[key])) return asArray(record[key]);
  }
  return [];
}
const field = (record: JsonRecord, ...keys: string[]) =>
  keys.map((key) => record[key]).find((value) => value != null);

export default function Dashboard() {
  const [section, setSection] = useState<Section>("dashboard");
  const [sidebar, setSidebar] = useState(false);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [checks, setChecks] = useState<Checks | null>(null);
  const [trace, setTrace] = useState<TraceLog | null>(null);
  const [rejected, setRejected] = useState<Rejection[]>([]);
  const [messages, setMessages] = useState<JsonRecord[]>([]);
  const [facts, setFacts] = useState<JsonRecord>({});
  const [constraints, setConstraints] = useState<JsonRecord[]>([]);
  const [history, setHistory] = useState<JsonRecord[]>([]);
  const [executions, setExecutions] = useState<JsonRecord[]>([]);
  const [health, setHealth] = useState<JsonRecord>({});
  const [overview, setOverview] = useState<JsonRecord>({});
  const [initialLoading, setInitialLoading] = useState(true);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const [toast, setToast] = useState<Toast | null>(null);
  const [dark, setDark] = useState(true);
  const [showAccess, setShowAccess] = useState(false);
  const [accessKey, setAccessKey] = useState("");
  const [rawPack, setRawPack] = useState("");
  const [packName, setPackName] = useState("");
  const [mode, setMode] = useState("auto");
  const [sender, setSender] = useState("");
  const [newMessage, setNewMessage] = useState("");
  const [prediction, setPrediction] = useState<JsonRecord | null>(null);
  const [search, setSearch] = useState("");
  const [traceArea, setTraceArea] = useState("all");
  const [confirmRun, setConfirmRun] = useState<"sample" | "pack" | null>(null);
  const [selectedVersion, setSelectedVersion] = useState<JsonRecord | null>(
    null,
  );
  const [selectedVersionId, setSelectedVersionId] = useState("");
  const [waStatus, setWaStatus] = useState<WhatsAppStatus | null>(null);
  const [recipients, setRecipients] = useState<Recipient[]>([]);
  const [notifications, setNotifications] = useState<JsonRecord[]>([]);
  const [webhooks, setWebhooks] = useState<JsonRecord[]>([]);
  const [templates, setTemplates] = useState<JsonRecord>({});
  const [recipientName, setRecipientName] = useState("");
  const [recipientPhone, setRecipientPhone] = useState("");
  const [consent, setConsent] = useState(false);
  const [notificationKind, setNotificationKind] = useState("event");
  const [notificationText, setNotificationText] = useState("");
  const [selectedRecipients, setSelectedRecipients] = useState<string[]>([]);
  const [liveSendConfirm, setLiveSendConfirm] = useState(false);
  const uploadRef = useRef<HTMLInputElement>(null);
  const hasPlan =
    !!plan &&
    !["EMPTY", "UNINITIALIZED"].includes(plan.status) &&
    plan.raw_messages_count > 0;

  const notify = useCallback(
    (text: string, kind: Toast["kind"] = "success") => setToast({ text, kind }),
    [],
  );

  const refresh = useCallback(async () => {
    try {
      const [current, traceLog, rejections, currentHealth] = await Promise.all([
        api<PlanResponse>("/plan"),
        api<TraceLog>("/trace"),
        api<Rejection[]>("/rejected"),
        api<JsonRecord>("/health"),
      ]);
      setPlan(current.plan);
      setChecks(current.checks);
      setTrace(traceLog);
      setRejected(rejections);
      setHealth(currentHealth);
      setError("");
      const extras = await Promise.allSettled([
        api<unknown>("/messages"),
        api<JsonRecord>("/facts"),
        api<unknown>("/constraints"),
        api<unknown>("/history"),
        api<JsonRecord>("/overview"),
        api<unknown>("/executions"),
      ]);
      if (extras[0].status === "fulfilled")
        setMessages(asArray(extras[0].value));
      if (extras[1].status === "fulfilled") setFacts(extras[1].value);
      if (extras[2].status === "fulfilled")
        setConstraints(asArray(extras[2].value));
      if (extras[3].status === "fulfilled")
        setHistory(asArray(extras[3].value));
      if (extras[4].status === "fulfilled") setOverview(extras[4].value);
      if (extras[5].status === "fulfilled")
        setExecutions(asArray(extras[5].value));
    } catch (issue) {
      setError(
        issue instanceof Error ? issue.message : "Could not load the event.",
      );
    } finally {
      setInitialLoading(false);
    }
  }, []);

  const refreshWhatsApp = useCallback(async () => {
    try {
      const [status, people, logs, events, approvedTemplates] =
        await Promise.all([
          api<WhatsAppStatus>("/whatsapp/status"),
          api<Recipient[]>("/whatsapp/recipients"),
          api<unknown>("/whatsapp/messages"),
          api<unknown>("/whatsapp/webhooks"),
          api<JsonRecord>("/whatsapp/templates"),
        ]);
      setWaStatus(status);
      setRecipients(people);
      setNotifications(asArray(logs));
      setWebhooks(asArray(events));
      setTemplates(approvedTemplates);
    } catch (issue) {
      notify(
        issue instanceof Error
          ? issue.message
          : "Cannot load WhatsApp configuration.",
        "error",
      );
    }
  }, [notify]);

  useEffect(() => {
    const timer = window.setTimeout(() => void refresh(), 0);
    return () => window.clearTimeout(timer);
  }, [refresh]);
  useEffect(() => {
    if (section !== "whatsapp") return;
    const timer = window.setTimeout(() => void refreshWhatsApp(), 0);
    return () => window.clearTimeout(timer);
  }, [section, refreshWhatsApp]);
  useEffect(() => {
    const syncHash = () => {
      const hash = window.location.hash.slice(1);
      if (navigation.some(([key]) => key === hash)) setSection(hash as Section);
    };
    const timer = window.setTimeout(syncHash, 0);
    window.addEventListener("hashchange", syncHash);
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener("hashchange", syncHash);
    };
  }, []);
  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(null), 9000);
    return () => window.clearTimeout(timer);
  }, [toast]);

  function navigate(next: Section) {
    setSection(next);
    setSidebar(false);
    setSearch("");
    window.history.pushState(null, "", `#${next}`);
  }
  async function action(label: string, operation: () => Promise<void>) {
    if (busy) return;
    setBusy(label);
    try {
      await operation();
    } catch (issue) {
      notify(
        issue instanceof Error ? issue.message : "The operation failed.",
        "error",
      );
    } finally {
      setBusy("");
    }
  }
  async function runPack(which: "sample" | "pack") {
    setConfirmRun(null);
    await action("Generating event plan", async () => {
      const result = await api<RunResponse>("/run", {
        method: "POST",
        body: JSON.stringify({
          ...(which === "pack" ? { raw_text: rawPack } : {}),
          mode,
        }),
      });
      await refresh();
      notify(
        result.status === "invalid"
          ? "The new message pack could not produce a valid plan. Review workflow decisions; any previous valid plan was preserved."
          : result.checks?.all_passed
            ? "Plan generated. All six validation checks passed."
            : "Plan processed. Review validation warnings and unresolved constraints.",
        result.status !== "invalid" && result.checks?.all_passed
          ? "success"
          : "info",
      );
      navigate("dashboard");
    });
  }
  async function submitMessage(event: FormEvent) {
    event.preventDefault();
    await action("Processing message update", async () => {
      const result = await api<RunResponse>("/message", {
        method: "POST",
        body: JSON.stringify({
          message: newMessage,
          sender: sender || "External",
          mode,
        }),
      });
      await refresh();
      if (result.accepted) {
        setNewMessage("");
        notify("Message accepted. The affected planning areas were updated.");
      } else
        notify(
          result.rejection_reason ||
            "Message rejected. The previous valid plan was preserved.",
          "info",
        );
    });
  }
  async function readPack(file?: File) {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".txt")) {
      notify("Choose a UTF-8 .txt message pack.", "error");
      return;
    }
    if (file.size > 512_000) {
      notify("Message packs must be smaller than 500 KB.", "error");
      return;
    }
    try {
      const text = await file.text();
      setRawPack(text);
      setPackName(file.name);
      notify(
        `Loaded ${file.name}. Review the original text before processing.`,
        "info",
      );
    } catch {
      notify("Could not read this file.", "error");
    }
  }
  function toggleTheme() {
    const next = !dark;
    setDark(next);
    document.documentElement.dataset.theme = next ? "dark" : "light";
  }
  const eventName = plan?.event?.name || "Physical hackathon";
  const latestExecution =
    overview.execution && typeof overview.execution === "object"
      ? (overview.execution as JsonRecord)
      : {};
  const factsObject =
    facts.facts && typeof facts.facts === "object"
      ? (facts.facts as JsonRecord)
      : facts;
  const students = hasPlan
    ? (plan?.event?.students ?? field(factsObject, "students", "student_count"))
    : undefined;
  const filteredMessages = messages.filter((message) =>
    JSON.stringify(message).toLowerCase().includes(search.toLowerCase()),
  );
  const filteredTrace = (trace?.entries || []).filter(
    (entry) =>
      (traceArea === "all" || entry.area_tag === traceArea) &&
      JSON.stringify(entry).toLowerCase().includes(search.toLowerCase()),
  );
  const currentRejections = rejected.filter((record) =>
    JSON.stringify(record).toLowerCase().includes(search.toLowerCase()),
  );
  const checkItems: [keyof Checks, string, string][] = [
    ["figures_valid", "Correct figures", "Calculated from source facts"],
    ["budget_valid", "Within budget", "Every expense accounted for"],
    ["venue_fits", "Venue fits", "Capacity and facilities"],
    ["schedule_valid", "Schedule valid", "Durations and required breaks"],
    ["enough_judges", "Enough judges", "Workload and coverage"],
    ["all_areas_covered", "Five areas covered", "Complete operational plan"],
  ];

  function noPlan() {
    return (
      <Empty
        action={
          <button
            className="btn btn-primary"
            onClick={() => navigate("messages")}
          >
            <Icon name="upload" />
            Import message pack
          </button>
        }
      />
    );
  }
  function renderTimeline(compact = false) {
    return (
      <div className="timeline-track space-y-5">
        {plan?.schedule.timeline.map((item, index) => (
          <div className="relative" key={`${item.activity}-${index}`}>
            <span className="timeline-node" />
            <div className="flex flex-wrap justify-between gap-2">
              <div>
                <p className="text-[11px] font-mono text-accent">
                  {item.time_slot}
                </p>
                <p className="mt-1 font-medium">{item.activity}</p>
              </div>
              <Badge>{item.duration_mins} min</Badge>
            </div>
            {!compact ? (
              <div className="mt-2 h-1 overflow-hidden rounded bg-elevated">
                <div
                  className="h-full bg-accent/60"
                  style={{
                    width: `${Math.max(2, (item.duration_mins / ((plan?.schedule.total_duration_hours || 1) * 60)) * 100)}%`,
                  }}
                />
              </div>
            ) : null}
          </div>
        ))}
      </div>
    );
  }
  function renderBudgetChart() {
    if (!plan || !hasPlan) return noPlan();
    const expenses = plan.budget.line_items.filter(
      (line) => line.status !== "REJECTED",
    );
    return (
      <div
        className="space-y-4"
        role="img"
        aria-label={`Budget breakdown. Planned expenditure ${money(plan.budget.total_projected)} of ${money(plan.budget.cap)}.`}
      >
        {expenses.map((item, index) => (
          <div key={`${item.item}-${index}`}>
            <div className="mb-2 flex justify-between gap-3 text-xs">
              <span className="text-muted">{item.item}</span>
              <span className="font-mono">{money(item.amount)}</span>
            </div>
            <div className="h-2 overflow-hidden rounded-sm bg-elevated">
              <div
                className={
                  index % 2 ? "h-full bg-accent/55" : "h-full bg-accent"
                }
                style={{
                  width: `${Math.min(100, Math.max(0, (item.amount / (plan.budget.cap || 1)) * 100))}%`,
                }}
              />
            </div>
          </div>
        ))}
        <div className="mt-5 flex justify-between border-t border-line pt-4">
          <span className="text-muted">Remaining budget</span>
          <strong
            className={
              plan.budget.surplus_deficit < 0 ? "text-danger" : "text-success"
            }
          >
            {money(plan.budget.surplus_deficit)}
          </strong>
        </div>
      </div>
    );
  }

  return (
    <>
      <a href="#main-content" className="skip-link btn btn-primary">
        Skip to content
      </a>
      {sidebar ? (
        <button
          className="fixed inset-0 z-30 bg-black/60 min-[901px]:hidden"
          onClick={() => setSidebar(false)}
          aria-label="Close navigation"
        />
      ) : null}
      <aside
        className={`app-sidebar ${sidebar ? "is-open" : ""}`}
        aria-label="Application navigation"
      >
        <div className="flex items-center gap-3 border-b border-line px-6 py-6">
          <div className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-[#6b2d5c] to-[#314cb6] text-white shadow-sm">
            <Icon name="bolt" size={21} />
          </div>
          <div>
            <span className="text-lg font-bold tracking-tight">
              HackPlan<span className="ml-1 text-[#0075f2]">AI</span>
            </span>
            <p className="mt-0.5 text-[10px] text-muted">
              Mind to Machine 2026
            </p>
          </div>
        </div>
        <div className="px-6 pb-2 pt-6 text-[11px] font-medium text-muted">
          Event workspace
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-2">
          {navigation.map(([key, label]) => (
            <button
              key={key}
              className="nav-item"
              onClick={() => navigate(key)}
              aria-current={section === key ? "page" : undefined}
            >
              <Icon name={key} />
              <span className="flex-1 text-[13px]">{label}</span>
              {key === "rejected" && rejected.length ? (
                <span className="rounded bg-danger/10 px-1.5 text-[10px] text-danger">
                  {rejected.length}
                </span>
              ) : null}
            </button>
          ))}
        </nav>
        <div className="m-4 rounded-lg border border-line bg-background p-3">
          <div className="flex items-center gap-2 text-xs">
            <span
              className={`h-1.5 w-1.5 rounded-full ${error ? "bg-danger" : "bg-success"}`}
            />
            {error
              ? "API unavailable"
              : initialLoading
                ? "Connecting to API"
                : "Local workspace"}
          </div>
          <p className="mt-2 text-[10px] leading-relaxed text-muted">
            Plans and audit history are saved by your local backend.
          </p>
        </div>
        <button
          className="mx-4 mb-4 flex items-center gap-2 text-xs text-muted hover:text-foreground"
          onClick={() => setShowAccess(true)}
        >
          <Icon name="shield" size={15} />
          Organizer access
        </button>
      </aside>

      <div className="app-main">
        <header className="sticky top-0 z-20 flex min-h-[73px] items-center justify-between gap-3 border-b border-line bg-background/95 px-5 backdrop-blur-sm lg:px-9">
          <div className="flex items-center gap-3">
            <button
              className="btn mobile-menu"
              onClick={() => setSidebar(true)}
              aria-label="Open navigation"
              aria-expanded={sidebar}
            >
              <Icon name="menu" />
            </button>
            <div>
              <p className="text-xs text-muted">Event operations</p>
              <p className="mt-0.5 text-sm font-medium">
                {hasPlan ? eventName : "Your planning workspace"}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 sm:gap-3">
            <span className="hidden text-xs text-muted md:block">
              {display(
                health.model ||
                  health.model_provider ||
                  health.provider ||
                  "Provider not loaded",
              )}
            </span>
            <button
              className="btn"
              onClick={toggleTheme}
              aria-label={
                dark ? "Switch to light theme" : "Switch to dark theme"
              }
            >
              <Icon name="sun" size={16} />
            </button>
            <button
              className="btn"
              disabled={!!busy}
              onClick={() => void action("Refreshing workspace", refresh)}
              aria-label="Refresh workspace"
            >
              <Icon
                name="refresh"
                size={16}
                className={busy === "Refreshing workspace" ? "spinner" : ""}
              />
            </button>
            <button
              className="btn btn-primary"
              onClick={() => navigate("messages")}
            >
              <Icon name="upload" size={15} />
              <span className="hidden sm:inline">Import messages</span>
              <span className="sm:hidden">Import</span>
            </button>
          </div>
        </header>

        <main className="content" id="main-content" tabIndex={-1}>
          <div className="mb-7 flex flex-wrap items-end justify-between gap-4">
            <div>
              <h1 className="text-[27px] font-semibold tracking-tight">
                {navigation.find(([key]) => key === section)?.[1]}
              </h1>
              <p className="mt-2 max-w-2xl text-[13px] text-muted">
                {descriptions[section]}
              </p>
            </div>
            {section === "dashboard" ? (
              <Badge
                tone={
                  hasPlan
                    ? checks?.all_passed
                      ? "success"
                      : "warning"
                    : "muted"
                }
              >
                {hasPlan
                  ? checks?.all_passed
                    ? "Plan validated"
                    : "Needs review"
                  : "Awaiting first run"}
              </Badge>
            ) : null}
          </div>
          {error ? (
            <div
              role="alert"
              className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-lg border border-danger/30 bg-danger/5 p-4"
            >
              <div className="flex gap-3">
                <Icon name="rejected" />
                <p className="text-sm text-danger">{error}</p>
              </div>
              <button className="btn" onClick={() => void refresh()}>
                Retry connection
              </button>
            </div>
          ) : null}
          {busy ? (
            <div
              role="status"
              className="mb-6 flex items-center gap-3 rounded-lg border border-accent/30 bg-accent/5 p-4 text-accent"
            >
              <Icon name="refresh" className="spinner" />
              <div>
                <p className="text-sm font-medium">{busy}…</p>
                <p className="text-xs text-muted">
                  Please keep this window open. Processing uses bounded provider
                  calls.
                </p>
              </div>
            </div>
          ) : null}

          {plan?.unresolved_constraints?.length ? (
            <div
              role="alert"
              className="mb-6 rounded-lg border border-warning/30 bg-warning/5 p-4"
            >
              <p className="mb-2 text-sm font-semibold text-warning">
                Unresolved source constraints
              </p>
              <ul className="space-y-2 text-xs text-muted">
                {plan.unresolved_constraints.map((constraint, index) => (
                  <li key={index}>{display(constraint)}</li>
                ))}
              </ul>
            </div>
          ) : null}
          {section === "trace" && trace?.usage_complete === false ? (
            <p className="mb-5 text-xs text-warning">
              Some provider calls did not return token usage. Totals include
              reported usage only.
            </p>
          ) : null}
          {initialLoading ? (
            <div aria-label="Loading workspace" className="space-y-5">
              <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
                {[0, 1, 2, 3].map((index) => (
                  <div key={index} className="panel p-6">
                    <div className="skeleton mb-5 h-3 w-24" />
                    <div className="skeleton h-8 w-28" />
                  </div>
                ))}
              </div>
              <div className="skeleton h-80 w-full" />
            </div>
          ) : (
            <>
              {section === "dashboard" ? (
                <div className="space-y-6">
                  <div className="relative overflow-hidden rounded-xl border border-line bg-surface p-6 sm:p-8">
                    <div
                      className="absolute -right-16 -top-24 h-64 w-64 rounded-full border-[30px] border-accent/[.04]"
                      aria-hidden="true"
                    />
                    <div className="relative flex flex-wrap items-start justify-between gap-6">
                      <div>
                        <div className="mb-3 flex items-center gap-2 text-xs text-accent">
                          <Icon name="venue" size={15} />
                          {plan?.event?.location || "Location not specified"}
                          {plan?.event?.date ? ` · ${plan.event.date}` : ""}
                        </div>
                        <h2 className="text-2xl font-semibold tracking-tight">
                          {hasPlan
                            ? eventName
                            : "From scattered messages to one clear plan."}
                        </h2>
                        <p className="mt-3 max-w-xl text-[13px] text-muted">
                          {hasPlan
                            ? `${plan?.raw_messages_count} source messages. Five connected planning areas. One auditable event plan.`
                            : "Import your emails, WhatsApp texts, and notices. The engine extracts facts, checks constraints, and brings your event together."}
                        </p>
                        <div className="mt-5 flex flex-wrap gap-3">
                          <button
                            className="btn btn-primary"
                            disabled={!!busy}
                            onClick={() => setConfirmRun("sample")}
                          >
                            <Icon name="play" size={15} />
                            {hasPlan
                              ? "Process sample pack"
                              : "Run official sample pack"}
                          </button>
                          <button
                            className="btn"
                            onClick={() =>
                              navigate(hasPlan ? "trace" : "messages")
                            }
                          >
                            <Icon
                              name={hasPlan ? "trace" : "upload"}
                              size={15}
                            />
                            {hasPlan
                              ? "Inspect execution"
                              : "Import your own pack"}
                          </button>
                        </div>
                      </div>
                      <div className="min-w-[145px] border-l border-line pl-6">
                        <p className="text-xs text-muted">Overall validation</p>
                        <p
                          className={`mt-2 text-4xl font-semibold tracking-tight ${hasPlan && checks?.all_passed ? "text-success" : "text-muted"}`}
                        >
                          {hasPlan && checks
                            ? `${checkItems.filter(([key]) => checks[key] === true).length}/6`
                            : "—"}
                        </p>
                        <p className="mt-2 text-xs text-muted">
                          {hasPlan
                            ? "checks passed"
                            : "Waiting for source facts"}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
                    <Stat
                      label="Students / teams"
                      value={
                        hasPlan
                          ? `${display(students)} / ${number(plan?.judging.teams_count)}`
                          : "—"
                      }
                      note={
                        hasPlan
                          ? `${number(plan?.judging.selected_judges ?? plan?.judging.confirmed_judges)} judges in the plan`
                          : "Derived from message pack"
                      }
                      icon="judging"
                    />
                    <Stat
                      label="Approved budget"
                      value={hasPlan ? money(plan?.budget.cap) : "—"}
                      note="Source-approved event funding"
                      icon="budget"
                    />
                    <Stat
                      label="Planned expenditure"
                      value={
                        hasPlan ? money(plan?.budget.total_projected) : "—"
                      }
                      note={
                        hasPlan
                          ? `${money(plan?.budget.total_committed)} committed`
                          : "No expenses calculated yet"
                      }
                      icon="budget"
                    />
                    <Stat
                      label="Remaining budget"
                      value={
                        hasPlan ? money(plan?.budget.surplus_deficit) : "—"
                      }
                      note="After all planned expenses"
                      icon="shield"
                      tone={
                        hasPlan
                          ? (plan?.budget.surplus_deficit || 0) >= 0
                            ? "text-success"
                            : "text-danger"
                          : ""
                      }
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3 xl:grid-cols-6">
                    {checkItems.map(([key, title, detail]) => (
                      <div
                        key={key}
                        className="rounded-lg border border-line bg-surface px-4 py-4"
                      >
                        <div
                          className={`mb-3 flex h-7 w-7 items-center justify-center rounded-full ${hasPlan ? (checks?.[key] ? "bg-success/10 text-success" : "bg-danger/10 text-danger") : "bg-elevated text-muted"}`}
                        >
                          <Icon
                            name={hasPlan && !checks?.[key] ? "close" : "check"}
                            size={15}
                          />
                        </div>
                        <p className="text-xs font-semibold">{title}</p>
                        <p className="mt-1.5 text-[10px] leading-relaxed text-muted">
                          {detail}
                        </p>
                        <p
                          className={`mt-2 text-[10px] ${hasPlan ? (checks?.[key] ? "text-success" : "text-danger") : "text-muted"}`}
                        >
                          {hasPlan
                            ? checks?.[key]
                              ? "Passed"
                              : "Review required"
                            : "Not evaluated"}
                        </p>
                      </div>
                    ))}
                  </div>
                  <div className="grid gap-6 xl:grid-cols-[1.1fr_1fr]">
                    <Panel
                      title="Event timeline"
                      subtitle={
                        hasPlan
                          ? `${plan?.schedule.total_duration_hours} hours planned`
                          : "Built from source constraints"
                      }
                      action={
                        <button
                          className="text-xs text-accent"
                          onClick={() => navigate("schedule")}
                        >
                          View schedule
                        </button>
                      }
                    >
                      {hasPlan ? renderTimeline(true) : noPlan()}
                    </Panel>
                    <Panel
                      title="Budget allocation"
                      subtitle="Expense proportions against the approved cap"
                      action={<Icon name="budget" />}
                    >
                      {hasPlan ? renderBudgetChart() : noPlan()}
                    </Panel>
                  </div>
                  <div className="grid gap-6 xl:grid-cols-[1.1fr_1fr]">
                    <Panel title="Planning areas" noPadding>
                      <Table
                        headers={[
                          "Planning area",
                          "Current decision",
                          "Status",
                        ]}
                        rows={[
                          [
                            "Venue",
                            hasPlan
                              ? plan?.venue.selected_room
                              : "Awaiting source facts",
                            hasPlan ? (
                              <Badge
                                tone={
                                  checks?.venue_fits ? "success" : "warning"
                                }
                              >
                                {checks?.venue_fits ? "Validated" : "Review"}
                              </Badge>
                            ) : (
                              <Badge>Pending</Badge>
                            ),
                          ],
                          [
                            "Food & catering",
                            hasPlan
                              ? `${plan?.food.headcount} meals · ${plan?.food.caterer_tier}`
                              : "Awaiting source facts",
                            <Badge key="food">
                              {hasPlan ? "Planned" : "Pending"}
                            </Badge>,
                          ],
                          [
                            "Judging",
                            hasPlan
                              ? `${plan?.judging.teams_count} teams · ${plan?.judging.confirmed_judges} judges`
                              : "Awaiting source facts",
                            <Badge key="judging">
                              {hasPlan ? "Assigned" : "Pending"}
                            </Badge>,
                          ],
                        ]}
                      />
                    </Panel>
                    <Panel
                      title="Latest processing"
                      action={
                        <Badge tone={busy ? "accent" : "muted"}>
                          {busy ? "Running" : "Idle"}
                        </Badge>
                      }
                    >
                      <dl className="space-y-4 text-xs">
                        <div className="flex justify-between gap-4">
                          <dt className="text-muted">Last plan update</dt>
                          <dd>
                            {hasPlan
                              ? time(plan?.last_updated)
                              : "No execution yet"}
                          </dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-muted">Actual model calls</dt>
                          <dd>{number(trace?.total_calls)}</dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-muted">
                            Provider-reported tokens
                          </dt>
                          <dd>
                            {trace?.overall_total_tokens == null
                              ? "Unavailable"
                              : number(trace.overall_total_tokens)}
                          </dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-muted">Rejected messages</dt>
                          <dd>{rejected.length}</dd>
                        </div>
                        <div className="flex justify-between gap-4">
                          <dt className="text-muted">Execution duration</dt>
                          <dd>
                            {typeof latestExecution.duration_seconds ===
                            "number"
                              ? `${latestExecution.duration_seconds.toFixed(2)} s`
                              : "See execution history"}
                          </dd>
                        </div>
                      </dl>
                    </Panel>
                  </div>
                  <Panel
                    title="Recent source messages"
                    action={
                      <button
                        className="text-xs text-accent"
                        onClick={() => navigate("messages")}
                      >
                        Open message center
                      </button>
                    }
                    noPadding
                  >
                    <Table
                      headers={["Sender", "Source", "Message"]}
                      rows={messages
                        .slice(-4)
                        .reverse()
                        .map((message) => [
                          display(field(message, "sender", "from")),
                          display(field(message, "source", "channel")),
                          <p
                            key="text"
                            className="max-w-2xl line-clamp-2 text-muted"
                          >
                            {display(
                              field(
                                message,
                                "text",
                                "raw_text",
                                "content",
                                "message",
                              ),
                            )}
                          </p>,
                        ])}
                    />
                  </Panel>
                </div>
              ) : null}

              {section === "messages" ? (
                <div className="space-y-6">
                  <div className="grid gap-6 xl:grid-cols-2">
                    <Panel
                      title="Import message pack"
                      subtitle="English and Roman Urdu · UTF-8 TXT · maximum 500 KB"
                    >
                      <div className="mb-5 rounded-lg border border-dashed border-line bg-background p-6 text-center">
                        <Icon
                          name="upload"
                          className="mx-auto mb-3 text-accent"
                          size={25}
                        />
                        <p className="text-sm font-medium">
                          Bring all your event messages together
                        </p>
                        <p className="mt-1 text-xs text-muted">
                          Choose a text file, or paste its unedited contents
                          below.
                        </p>
                        <input
                          ref={uploadRef}
                          type="file"
                          accept=".txt,text/plain"
                          aria-label="Upload TXT message pack"
                          onChange={(event) =>
                            void readPack(event.target.files?.[0])
                          }
                          className="mt-4 max-w-full text-xs text-muted file:mr-3 file:rounded file:border file:border-line file:bg-elevated file:px-3 file:py-2 file:text-foreground"
                        />
                        {packName ? (
                          <p className="mt-3 text-xs text-accent">{packName}</p>
                        ) : null}
                      </div>
                      <label className="field-label" htmlFor="pack-text">
                        Original message pack
                      </label>
                      <textarea
                        id="pack-text"
                        className="field min-h-48 font-mono text-xs"
                        value={rawPack}
                        onChange={(event) => setRawPack(event.target.value)}
                        placeholder="Paste the complete pack, including senders, dates, and original messages…"
                      />
                      <div className="mt-4 flex flex-wrap items-end justify-between gap-4">
                        <div>
                          <label
                            className="field-label"
                            htmlFor="processing-mode"
                          >
                            Processing mode
                          </label>
                          <select
                            id="processing-mode"
                            value={mode}
                            onChange={(event) => setMode(event.target.value)}
                            className="field text-xs"
                          >
                            <option value="auto">
                              Automatic (configured model)
                            </option>
                            <option value="provider">
                              Require live AI provider
                            </option>
                            <option value="offline">
                              Offline parser (no model calls)
                            </option>
                          </select>
                        </div>
                        <button
                          className="btn btn-primary"
                          disabled={!!busy || !rawPack.trim()}
                          onClick={() => setConfirmRun("pack")}
                        >
                          <Icon name="play" size={15} />
                          Process message pack
                        </button>
                      </div>
                    </Panel>
                    <Panel
                      title="Submit an event update"
                      subtitle="The current valid plan is preserved when an update conflicts."
                    >
                      <form
                        onSubmit={(event) => void submitMessage(event)}
                        className="space-y-4"
                      >
                        <div>
                          <label
                            htmlFor="message-sender"
                            className="field-label"
                          >
                            Sender or source
                          </label>
                          <input
                            id="message-sender"
                            value={sender}
                            onChange={(event) => setSender(event.target.value)}
                            className="field"
                            maxLength={120}
                            placeholder="Finance, caterer, organizer…"
                          />
                        </div>
                        <div>
                          <label htmlFor="new-message" className="field-label">
                            New message
                          </label>
                          <textarea
                            id="new-message"
                            value={newMessage}
                            onChange={(event) => {
                              setNewMessage(event.target.value);
                              setPrediction(null);
                            }}
                            className="field min-h-48"
                            maxLength={20000}
                            required
                            placeholder="Paste the original update in English or Roman Urdu…"
                          />
                        </div>
                        <div className="rounded-lg border border-line bg-background p-3 text-xs text-muted">
                          <div className="mb-1 flex items-center gap-2 text-foreground">
                            <Icon name="shield" size={15} />
                            Updates are validated before saving
                          </div>
                          Only affected planning areas are recalculated.
                          Conflicts are recorded with a reason.
                        </div>
                        <button
                          type="button"
                          className="btn w-full"
                          disabled={!!busy || !newMessage.trim()}
                          onClick={() =>
                            void action(
                              "Predicting affected areas",
                              async () => {
                                setPrediction(
                                  await api<JsonRecord>(
                                    `/predict?message=${encodeURIComponent(newMessage)}`,
                                  ),
                                );
                              },
                            )
                          }
                        >
                          Predict affected areas
                        </button>
                        {prediction ? (
                          <div className="rounded border border-accent/25 bg-accent/5 p-3 text-xs">
                            <p className="font-semibold text-accent">
                              Predicted planning areas
                            </p>
                            <p className="mt-2">
                              {display(prediction.affected_areas)}
                            </p>
                            <p className="mt-2 text-muted">
                              {mode === "offline"
                                ? "Offline parsing: no model calls."
                                : `Predicted model-call tags: ${display(prediction.model_call_areas ?? prediction.affected_areas)}. At most ${display(prediction.maximum_model_calls)} extraction call; planning calculations use deterministic code.`}
                            </p>
                          </div>
                        ) : null}
                        <button
                          type="submit"
                          className="btn btn-primary w-full"
                          disabled={!!busy || !hasPlan || !newMessage.trim()}
                        >
                          <Icon name="arrow" size={15} />
                          Process update
                        </button>
                        {!hasPlan ? (
                          <p className="text-xs text-warning">
                            Generate an initial plan before submitting updates.
                          </p>
                        ) : null}
                      </form>
                    </Panel>
                  </div>
                  <Panel
                    title="Original messages"
                    subtitle={`${messages.length} persisted source records`}
                    action={
                      <Search
                        value={search}
                        onChange={setSearch}
                        label="Search messages"
                      />
                    }
                    noPadding
                  >
                    <Table
                      headers={[
                        "Reference",
                        "Sender / source",
                        "Date",
                        "Original message",
                        "Status",
                      ]}
                      rows={filteredMessages.map((message, index) => [
                        display(
                          field(message, "id", "message_id", "index") ??
                            index + 1,
                        ),
                        <div key="sender">
                          <p>{display(field(message, "sender", "from"))}</p>
                          <p className="mt-1 text-[11px] text-muted">
                            {display(field(message, "source", "channel"))}
                          </p>
                        </div>,
                        display(
                          field(message, "date", "timestamp", "created_at"),
                        ),
                        <p
                          key="message"
                          className="min-w-64 max-w-2xl whitespace-pre-wrap break-words text-muted"
                        >
                          {display(
                            field(
                              message,
                              "text",
                              "raw_text",
                              "content",
                              "message",
                            ),
                          )}
                        </p>,
                        <Badge key="status">
                          {display(
                            field(message, "status", "processing_status") ||
                              "Processed",
                          )}
                        </Badge>,
                      ])}
                    />
                  </Panel>
                  <div className="grid gap-6 xl:grid-cols-2">
                    <Panel
                      title="Extracted facts"
                      subtitle="Structured values retained by the backend"
                      noPadding
                    >
                      <Table
                        headers={["Fact", "Value"]}
                        rows={Object.entries(factsObject).map(
                          ([key, value]) => [
                            key.replaceAll("_", " "),
                            <pre
                              key="value"
                              className="max-w-lg text-xs text-muted"
                            >
                              {display(value)}
                            </pre>,
                          ],
                        )}
                      />
                    </Panel>
                    <Panel
                      title="Extracted constraints"
                      subtitle="Source rules and unresolved requirements"
                      noPadding
                    >
                      <Table
                        headers={["Area", "Constraint", "Status"]}
                        rows={constraints.map((constraint) => [
                          display(field(constraint, "area", "planning_area")),
                          <pre key="constraint" className="max-w-md text-xs">
                            {display(constraint)}
                          </pre>,
                          <Badge
                            key="status"
                            tone={
                              constraint.status === "unresolved" ||
                              constraint.effective_status === "unresolved"
                                ? "warning"
                                : "muted"
                            }
                          >
                            {display(
                              field(constraint, "status", "effective_status") ||
                                "Active",
                            )}
                          </Badge>,
                        ])}
                      />
                    </Panel>
                  </div>
                </div>
              ) : null}

              {section === "venue" ? (
                <div className="space-y-6">
                  {hasPlan && plan ? (
                    <>
                      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
                        <Stat
                          label="Selected venue"
                          value={plan.venue.selected_room || "Unresolved"}
                          icon="venue"
                        />
                        <Stat
                          label="Seating capacity"
                          value={number(plan.venue.capacity)}
                          note={`${display(plan.event?.required_headcount ?? checks?.details.headcount_required)} required seats`}
                        />
                        <Stat
                          label="Venue cost"
                          value={money(plan.venue.cost)}
                          icon="budget"
                        />
                        <Stat
                          label="Standby generator"
                          value={
                            plan.venue.generator_standby
                              ? "Available"
                              : "Not confirmed"
                          }
                          icon="bolt"
                        />
                      </div>
                      <Panel
                        title="Selection rationale"
                        action={
                          <Badge
                            tone={checks?.venue_fits ? "success" : "warning"}
                          >
                            {checks?.venue_fits
                              ? "Capacity validated"
                              : "Review constraints"}
                          </Badge>
                        }
                      >
                        <p className="text-sm text-muted">
                          {plan.venue.rationale}
                        </p>
                        {plan.venue.facilities?.length ? (
                          <div className="mt-4 flex flex-wrap gap-2">
                            {plan.venue.facilities.map((item) => (
                              <Badge key={item}>{item}</Badge>
                            ))}
                          </div>
                        ) : null}
                      </Panel>
                      <Panel
                        title="Available venue options"
                        subtitle="Quotes and facilities extracted from the source pack"
                        noPadding
                      >
                        <Table
                          headers={[
                            "Venue",
                            "Capacity",
                            "Price",
                            "Generator",
                            "Facilities",
                            "Selection",
                          ]}
                          rows={(
                            plan.venue.options ||
                            asArray(
                              factsObject.venues || factsObject.venue_options,
                            )
                          ).map((option) => [
                            display(
                              field(
                                option,
                                "name",
                                "room",
                                "venue",
                                "selected_room",
                              ),
                            ),
                            display(field(option, "capacity", "seats")),
                            money(
                              Number(
                                field(option, "cost", "price", "rental_cost") ||
                                  0,
                              ),
                            ),
                            field(
                              option,
                              "generator",
                              "generator_standby",
                              "has_generator",
                            ) === true
                              ? "Available"
                              : "Not stated",
                            display(option.facilities),
                            <Badge
                              key="selection"
                              tone={
                                field(option, "name", "room", "venue") ===
                                plan.venue.selected_room
                                  ? "accent"
                                  : "muted"
                              }
                            >
                              {field(option, "name", "room", "venue") ===
                              plan.venue.selected_room
                                ? "Selected"
                                : "Alternative"}
                            </Badge>,
                          ])}
                        />
                      </Panel>
                      <DomainConstraints
                        area="venue"
                        constraints={constraints}
                      />
                    </>
                  ) : (
                    noPlan()
                  )}
                </div>
              ) : null}

              {section === "schedule" ? (
                <div className="space-y-6">
                  {hasPlan && plan ? (
                    <>
                      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
                        <Stat
                          label="Event duration"
                          value={`${plan.schedule.total_duration_hours} hours`}
                          icon="clock"
                        />
                        <Stat
                          label="Prayer break"
                          value={`${plan.schedule.prayer_break_minutes} min`}
                          note="As required by source messages"
                        />
                        <Stat
                          label="Judging block"
                          value={`${plan.judging.duration_minutes} min`}
                          icon="judging"
                        />
                        <Stat
                          label="Timeline validation"
                          value={
                            checks?.schedule_valid ? "Passed" : "Needs review"
                          }
                          tone={
                            checks?.schedule_valid
                              ? "text-success"
                              : "text-warning"
                          }
                        />
                      </div>
                      <div className="grid gap-6 xl:grid-cols-[1fr_1.3fr]">
                        <Panel
                          title="Event timeline"
                          subtitle="Relative times are shown when no start time is provided."
                        >
                          {renderTimeline()}
                        </Panel>
                        <Panel title="Activity durations" noPadding>
                          <Table
                            headers={["Time slot", "Activity", "Duration"]}
                            rows={plan.schedule.timeline.map((item) => [
                              item.time_slot,
                              item.activity,
                              `${item.duration_mins} min`,
                            ])}
                            caption={`Total: ${plan.schedule.timeline.reduce((sum, item) => sum + item.duration_mins, 0)} minutes.`}
                          />
                          <div className="p-5">
                            <Badge
                              tone={
                                checks?.schedule_valid ? "success" : "warning"
                              }
                            >
                              {checks?.schedule_valid
                                ? "Timeline satisfies required duration and breaks"
                                : "Review timeline conflicts"}
                            </Badge>
                            {plan.schedule.conflicts?.map((conflict) => (
                              <p
                                className="mt-3 text-xs text-danger"
                                key={conflict}
                              >
                                {conflict}
                              </p>
                            ))}
                          </div>
                        </Panel>
                      </div>
                      <DomainConstraints
                        area="schedule"
                        constraints={constraints}
                      />
                    </>
                  ) : (
                    noPlan()
                  )}
                </div>
              ) : null}

              {section === "judging" ? (
                <div className="space-y-6">
                  {hasPlan && plan ? (
                    <>
                      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
                        <Stat
                          label="Teams"
                          value={number(plan.judging.teams_count)}
                          note={`${display(students)} students in source facts`}
                          icon="judging"
                        />
                        <Stat
                          label="Confirmed judges"
                          value={number(plan.judging.confirmed_judges)}
                          note={`${plan.judging.selected_judges ?? plan.judging.confirmed_judges} allocated · ${money(plan.judging.honorarium_per_judge)} each`}
                        />
                        <Stat
                          label="Teams per judge"
                          value={number(plan.judging.teams_per_judge)}
                          note="Backend-validated allocation"
                        />
                        <Stat
                          label="Judging time"
                          value={`${plan.judging.minutes_per_team} min / team`}
                          note={`${plan.judging.duration_minutes} minute concurrent block`}
                          icon="clock"
                        />
                      </div>
                      <Panel
                        title="Judge assignments"
                        subtitle="Generated identifiers represent assignments, not source-provided names."
                        action={
                          <Badge
                            tone={checks?.enough_judges ? "success" : "warning"}
                          >
                            {checks?.enough_judges
                              ? "Workload validated"
                              : "Assignment review required"}
                          </Badge>
                        }
                        noPadding
                      >
                        <Table
                          headers={[
                            "Judge",
                            "Teams",
                            "Workload / slots",
                            "Availability",
                          ]}
                          rows={(plan.judging.assignments || []).map(
                            (assignment) => [
                              display(
                                field(
                                  assignment,
                                  "judge_id",
                                  "judge",
                                  "judge_identifier",
                                ),
                              ),
                              display(
                                field(
                                  assignment,
                                  "team_id",
                                  "team_ids",
                                  "teams",
                                  "assigned_teams",
                                ),
                              ),
                              assignment.slot != null
                                ? `Slot ${display(assignment.slot)}: ${display(assignment.start_minute)}–${display(assignment.end_minute)} min`
                                : display(
                                    field(
                                      assignment,
                                      "slots",
                                      "duration_minutes",
                                      "minutes",
                                      "workload",
                                    ),
                                  ),
                              display(
                                field(
                                  assignment,
                                  "availability",
                                  "available_from",
                                  "status",
                                ) || "No individual window specified",
                              ),
                            ],
                          )}
                        />
                      </Panel>
                      <div className="grid gap-6 xl:grid-cols-2">
                        <Panel title="Coverage and conflicts">
                          {plan.judging.availability?.length ? (
                            <div className="mb-4">
                              <h3 className="mb-2 text-xs font-semibold">
                                Source availability notes
                              </h3>
                              {plan.judging.availability.map((note, index) => (
                                <pre
                                  key={index}
                                  className="mb-2 rounded border border-line bg-background p-3 text-xs text-muted"
                                >
                                  {display(note)}
                                </pre>
                              ))}
                            </div>
                          ) : null}
                          <p className="text-sm text-muted">
                            Unassigned teams:{" "}
                            <strong className="text-foreground">
                              {plan.judging.unassigned_teams?.length ??
                                (checks?.enough_judges ? 0 : "Not established")}
                            </strong>
                          </p>
                          {plan.judging.unassigned_teams?.length ? (
                            <p className="mt-3 text-xs text-warning">
                              {plan.judging.unassigned_teams.join(", ")}
                            </p>
                          ) : null}
                          {plan.judging.conflicts?.map((conflict) => (
                            <p
                              key={conflict}
                              className="mt-3 text-sm text-danger"
                            >
                              {conflict}
                            </p>
                          ))}
                          <p className="mt-4 text-xs text-muted">
                            Student names and team membership are displayed only
                            when present in the source. The planner does not
                            invent personal records.
                          </p>
                        </Panel>
                        <DomainConstraints
                          area="judging"
                          constraints={constraints}
                        />
                      </div>
                    </>
                  ) : (
                    noPlan()
                  )}
                </div>
              ) : null}

              {section === "food" ? (
                <div className="space-y-6">
                  {hasPlan && plan ? (
                    <>
                      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
                        <Stat
                          label="Required meals"
                          value={number(plan.food.headcount)}
                          icon="food"
                        />
                        <Stat
                          label="Meal price"
                          value={money(plan.food.unit_cost)}
                          note={plan.food.caterer_tier}
                        />
                        <Stat
                          label="Delivery expense"
                          value={
                            plan.food.delivery_cost == null
                              ? "See terms"
                              : money(plan.food.delivery_cost)
                          }
                          note={plan.food.delivery_terms}
                        />
                        <Stat
                          label="Total catering"
                          value={money(plan.food.total_cost)}
                          icon="budget"
                        />
                      </div>
                      <div className="grid gap-6 xl:grid-cols-2">
                        <Panel title="Attendee categories" noPadding>
                          <Table
                            headers={["Category", "Count"]}
                            rows={[
                              ["Students", display(students)],
                              [
                                "Staff",
                                display(
                                  plan.event?.staff ??
                                    field(factsObject, "staff", "staff_count"),
                                ),
                              ],
                              [
                                "Judges in event plan",
                                number(
                                  plan.food.attendee_categories?.judges ??
                                    plan.judging.selected_judges ??
                                    plan.judging.confirmed_judges,
                                ),
                              ],
                              ["Meals required", number(plan.food.headcount)],
                            ]}
                            caption="Meal quantities follow the validated plan; source-specific attendance rules may affect the total."
                          />
                        </Panel>
                        <Panel title="Selected catering">
                          <div className="mb-5 flex items-center justify-between gap-4">
                            <h3 className="text-lg font-semibold">
                              {plan.food.caterer_tier}
                            </h3>
                            <Badge tone="accent">Current selection</Badge>
                          </div>
                          <p className="font-mono text-lg">
                            {plan.food.headcount} × {money(plan.food.unit_cost)}
                          </p>
                          <p className="mt-3 text-sm text-muted">
                            {plan.food.delivery_terms}
                          </p>
                          <div className="mt-5 flex justify-between border-t border-line pt-4">
                            <span className="text-muted">
                              Total including delivery
                            </span>
                            <strong>{money(plan.food.total_cost)}</strong>
                          </div>
                        </Panel>
                      </div>
                      <Panel
                        title="Supplier options and current quotes"
                        noPadding
                      >
                        <Table
                          headers={[
                            "Option",
                            "Unit price",
                            "Delivery",
                            "Source / effective date",
                          ]}
                          rows={(
                            plan.food.options ||
                            asArray(
                              factsObject.catering_options ||
                                factsObject.food_options,
                            )
                          ).map((option) => [
                            display(
                              field(option, "name", "tier", "caterer_tier"),
                            ),
                            money(
                              Number(
                                field(
                                  option,
                                  "unit_cost",
                                  "price",
                                  "unit_price",
                                ) || 0,
                              ),
                            ),
                            display(
                              field(
                                option,
                                "delivery_terms",
                                "delivery_cost",
                                "delivery",
                              ),
                            ),
                            display(
                              field(option, "source", "date", "source_message"),
                            ),
                          ])}
                        />
                      </Panel>
                      <DomainConstraints
                        area="food"
                        constraints={constraints}
                      />
                      <Panel title="Rejected supplier changes">
                        {rejected.filter((record) =>
                          record.target_area.includes("food"),
                        ).length ? (
                          rejected
                            .filter((record) =>
                              record.target_area.includes("food"),
                            )
                            .map((record, index) => (
                              <div
                                key={index}
                                className="mb-3 border-l-2 border-danger pl-4"
                              >
                                <p className="text-sm">{record.raw_text}</p>
                                <p className="mt-2 text-xs text-danger">
                                  {record.rejection_reason}
                                </p>
                              </div>
                            ))
                        ) : (
                          <p className="text-sm text-muted">
                            No rejected catering changes.
                          </p>
                        )}
                      </Panel>
                    </>
                  ) : (
                    noPlan()
                  )}
                </div>
              ) : null}

              {section === "budget" ? (
                <div className="space-y-6">
                  {hasPlan && plan ? (
                    <>
                      <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
                        <Stat
                          label="Approved budget"
                          value={money(plan.budget.cap)}
                          icon="budget"
                        />
                        <Stat
                          label="Committed expenses"
                          value={money(plan.budget.total_committed)}
                          note="Previously authorized costs"
                        />
                        <Stat
                          label="Total planned"
                          value={money(plan.budget.total_projected)}
                          note={`${money(plan.budget.total_variable)} variable costs`}
                        />
                        <Stat
                          label="Remaining funds"
                          value={money(plan.budget.surplus_deficit)}
                          tone={
                            plan.budget.surplus_deficit >= 0
                              ? "text-success"
                              : "text-danger"
                          }
                        />
                      </div>
                      {!checks?.budget_valid ? (
                        <div
                          role="alert"
                          className="rounded-lg border border-danger/30 p-4 text-danger"
                        >
                          Budget validation failed. Review spending and
                          unresolved financial constraints.
                        </div>
                      ) : null}
                      <div className="grid gap-6 xl:grid-cols-[1fr_1.7fr]">
                        <Panel
                          title="Expense breakdown"
                          subtitle="Proportion of approved budget"
                        >
                          {renderBudgetChart()}
                        </Panel>
                        <Panel
                          title="Expense ledger"
                          subtitle="All calculations are made by the backend."
                          action={
                            <Badge
                              tone={
                                checks?.budget_valid ? "success" : "warning"
                              }
                            >
                              {checks?.budget_valid
                                ? "Within budget"
                                : "Over limit / unresolved"}
                            </Badge>
                          }
                          noPadding
                        >
                          <Table
                            headers={[
                              "Category",
                              "Expense",
                              "Authorization",
                              "Amount",
                            ]}
                            rows={plan.budget.line_items.map((line) => [
                              line.category,
                              line.item,
                              <Badge
                                key="status"
                                tone={
                                  line.status === "REJECTED"
                                    ? "danger"
                                    : "muted"
                                }
                              >
                                {line.status}
                              </Badge>,
                              <span
                                key="amount"
                                className="whitespace-nowrap font-mono"
                              >
                                {money(line.amount)}
                              </span>,
                            ])}
                          />
                          <div className="flex justify-between border-t border-line p-5 font-semibold">
                            <span>Total planned expenditure</span>
                            <span>{money(plan.budget.total_projected)}</span>
                          </div>
                        </Panel>
                      </div>
                      <DomainConstraints
                        area="budget"
                        constraints={constraints}
                      />
                    </>
                  ) : (
                    noPlan()
                  )}
                </div>
              ) : null}

              {section === "trace" ? (
                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4 xl:grid-cols-4">
                    <Stat
                      label="Actual model calls"
                      value={number(trace?.total_calls)}
                      icon="trace"
                    />
                    <Stat
                      label="Input tokens"
                      value={
                        trace?.total_prompt_tokens == null
                          ? "Unavailable"
                          : number(trace.total_prompt_tokens)
                      }
                      note="Reported by the provider"
                    />
                    <Stat
                      label="Output tokens"
                      value={
                        trace?.total_completion_tokens == null
                          ? "Unavailable"
                          : number(trace.total_completion_tokens)
                      }
                      note="Reported by the provider"
                    />
                    <Stat
                      label="Total tokens"
                      value={
                        trace?.overall_total_tokens == null
                          ? "Unavailable"
                          : number(trace.overall_total_tokens)
                      }
                      note="No estimated usage is presented"
                      icon="bolt"
                    />
                  </div>
                  <Panel
                    title="Model call trace"
                    subtitle="Exact model identifiers, inputs, outputs, and provider usage."
                    action={
                      <div className="flex flex-wrap gap-2">
                        <Search
                          value={search}
                          onChange={setSearch}
                          label="Search model trace"
                        />
                        <select
                          className="field max-w-36 text-xs"
                          aria-label="Filter trace area"
                          value={traceArea}
                          onChange={(event) => setTraceArea(event.target.value)}
                        >
                          <option value="all">All areas</option>
                          {[
                            "reading",
                            "venue",
                            "schedule",
                            "food",
                            "judging",
                            "budget",
                          ].map((area) => (
                            <option key={area}>{area}</option>
                          ))}
                        </select>
                      </div>
                    }
                    noPadding
                  >
                    {filteredTrace.length ? (
                      <div className="divide-y divide-line">
                        {filteredTrace.map((entry) => (
                          <details className="group" key={entry.call_number}>
                            <summary className="flex list-none flex-wrap items-center justify-between gap-3 px-5 py-5 hover:bg-elevated/50">
                              <div className="flex items-center gap-3">
                                <span className="grid h-8 w-8 place-items-center rounded border border-line bg-background font-mono text-xs text-accent">
                                  #{entry.call_number}
                                </span>
                                <div>
                                  <p className="break-all text-sm font-medium">
                                    {entry.model_name}
                                  </p>
                                  <p className="mt-1 text-[10px] text-muted">
                                    {entry.duration_seconds != null
                                      ? `${entry.duration_seconds.toFixed(2)} s`
                                      : entry.duration_ms != null
                                        ? `${entry.duration_ms} ms`
                                        : "Duration unavailable"}
                                    {entry.retry
                                      ? ` · Retry ${entry.retry}`
                                      : ""}
                                  </p>
                                </div>
                              </div>
                              <div className="flex items-center gap-3">
                                <Badge tone="accent">{entry.area_tag}</Badge>
                                <Badge
                                  tone={
                                    entry.status === "error" || entry.error
                                      ? "danger"
                                      : "muted"
                                  }
                                >
                                  {entry.status ||
                                    (entry.error ? "Error" : "Recorded")}
                                </Badge>
                                <span className="font-mono text-xs text-muted">
                                  {entry.total_tokens == null
                                    ? "Usage unavailable"
                                    : `${number(entry.total_tokens)} tokens`}
                                </span>
                                <span className="text-xs text-accent group-open:rotate-90">
                                  ›
                                </span>
                              </div>
                            </summary>
                            <div className="grid gap-4 border-t border-line bg-background p-5 xl:grid-cols-2">
                              <div>
                                <p className="mb-2 text-xs text-accent">
                                  Exact model input
                                </p>
                                <pre className="max-h-96 overflow-auto rounded-lg border border-line p-4 font-mono text-xs text-muted">
                                  {entry.input}
                                </pre>
                              </div>
                              <div>
                                <p className="mb-2 text-xs text-success">
                                  Exact model output
                                </p>
                                <pre className="max-h-96 overflow-auto rounded-lg border border-line p-4 font-mono text-xs text-muted">
                                  {entry.output || "No output returned"}
                                </pre>
                              </div>
                              <p className="text-xs text-muted xl:col-span-2">
                                Input:{" "}
                                {entry.prompt_tokens == null
                                  ? "Unavailable"
                                  : number(entry.prompt_tokens)}{" "}
                                · Output:{" "}
                                {entry.completion_tokens == null
                                  ? "Unavailable"
                                  : number(entry.completion_tokens)}{" "}
                                · Total:{" "}
                                {entry.total_tokens == null
                                  ? "Unavailable"
                                  : number(entry.total_tokens)}
                              </p>
                              {entry.error ? (
                                <p className="text-sm text-danger xl:col-span-2">
                                  {entry.error}
                                </p>
                              ) : null}
                            </div>
                          </details>
                        ))}
                      </div>
                    ) : (
                      <Empty
                        title="No model calls recorded"
                        text="Offline parsing makes no model calls. Provider calls appear here after an AI execution; failures are also recorded."
                      />
                    )}
                  </Panel>
                  <Panel
                    title="Execution history"
                    subtitle="Persisted run timings and update outcomes"
                    noPadding
                  >
                    <Table
                      headers={[
                        "Execution",
                        "Status",
                        "Affected areas",
                        "Model calls",
                        "Duration",
                      ]}
                      rows={executions.map((execution) => [
                        display(execution.kind),
                        <Badge
                          key="status"
                          tone={
                            execution.status === "failed"
                              ? "danger"
                              : execution.status === "rejected"
                                ? "warning"
                                : "muted"
                          }
                        >
                          {display(execution.status)}
                        </Badge>,
                        display(execution.affected_areas),
                        display(execution.model_calls),
                        typeof execution.duration_seconds === "number"
                          ? `${execution.duration_seconds.toFixed(3)} s`
                          : "Not recorded",
                      ])}
                    />
                  </Panel>
                  <Panel
                    title="Workflow decisions"
                    subtitle="Deterministic planning, updates, and rejection events"
                  >
                    {trace?.events?.length ? (
                      <div className="space-y-3">
                        {trace.events.map((event, index) => (
                          <pre
                            className="rounded border border-line bg-background p-3 text-xs text-muted"
                            key={index}
                          >
                            {JSON.stringify(event, null, 2)}
                          </pre>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-muted">
                        No workflow events recorded yet.
                      </p>
                    )}
                  </Panel>
                </div>
              ) : null}

              {section === "rejected" ? (
                <div className="space-y-6">
                  <div className="flex flex-wrap items-center justify-between gap-4">
                    <Badge tone={rejected.length ? "warning" : "muted"}>
                      {rejected.length} rejected messages
                    </Badge>
                    <Search
                      value={search}
                      onChange={setSearch}
                      label="Search rejected messages"
                    />
                  </div>
                  {currentRejections.length ? (
                    currentRejections.map((record, index) => (
                      <Panel
                        title={`Message ${record.message_index || index + 1} · ${record.sender}`}
                        key={`${record.timestamp}-${index}`}
                        action={
                          <Badge tone="danger">{record.target_area}</Badge>
                        }
                      >
                        <div className="space-y-4">
                          <p className="text-xs text-muted">
                            {time(record.timestamp)}
                            {record.source_reference
                              ? ` · Source: ${record.source_reference}`
                              : ""}
                          </p>
                          <blockquote className="rounded-lg border border-line bg-background p-4 text-sm">
                            {record.raw_text}
                          </blockquote>
                          <div className="rounded-lg border border-danger/25 bg-danger/5 p-4">
                            <p className="mb-2 text-xs font-semibold text-danger">
                              Reason for rejection
                            </p>
                            <p className="text-sm">{record.rejection_reason}</p>
                          </div>
                          <div className="flex items-center gap-2 text-xs text-success">
                            <Icon name="shield" size={16} />
                            The active plan was preserved when this update was
                            rejected.
                          </div>
                        </div>
                      </Panel>
                    ))
                  ) : (
                    <Panel title="Conflict audit">
                      <Empty
                        title={
                          search
                            ? "No matching rejections"
                            : "No rejected messages"
                        }
                        text="Conflicting messages will appear here with their original text, affected area, and rejection reason."
                      />
                    </Panel>
                  )}
                </div>
              ) : null}

              {section === "history" ? (
                <div className="space-y-6">
                  <div className="grid gap-4 lg:grid-cols-3">
                    {(["json", "markdown", "trace"] as const).map((format) => (
                      <div key={format} className="panel p-6">
                        <Icon
                          name={format === "trace" ? "trace" : "download"}
                          className="mb-4 text-accent"
                          size={24}
                        />
                        <h2 className="font-semibold">
                          {format === "json"
                            ? "Complete JSON artifact"
                            : format === "markdown"
                              ? "Human-readable report"
                              : "Full model trace"}
                        </h2>
                        <p className="mb-5 mt-2 text-xs text-muted">
                          {format === "json"
                            ? "Current plan, checks, source facts, and audit history."
                            : format === "markdown"
                              ? "Share a readable plan and validation summary."
                              : "Exact model calls and provider-reported token usage."}
                        </p>
                        <button
                          className="btn w-full"
                          disabled={!hasPlan || !!busy}
                          onClick={() =>
                            void action("Exporting artifact", async () => {
                              await downloadExport(format);
                              notify("Export downloaded.");
                            })
                          }
                        >
                          <Icon name="download" size={15} />
                          Download{" "}
                          {format === "markdown"
                            ? "report"
                            : format.toUpperCase()}
                        </button>
                      </div>
                    ))}
                  </div>
                  <Panel
                    title="Plan versions"
                    subtitle="Accepted plans are persisted; rejected updates do not replace a valid version."
                    noPadding
                  >
                    <Table
                      headers={[
                        "Version",
                        "Saved",
                        "Change summary",
                        "Status",
                        "Review",
                      ]}
                      rows={history.map((version, index) => {
                        const id = String(
                          field(version, "id", "version", "version_id") ??
                            index + 1,
                        );
                        return [
                          id,
                          time(
                            field(
                              version,
                              "created_at",
                              "timestamp",
                              "last_updated",
                            ),
                          ),
                          display(
                            field(
                              version,
                              "summary",
                              "change_summary",
                              "message",
                              "reason",
                            ) || "Plan snapshot",
                          ),
                          <Badge key="status">
                            {display(field(version, "status") || "Saved")}
                          </Badge>,
                          <button
                            key="view"
                            className="text-xs text-accent"
                            onClick={() =>
                              void action("Loading plan version", async () => {
                                const snapshot = await api<JsonRecord>(
                                  `/history/${encodeURIComponent(id)}`,
                                );
                                setSelectedVersion(snapshot);
                                setSelectedVersionId(id);
                              })
                            }
                          >
                            Compare with current
                          </button>,
                        ];
                      })}
                    />
                  </Panel>
                  <Panel
                    title="Rejection history"
                    subtitle="Retained alongside the active event plan"
                    noPadding
                  >
                    <Table
                      headers={["Timestamp", "Sender", "Area", "Reason"]}
                      rows={rejected.map((record) => [
                        time(record.timestamp),
                        record.sender,
                        record.target_area,
                        record.rejection_reason,
                      ])}
                    />
                  </Panel>
                </div>
              ) : null}

              {section === "whatsapp" ? (
                <div className="space-y-6">
                  <Panel
                    title="WhatsApp connection"
                    subtitle="Credentials remain on the backend."
                    action={
                      <button
                        className="btn"
                        disabled={!!busy}
                        onClick={() =>
                          void action(
                            "Verifying provider connection",
                            async () => {
                              const result = await api<WhatsAppStatus>(
                                "/whatsapp/status/verify",
                                { method: "POST" },
                              );
                              setWaStatus(result);
                              notify(
                                result.connected
                                  ? "Provider connection verified. No messages were sent."
                                  : "Provider did not confirm a connection. Review configuration blockers.",
                                result.connected ? "success" : "info",
                              );
                            },
                          )
                        }
                      >
                        <Icon name="refresh" size={15} />
                        Verify connection
                      </button>
                    }
                  >
                    <div className="grid gap-5 sm:grid-cols-3">
                      <div>
                        <p className="text-xs text-muted">Detected provider</p>
                        <p className="mt-2 font-semibold">
                          {waStatus?.provider || "Not loaded"}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted">Connection state</p>
                        <div className="mt-2">
                          <Badge
                            tone={waStatus?.connected ? "success" : "warning"}
                          >
                            {waStatus?.connection_state || "Not verified"}
                          </Badge>
                        </div>
                      </div>
                      <div>
                        <p className="text-xs text-muted">Sending mode</p>
                        <div className="mt-2">
                          <Badge tone={waStatus?.live_sending_enabled ? "success" : "accent"}>
                            {waStatus?.live_sending_enabled ? "Live sending enabled" : "Safe preview only"}
                          </Badge>
                        </div>
                      </div>
                    </div>
                    <p className="mt-5 text-xs text-muted">
                      {waStatus?.live_sending_enabled
                        ? "Live sending is enabled on the server. You can send live WhatsApp messages to opted-in recipients or save previews."
                        : "Notifications created here are previews. Live sending is disabled in server configuration. Last verification: " + time(waStatus?.verified_at) + "."}
                    </p>
                    {waStatus?.blockers?.length ? (
                      <ul className="mt-4 space-y-2 rounded border border-warning/20 bg-warning/5 p-4 text-xs text-warning">
                        {waStatus.blockers.map((blocker) => (
                          <li key={blocker}>{blocker}</li>
                        ))}
                      </ul>
                    ) : null}
                    {waStatus?.missing_variables?.length ? (
                      <p className="mt-3 text-xs text-warning">
                        Missing environment variables:{" "}
                        {waStatus.missing_variables.join(", ")}
                      </p>
                    ) : null}
                  </Panel>
                  <div className="grid gap-6 xl:grid-cols-2">
                    <Panel
                      title="Add a recipient"
                      subtitle="Record consent before preparing notifications."
                    >
                      <form
                        onSubmit={(event) => {
                          event.preventDefault();
                          void action("Saving recipient", async () => {
                            await api<Recipient>("/whatsapp/recipients", {
                              method: "POST",
                              body: JSON.stringify({
                                name: recipientName,
                                phone: recipientPhone,
                                opted_in: consent,
                              }),
                            });
                            setRecipientName("");
                            setRecipientPhone("");
                            setConsent(false);
                            await refreshWhatsApp();
                            notify("Recipient saved.");
                          });
                        }}
                        className="space-y-4"
                      >
                        <div>
                          <label
                            className="field-label"
                            htmlFor="recipient-name"
                          >
                            Recipient name
                          </label>
                          <input
                            id="recipient-name"
                            className="field"
                            value={recipientName}
                            onChange={(event) =>
                              setRecipientName(event.target.value)
                            }
                            maxLength={100}
                            required
                          />
                        </div>
                        <div>
                          <label
                            className="field-label"
                            htmlFor="recipient-phone"
                          >
                            Phone number (international format)
                          </label>
                          <input
                            id="recipient-phone"
                            className="field"
                            type="tel"
                            value={recipientPhone}
                            onChange={(event) =>
                              setRecipientPhone(event.target.value)
                            }
                            placeholder="+92…"
                            pattern="\+[1-9][0-9]{7,14}"
                            required
                          />
                        </div>
                        <label className="flex items-start gap-3 text-xs text-muted">
                          <input
                            type="checkbox"
                            className="mt-0.5 accent-blue-500"
                            checked={consent}
                            onChange={(event) =>
                              setConsent(event.target.checked)
                            }
                          />
                          <span>
                            This recipient has explicitly opted in to event
                            notifications.
                          </span>
                        </label>
                        <button type="submit" className="btn" disabled={!!busy}>
                          Save recipient
                        </button>
                      </form>
                    </Panel>
                    <Panel
                      title="Prepare a notification"
                      subtitle="Event, schedule, venue, judge, team, and reminder messages."
                    >
                      <form
                        className="space-y-4"
                        onSubmit={(event) => {
                          event.preventDefault();
                          const isLive = liveSendConfirm && !!waStatus?.live_sending_enabled;
                          void action(
                            isLive
                              ? "Dispatching live WhatsApp notification"
                              : "Preparing safe notification preview",
                            async () => {
                              await api<JsonRecord>("/whatsapp/notifications", {
                                method: "POST",
                                body: JSON.stringify({
                                  recipient_ids: selectedRecipients.map((id) =>
                                    Number.isNaN(Number(id)) ? id : Number(id),
                                  ),
                                  kind: notificationKind,
                                  message: notificationText,
                                  idempotency_key: crypto.randomUUID(),
                                  dry_run: !isLive,
                                  confirm_live_send: isLive,
                                }),
                              });
                              await refreshWhatsApp();
                              notify(
                                isLive
                                  ? "WhatsApp message dispatched."
                                  : "Notification preview saved. No WhatsApp message was sent.",
                              );
                            },
                          );
                        }}
                      >
                        <div>
                          <label
                            className="field-label"
                            htmlFor="notification-kind"
                          >
                            Notification type
                          </label>
                          <select
                            id="notification-kind"
                            className="field"
                            value={notificationKind}
                            onChange={(event) =>
                              setNotificationKind(event.target.value)
                            }
                          >
                            {[
                              "event",
                              "schedule",
                              "venue",
                              "judging",
                              "team",
                              "reminder",
                            ].map((kind) => (
                              <option key={kind}>{kind}</option>
                            ))}
                          </select>
                        </div>
                        <div>
                          <label
                            className="field-label"
                            htmlFor="notification-text"
                          >
                            Message
                          </label>
                          <textarea
                            id="notification-text"
                            className="field min-h-24"
                            value={notificationText}
                            onChange={(event) =>
                              setNotificationText(event.target.value)
                            }
                            maxLength={4096}
                            required
                          />
                        </div>
                        <fieldset>
                          <legend className="field-label">
                            Recipients with consent
                          </legend>
                          <div className="max-h-32 space-y-2 overflow-auto rounded border border-line p-3">
                            {recipients.filter(
                              (recipient) => recipient.opted_in,
                            ).length ? (
                              recipients
                                .filter((recipient) => recipient.opted_in)
                                .map((recipient) => (
                                  <label
                                    key={recipient.id}
                                    className="flex items-center gap-3 text-xs"
                                  >
                                    <input
                                      type="checkbox"
                                      checked={selectedRecipients.includes(
                                        String(recipient.id),
                                      )}
                                      onChange={(event) =>
                                        setSelectedRecipients((current) =>
                                          event.target.checked
                                            ? [...current, String(recipient.id)]
                                            : current.filter(
                                                (id) =>
                                                  id !== String(recipient.id),
                                              ),
                                        )
                                      }
                                    />
                                    {recipient.name}{" "}
                                    <span className="text-muted">
                                      {recipient.phone}
                                    </span>
                                  </label>
                                ))
                            ) : (
                              <p className="text-xs text-muted">
                                Add an opted-in recipient first.
                              </p>
                            )}
                          </div>
                        </fieldset>
                        {waStatus?.live_sending_enabled ? (
                          <label className="flex items-start gap-3 rounded border border-warning/40 bg-warning/10 p-3 text-xs text-warning">
                            <input
                              type="checkbox"
                              className="mt-0.5 accent-blue-500"
                              checked={liveSendConfirm}
                              onChange={(event) =>
                                setLiveSendConfirm(event.target.checked)
                              }
                            />
                            <span>
                              <strong>Live WhatsApp dispatch:</strong> Send real WhatsApp message to selected recipients via the connected bot.
                            </span>
                          </label>
                        ) : null}
                        <button
                          className={`btn ${liveSendConfirm && waStatus?.live_sending_enabled ? "btn-primary font-semibold" : "btn-primary"}`}
                          type="submit"
                          disabled={
                            !!busy ||
                            !selectedRecipients.length ||
                            !notificationText.trim()
                          }
                        >
                          {liveSendConfirm && waStatus?.live_sending_enabled
                            ? "Send live WhatsApp notification"
                            : "Save notification preview"}
                        </button>
                      </form>
                    </Panel>
                  </div>
                  <Panel
                    title="Recipient consent"
                    subtitle="Recipient information is organizer-only."
                    noPadding
                  >
                    <Table
                      headers={["Name", "Phone", "Consent", "Action"]}
                      rows={recipients.map((recipient) => [
                        recipient.name,
                        recipient.phone,
                        <Badge
                          key="consent"
                          tone={recipient.opted_in ? "success" : "muted"}
                        >
                          {recipient.opted_in ? "Opted in" : "Opted out"}
                        </Badge>,
                        <button
                          key="action"
                          className="text-xs text-accent"
                          disabled={!!busy}
                          onClick={() =>
                            void action("Updating consent", async () => {
                              await api<Recipient>(
                                `/whatsapp/recipients/${recipient.id}`,
                                {
                                  method: "PATCH",
                                  body: JSON.stringify({
                                    opted_in: !recipient.opted_in,
                                  }),
                                },
                              );
                              setSelectedRecipients((current) =>
                                current.filter(
                                  (id) => id !== String(recipient.id),
                                ),
                              );
                              await refreshWhatsApp();
                              notify("Recipient consent updated.");
                            })
                          }
                        >
                          {recipient.opted_in
                            ? "Record opt-out"
                            : "Record opt-in"}
                        </button>,
                      ])}
                    />
                  </Panel>
                  <Panel title="Notification and delivery log" noPadding>
                    <Table
                      headers={[
                        "Created",
                        "Recipient",
                        "Type",
                        "Message",
                        "Status / error",
                      ]}
                      rows={notifications.map((notification) => [
                        time(field(notification, "created_at", "timestamp")),
                        display(
                          field(
                            notification,
                            "recipient_name",
                            "phone",
                            "recipient_id",
                          ),
                        ),
                        display(field(notification, "kind", "type")),
                        <p
                          key="message"
                          className="max-w-lg text-xs text-muted"
                        >
                          {display(
                            field(notification, "message", "body", "text"),
                          )}
                        </p>,
                        <div key="status">
                          <Badge
                            tone={
                              field(notification, "status", "delivery_status") === "submitted" ||
                              field(notification, "status", "delivery_status") === "sent" ||
                              field(notification, "status", "delivery_status") === "delivered" ||
                              field(notification, "status", "delivery_status") === "read"
                                ? "success"
                                : field(notification, "status", "delivery_status") === "failed"
                                ? "danger"
                                : field(notification, "status", "delivery_status") === "preview"
                                ? "accent"
                                : "muted"
                            }
                          >
                            {display(
                              field(notification, "status", "delivery_status"),
                            )}
                          </Badge>
                          {notification.error ? (
                            <p className="mt-2 text-xs text-danger">
                              {display(notification.error)}
                            </p>
                          ) : null}
                        </div>,
                      ])}
                    />
                  </Panel>
                  <div className="grid gap-6 xl:grid-cols-2">
                    <Panel title="Provider templates">
                      <p className="text-xs text-muted">
                        {display(
                          templates.reason ||
                            "Template support depends on the configured provider and account permissions.",
                        )}
                      </p>
                      {asArray(templates.templates).map((template, index) => (
                        <pre className="mt-3 text-xs" key={index}>
                          {JSON.stringify(template, null, 2)}
                        </pre>
                      ))}
                    </Panel>
                    <Panel title="Webhook event history">
                      <div className="max-h-80 space-y-3 overflow-auto">
                        {webhooks.length ? (
                          webhooks.map((event, index) => (
                            <pre
                              className="rounded border border-line bg-background p-3 text-xs text-muted"
                              key={index}
                            >
                              {JSON.stringify(event, null, 2)}
                            </pre>
                          ))
                        ) : (
                          <p className="text-xs text-muted">
                            No webhook events received. Inbound events require a
                            reachable provider webhook and valid signature.
                          </p>
                        )}
                      </div>
                    </Panel>
                  </div>
                </div>
              ) : null}
            </>
          )}
          <footer className="mt-10 flex flex-wrap justify-between gap-2 border-t border-line pt-5 text-[10px] text-muted">
            <span>HackPlan AI · Mind to Machine</span>
            <span>
              Local workspace · Source-backed planning · Transparent execution
            </span>
          </footer>
        </main>
      </div>

      {toast ? (
        <div
          role={toast.kind === "error" ? "alert" : "status"}
          className={`toast panel flex items-start gap-3 border-l-4 p-4 ${toast.kind === "error" ? "border-l-danger" : toast.kind === "info" ? "border-l-accent" : "border-l-success"}`}
        >
          <Icon
            name={toast.kind === "error" ? "rejected" : "check"}
            className={toast.kind === "error" ? "text-danger" : "text-accent"}
          />
          <p className="flex-1 text-sm">{toast.text}</p>
          <button
            aria-label="Dismiss notification"
            className="text-muted"
            onClick={() => setToast(null)}
          >
            <Icon name="close" size={16} />
          </button>
        </div>
      ) : null}
      {confirmRun ? (
        <Modal
          title={
            hasPlan ? "Generate a new baseline plan?" : "Generate event plan"
          }
          onClose={() => setConfirmRun(null)}
          footer={
            <>
              <button className="btn" onClick={() => setConfirmRun(null)}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={() => void runPack(confirmRun)}
              >
                Generate plan
              </button>
            </>
          }
        >
          <p className="text-sm text-muted">
            {confirmRun === "sample"
              ? "Process the official sample_pack.txt file from the repository."
              : `Process ${packName || "the pasted message pack"} exactly as supplied.`}{" "}
            {hasPlan
              ? "This starts a new baseline; saved plan versions remain available in history."
              : "The backend will extract facts and validate all five planning domains."}
          </p>
          <p className="mt-4 text-xs text-accent">
            Mode:{" "}
            {mode === "offline"
              ? "Offline parser — no model calls"
              : mode === "provider"
                ? "Configured live AI provider required"
                : "Automatic provider selection"}
            . This action never sends WhatsApp messages.
          </p>
        </Modal>
      ) : null}
      {showAccess ? (
        <Modal
          title="Organizer access"
          onClose={() => setShowAccess(false)}
          footer={
            <button
              className="btn btn-primary"
              onClick={() => {
                setOrganizerKey(accessKey);
                setShowAccess(false);
                void refresh();
                if (section === "whatsapp") void refreshWhatsApp();
                notify(
                  "Organizer key applied to this browser session.",
                  "info",
                );
              }}
            >
              Apply access key
            </button>
          }
        >
          <p className="mb-4 text-xs text-muted">
            If ORGANIZER_API_KEY is enabled on your backend, enter it here. It
            is held in memory and sent only to your local API. Leave empty when
            local access does not require a key.
          </p>
          <label htmlFor="organizer-key" className="field-label">
            Organizer access key
          </label>
          <input
            id="organizer-key"
            type="password"
            className="field"
            value={accessKey}
            onChange={(event) => setAccessKey(event.target.value)}
            autoComplete="off"
          />
        </Modal>
      ) : null}
      {selectedVersion ? (
        <Modal
          title={`Compare version ${selectedVersionId}`}
          onClose={() => setSelectedVersion(null)}
        >
          <VersionComparison snapshot={selectedVersion} current={plan} />
        </Modal>
      ) : null}
      {process.env.NODE_ENV === "development" &&
      process.env.NEXT_PUBLIC_ENABLE_AGENTATION === "true" ? (
        <Agentation />
      ) : null}
    </>
  );
}

function Search({
  value,
  onChange,
  label,
}: {
  value: string;
  onChange: (value: string) => void;
  label: string;
}) {
  return (
    <div className="relative">
      <Icon
        name="search"
        size={14}
        className="pointer-events-none absolute left-3 top-3.5 text-muted"
      />
      <input
        aria-label={label}
        className="field max-w-60 py-2 pl-9 text-xs"
        placeholder={label}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </div>
  );
}
function DomainConstraints({
  area,
  constraints,
}: {
  area: string;
  constraints: JsonRecord[];
}) {
  const relevant = constraints.filter((constraint) =>
    String(field(constraint, "area", "planning_area", "domain") || "").includes(
      area,
    ),
  );
  return (
    <Panel
      title="Source constraints"
      subtitle={`Rules affecting ${area}`}
      noPadding
    >
      <Table
        headers={["Rule", "Source", "Status"]}
        rows={relevant.map((constraint) => [
          display(
            field(
              constraint,
              "description",
              "text",
              "constraint_type",
              "type",
            ) || constraint,
          ),
          display(
            field(
              constraint,
              "source_message",
              "source_message_id",
              "source",
              "source_reference",
            ),
          ),
          <Badge
            key="status"
            tone={
              field(constraint, "status", "effective_status") === "unresolved"
                ? "warning"
                : "muted"
            }
          >
            {display(
              field(constraint, "status", "effective_status") || "Active",
            )}
          </Badge>,
        ])}
      />
    </Panel>
  );
}
function VersionComparison({
  snapshot,
  current,
}: {
  snapshot: JsonRecord;
  current: Plan | null;
}) {
  const previous = (snapshot.plan ||
    (snapshot.snapshot && typeof snapshot.snapshot === "object"
      ? (snapshot.snapshot as JsonRecord).plan
      : null) ||
    snapshot) as unknown as Plan;
  const rows: [string, unknown, unknown][] = [
    ["Venue", previous.venue?.selected_room, current?.venue.selected_room],
    ["Venue cost", previous.venue?.cost, current?.venue.cost],
    ["Meal count", previous.food?.headcount, current?.food.headcount],
    ["Food cost", previous.food?.total_cost, current?.food.total_cost],
    [
      "Judges",
      previous.judging?.confirmed_judges,
      current?.judging.confirmed_judges,
    ],
    [
      "Event hours",
      previous.schedule?.total_duration_hours,
      current?.schedule.total_duration_hours,
    ],
    [
      "Planned expenditure",
      previous.budget?.total_projected,
      current?.budget.total_projected,
    ],
    [
      "Remaining budget",
      previous.budget?.surplus_deficit,
      current?.budget.surplus_deficit,
    ],
  ];
  return (
    <div>
      <p className="mb-4 text-xs text-muted">
        Changed values are highlighted. The current plan stays active.
      </p>
      <Table
        headers={["Field", "Selected version", "Current"]}
        rows={rows.map(([label, before, after]) => [
          label,
          display(before),
          <span
            key="after"
            className={before !== after ? "font-semibold text-accent" : ""}
          >
            {display(after)}
          </span>,
        ])}
      />
      <details className="mt-5">
        <summary className="text-xs text-accent">
          View full saved version
        </summary>
        <pre className="mt-3 max-h-96 overflow-auto rounded border border-line bg-background p-3 text-[11px] text-muted">
          {JSON.stringify(snapshot, null, 2)}
        </pre>
      </details>
    </div>
  );
}
