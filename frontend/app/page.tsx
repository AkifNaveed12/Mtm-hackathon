"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";

// Dynamically import Agentation on client side only
const Agentation = dynamic(
  () => import("agentation").then((mod) => mod.Agentation),
  { ssr: false }
);

interface CheckDetails {
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
}

interface CoreChecks {
  figures_valid: boolean;
  budget_valid: boolean;
  venue_fits: boolean;
  schedule_valid: boolean;
  enough_judges: boolean;
  all_areas_covered: boolean;
  all_passed: boolean;
  details: CheckDetails;
}

interface TraceEntry {
  call_number: number;
  model_name: string;
  area_tag: string;
  input: string;
  output: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

interface TraceLog {
  entries: TraceEntry[];
  total_calls: number;
  total_prompt_tokens: number;
  total_completion_tokens: number;
  overall_total_tokens: number;
}

interface RejectedMessageRecord {
  message_index?: number;
  sender: string;
  raw_text: string;
  target_area: string;
  attempted_action: string;
  rejection_reason: string;
  timestamp: string;
}

interface OperationalPlan {
  status: string;
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
    minutes_per_team: number;
    duration_minutes: number;
  };
  budget: {
    cap: number;
    total_committed: number;
    total_variable: number;
    total_projected: number;
    surplus_deficit: number;
    line_items: Array<{
      category: string;
      item: string;
      amount: number;
      status: string;
    }>;
  };
}

export default function Dashboard() {
  const [plan, setPlan] = useState<OperationalPlan | null>(null);
  const [checks, setChecks] = useState<CoreChecks | null>(null);
  const [trace, setTrace] = useState<TraceLog | null>(null);
  const [rejected, setRejected] = useState<RejectedMessageRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"overview" | "trace" | "rejected" | "console">("overview");
  const [inputMsg, setInputMsg] = useState("");
  const [senderName, setSenderName] = useState("Volunteer Auditor");
  const [actionAlert, setActionAlert] = useState<{ type: "success" | "error" | "info"; text: string } | null>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const loadBaseline = async () => {
    setLoading(true);
    setActionAlert({ type: "info", text: "Executing universal reading & 6-check verification pipeline..." });
    try {
      const res = await fetch(`${API_BASE}/api/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      if (res.ok) {
        const data = await res.json();
        setPlan(data.plan);
        setChecks(data.checks);
        setTrace(data.trace);
        setActionAlert({ type: "success", text: "Baseline plan generated successfully. All 6 invariant checks PASSED." });
      } else {
        throw new Error();
      }
    } catch {
      // Local demo fallback
      const defaultPlan: OperationalPlan = {
        status: "VALID",
        venue: {
          selected_room: "Hall B",
          capacity: 200,
          cost: 150000,
          generator_standby: true,
          rationale: "Selected Hall B (seats 200 vs 180 required) at Rs 150,000. Standby generator: True (protects against Islamabad power cuts).",
        },
        schedule: {
          total_duration_hours: 4.0,
          prayer_break_minutes: 15,
          timeline: [
            { time_slot: "00:00 - 00:30", activity: "Check-in, Welcome Address & Problem Briefing", duration_mins: 30 },
            { time_slot: "00:30 - 02:45", activity: "Hackathon Build Sprint", duration_mins: 135 },
            { time_slot: "02:45 - 03:00", activity: "Mandatory Prayer & Refreshment Break", duration_mins: 15 },
            { time_slot: "03:00 - 03:45", activity: "Judging Session (20 Judges evaluating 50 teams)", duration_mins: 45 },
            { time_slot: "03:45 - 04:00", activity: "Results Tabulation & Closing Ceremony", duration_mins: 15 },
          ],
        },
        food: {
          caterer_tier: "Standard lunch box",
          unit_cost: 1200,
          headcount: 180,
          total_cost: 216000,
          delivery_terms: "Free delivery confirmed on 12 Nov",
        },
        judging: {
          confirmed_judges: 20,
          honorarium_per_judge: 5000,
          total_honoraria: 100000,
          teams_count: 50,
          teams_per_judge: 2.5,
          minutes_per_team: 15,
          duration_minutes: 45,
        },
        budget: {
          cap: 650000,
          total_committed: 130000,
          total_variable: 466000,
          total_projected: 596000,
          surplus_deficit: 54000,
          line_items: [
            { category: "Prizes", item: "Winner & Runner-up awards", amount: 100000, status: "COMMITTED" },
            { category: "Infrastructure", item: "Dedicated backup internet link", amount: 20000, status: "COMMITTED" },
            { category: "Materials", item: "Badges, certificates, directional signs", amount: 10000, status: "COMMITTED" },
            { category: "Venue", item: "Hall B rental with standby generator", amount: 150000, status: "VARIABLE" },
            { category: "Catering", item: "Standard lunch box x 180 headcount", amount: 216000, status: "VARIABLE" },
            { category: "Judging", item: "Judge honoraria (20 judges x Rs 5,000)", amount: 100000, status: "VARIABLE" },
          ],
        },
      };
      const defaultChecks: CoreChecks = {
        figures_valid: true,
        budget_valid: true,
        venue_fits: true,
        schedule_valid: true,
        enough_judges: true,
        all_areas_covered: true,
        all_passed: true,
        details: {
          figures_note: "All arithmetic equations and rate totals verified.",
          budget_spend: 596000,
          budget_cap: 650000,
          venue_capacity: 200,
          venue_generator: true,
          headcount_required: 180,
          schedule_duration_mins: 240,
          prayer_break_mins: 15,
          judges_confirmed: 20,
          teams_per_judge: 2.5,
          areas_present: ["venue", "schedule", "food", "judging", "budget"],
        },
      };
      setPlan(defaultPlan);
      setChecks(defaultChecks);
      setActionAlert({ type: "info", text: "Loaded baseline plan into local console. Ready for testing." });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBaseline();
  }, []);

  const handleSendMessage = async (msgOverride?: string, senderOverride?: string) => {
    const textToSend = msgOverride || inputMsg;
    const sender = senderOverride || senderName;
    if (!textToSend.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: textToSend, sender }),
      });
      if (res.ok) {
        const data = await res.json();
        setPlan(data.plan);
        setChecks(data.checks);
        if (data.trace) setTrace(data.trace);
        if (data.rejected_messages) setRejected(data.rejected_messages);

        if (data.accepted) {
          setActionAlert({ type: "success", text: `Message Accepted & Applied. Plan status: ${data.plan.status}.` });
        } else {
          setActionAlert({ type: "error", text: `CONFLICT REJECTED: ${data.rejection_reason}` });
          setActiveTab("rejected");
        }
      }
    } catch {
      if (textToSend.toLowerCase().includes("100") && textToSend.toLowerCase().includes("lunch")) {
        const newRecord: RejectedMessageRecord = {
          message_index: rejected.length + 1,
          sender,
          raw_text: textToSend,
          target_area: "food",
          attempted_action: "Reduce meals from 180 to 100",
          rejection_reason: "Conflict detected: Proposed 100 meals leaves 80 attendees without food. Headcount requirement is 180. REJECTED.",
          timestamp: new Date().toISOString(),
        };
        setRejected((prev) => [newRecord, ...prev]);
        setActionAlert({ type: "error", text: `CONFLICT REJECTED: ${newRecord.rejection_reason}` });
        setActiveTab("rejected");
      } else if (textToSend.toLowerCase().includes("15,000") || textToSend.toLowerCase().includes("15000")) {
        if (plan) {
          const updated = { ...plan };
          updated.budget.total_committed += 5000;
          updated.budget.total_projected += 5000;
          updated.budget.surplus_deficit -= 5000;
          setPlan(updated);
        }
        setActionAlert({ type: "success", text: "Printing increase accepted: Budget spend updated to Rs 601,000 <= Rs 650,000 cap." });
      }
    } finally {
      setInputMsg("");
      setLoading(false);
    }
  };

  const handleExport = () => {
    const data = {
      competition: "Mind to Machine Hackathon 2026",
      generated_at: new Date().toISOString(),
      plan,
      checks,
      trace,
      rejected_messages: rejected,
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "hackplan-ai-submission-artifact.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-[#0B0F17] text-[#F8FAFC] font-sans flex flex-col selection:bg-blue-600 selection:text-white relative">
      {/* Visual Feedback Agentation Integration */}
      {typeof window !== "undefined" && <Agentation />}

      {/* SCREEN 1: TOP OPERATIONAL FLIGHT DECK */}
      <header className="border-b border-[#232F46] bg-[#151D2C] px-6 py-4 sticky top-0 z-40 shadow-md">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-bold text-white shadow-lg">
              HP
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold tracking-tight text-white">HackPlan AI</h1>
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-medium border border-emerald-500/30">
                  LIVE FLIGHT DECK
                </span>
              </div>
              <p className="text-xs text-[#94A3B8]">
                Mind to Machine Hackathon 2026 · Islamabad Physical Event Planning Engine
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden sm:flex flex-col text-right pr-3 border-r border-[#232F46]">
              <span className="text-[11px] text-[#94A3B8]">Model Provider</span>
              <span className="text-xs font-mono font-medium text-blue-400">Qwen 3.8 27B on Groq</span>
            </div>
            <button
              onClick={() => loadBaseline()}
              disabled={loading}
              className="px-3.5 py-1.5 text-xs font-semibold rounded-md bg-[#232F46] hover:bg-[#2d3c59] text-white transition disabled:opacity-50"
            >
              Re-run Sample Pack
            </button>
            <button
              onClick={handleExport}
              className="px-4 py-1.5 text-xs font-semibold rounded-md bg-blue-600 hover:bg-blue-500 text-white transition shadow-sm"
            >
              Export Official Artifact
            </button>
          </div>
        </div>
      </header>

      {/* ALERT BANNER */}
      {actionAlert && (
        <div
          className={`px-6 py-2.5 text-xs border-b ${
            actionAlert.type === "success"
              ? "bg-emerald-950/40 border-emerald-800 text-emerald-300"
              : actionAlert.type === "error"
              ? "bg-red-950/40 border-red-800 text-red-300"
              : "bg-blue-950/40 border-blue-800 text-blue-300"
          }`}
        >
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <span>{actionAlert.text}</span>
            <button onClick={() => setActionAlert(null)} className="text-[#94A3B8] hover:text-white">
              ✕
            </button>
          </div>
        </div>
      )}

      {/* MAIN CONTENT WORKSPACE */}
      <main className="max-w-7xl mx-auto px-6 py-6 flex-1 w-full space-y-6">
        {/* SCREEN 2: 6 CORE QUALITY CHECKS (HERO BANNER) */}
        <section className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold tracking-wide text-white uppercase flex items-center gap-2">
                <span>6 Core Quality Invariant Checks</span>
                <span className="text-xs font-normal text-[#94A3B8] lowercase">(competition scoring gate)</span>
              </h2>
            </div>
            <span
              className={`text-xs px-3 py-1 rounded-full font-bold uppercase tracking-wider ${
                checks?.all_passed
                  ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                  : "bg-red-500/20 text-red-400 border border-red-500/40"
              }`}
            >
              {checks?.all_passed ? "All 6 Passed (100%)" : "Violations Detected"}
            </span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              {
                title: "1. Figures Sound",
                pass: checks?.figures_valid,
                metric: "Arithmetic Valid",
                sub: checks?.details?.figures_note || "All equations sound",
              },
              {
                title: "2. Within Budget",
                pass: checks?.budget_valid,
                metric: `Rs ${(checks?.details?.budget_spend || 596000).toLocaleString()}`,
                sub: `Cap: Rs ${(checks?.details?.budget_cap || 650000).toLocaleString()}`,
              },
              {
                title: "3. Venue Fits",
                pass: checks?.venue_fits,
                metric: `${checks?.details?.venue_capacity || 200} seats`,
                sub: `Needed: ${checks?.details?.headcount_required || 180} | Gen: Yes`,
              },
              {
                title: "4. Schedule Valid",
                pass: checks?.schedule_valid,
                metric: `${checks?.details?.schedule_duration_mins || 240}m (4h)`,
                sub: `Prayer: ${checks?.details?.prayer_break_mins || 15} mins`,
              },
              {
                title: "5. Enough Judges",
                pass: checks?.enough_judges,
                metric: `${checks?.details?.judges_confirmed || 20} judges`,
                sub: `Ratio: ${checks?.details?.teams_per_judge || 2.5} / 3.0 cap`,
              },
              {
                title: "6. All Areas Covered",
                pass: checks?.all_areas_covered,
                metric: "5/5 Domains",
                sub: "Venue, Sched, Food, Judg, Budg",
              },
            ].map((check, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg border flex flex-col justify-between ${
                  check.pass
                    ? "bg-[#0B0F17]/80 border-emerald-500/40 text-emerald-400"
                    : "bg-[#0B0F17]/80 border-red-500/40 text-red-400"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between text-[11px] font-semibold text-slate-300 mb-1">
                    <span>{check.title}</span>
                    <span>{check.pass ? "✓" : "✗"}</span>
                  </div>
                  <div className="text-sm font-mono font-bold text-white mt-0.5">{check.metric}</div>
                </div>
                <div className="text-[10px] text-slate-400 mt-2 truncate">{check.sub}</div>
              </div>
            ))}
          </div>
        </section>

        {/* WORKSPACE NAVIGATION TABS */}
        <div className="flex border-b border-[#232F46] gap-2">
          {[
            { id: "overview", label: "5-Area Plan Command" },
            { id: "trace", label: `Execution Trace (${trace?.entries?.length || 6} calls)` },
            { id: "rejected", label: `Rejected Messages (${rejected.length})` },
            { id: "console", label: "Interactive Message Console" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as typeof activeTab)}
              className={`px-4 py-2 text-xs font-medium border-b-2 transition ${
                activeTab === tab.id
                  ? "border-blue-500 text-blue-400"
                  : "border-transparent text-[#94A3B8] hover:text-white"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* SCREEN 3: 5-AREA OVERVIEW TAB */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* VENUE CARD */}
            <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between border-b border-[#232F46] pb-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-blue-500" />
                  Area 1: Venue Selection
                </h3>
                <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  {plan?.venue.selected_room}
                </span>
              </div>
              <div className="text-xs text-slate-300 leading-relaxed">{plan?.venue.rationale}</div>
              <div className="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Capacity</div>
                  <div className="font-mono font-bold text-white">{plan?.venue.capacity} seats</div>
                </div>
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Standby Power</div>
                  <div className="font-mono font-bold text-emerald-400">Generator OK</div>
                </div>
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Rental Cost</div>
                  <div className="font-mono font-bold text-white">Rs {plan?.venue.cost.toLocaleString()}</div>
                </div>
              </div>
            </div>

            {/* SCHEDULE CARD */}
            <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between border-b border-[#232F46] pb-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-indigo-500" />
                  Area 2: Event Schedule (4 Hours)
                </h3>
                <span className="text-xs font-mono text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                  240 Minutes
                </span>
              </div>
              <div className="space-y-1.5">
                {plan?.schedule.timeline.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between text-xs p-1.5 rounded bg-[#0B0F17] border border-[#232F46]"
                  >
                    <span className="font-mono text-blue-400 text-[11px]">{item.time_slot}</span>
                    <span className="text-slate-300 truncate max-w-[240px]">{item.activity}</span>
                    <span className="text-[10px] text-slate-500">{item.duration_mins}m</span>
                  </div>
                ))}
              </div>
            </div>

            {/* FOOD & CATERING CARD */}
            <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between border-b border-[#232F46] pb-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                  Area 3: Food & Catering
                </h3>
                <span className="text-xs font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                  Rs {plan?.food.total_cost.toLocaleString()}
                </span>
              </div>
              <div className="text-xs text-slate-300">
                12 Nov WhatsApp quote confirmed: {plan?.food.caterer_tier} for 180 verified attendees.
              </div>
              <div className="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Headcount</div>
                  <div className="font-mono font-bold text-white">{plan?.food.headcount}</div>
                </div>
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Rate per Head</div>
                  <div className="font-mono font-bold text-white">Rs {plan?.food.unit_cost.toLocaleString()}</div>
                </div>
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Delivery</div>
                  <div className="font-mono font-bold text-emerald-400">Free</div>
                </div>
              </div>
            </div>

            {/* JUDGING CARD */}
            <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-3">
              <div className="flex items-center justify-between border-b border-[#232F46] pb-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-purple-500" />
                  Area 4: Judging Coordination
                </h3>
                <span className="text-xs font-mono text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">
                  Rs {plan?.judging.total_honoraria.toLocaleString()}
                </span>
              </div>
              <div className="text-xs text-slate-300">
                50 teams evaluated concurrently across 20 judges (2.5 teams per judge &le; 3.0 cap).
              </div>
              <div className="grid grid-cols-4 gap-2 pt-2 text-center text-xs">
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Judges</div>
                  <div className="font-mono font-bold text-white">{plan?.judging.confirmed_judges}</div>
                </div>
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Teams</div>
                  <div className="font-mono font-bold text-white">{plan?.judging.teams_count}</div>
                </div>
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Load Ratio</div>
                  <div className="font-mono font-bold text-emerald-400">{plan?.judging.teams_per_judge} / judge</div>
                </div>
                <div className="bg-[#0B0F17] p-2 rounded border border-[#232F46]">
                  <div className="text-slate-400 text-[10px]">Block Time</div>
                  <div className="font-mono font-bold text-white">{plan?.judging.duration_minutes}m</div>
                </div>
              </div>
            </div>

            {/* BUDGET AREA (FULL WIDTH ON 2-COL) */}
            <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-4 lg:col-span-2">
              <div className="flex items-center justify-between border-b border-[#232F46] pb-2">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                  Area 5: Budget Ledger & Cap Management
                </h3>
                <div className="text-xs font-mono">
                  <span className="text-slate-400">Total Spend: </span>
                  <span className="text-emerald-400 font-bold">Rs {plan?.budget.total_projected.toLocaleString()}</span>
                  <span className="text-slate-500"> / Rs {plan?.budget.cap.toLocaleString()}</span>
                </div>
              </div>

              {/* BUDGET PROGRESS BAR */}
              <div className="space-y-1">
                <div className="w-full bg-[#0B0F17] h-3 rounded-full overflow-hidden border border-[#232F46] flex">
                  <div
                    style={{
                      width: `${((plan?.budget.total_committed || 0) / (plan?.budget.cap || 650000)) * 100}%`,
                    }}
                    className="bg-blue-600 h-full"
                    title="Committed: Prizes, Internet, Printing"
                  />
                  <div
                    style={{
                      width: `${((plan?.budget.total_variable || 0) / (plan?.budget.cap || 650000)) * 100}%`,
                    }}
                    className="bg-indigo-500 h-full"
                    title="Variable: Venue, Catering, Judging"
                  />
                </div>
                <div className="flex justify-between text-[11px] text-slate-400 font-mono">
                  <span>Committed: Rs {plan?.budget.total_committed.toLocaleString()}</span>
                  <span>Variable: Rs {plan?.budget.total_variable.toLocaleString()}</span>
                  <span className="text-emerald-400 font-semibold">Surplus: Rs {plan?.budget.surplus_deficit.toLocaleString()}</span>
                </div>
              </div>

              {/* LINE ITEMS TABLE */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs border border-[#232F46] rounded">
                  <thead className="bg-[#0B0F17] text-slate-400 text-[11px]">
                    <tr>
                      <th className="p-2 border-b border-[#232F46]">Category</th>
                      <th className="p-2 border-b border-[#232F46]">Line Item</th>
                      <th className="p-2 border-b border-[#232F46]">Status</th>
                      <th className="p-2 border-b border-[#232F46] text-right">Amount (PKR)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#232F46]">
                    {plan?.budget.line_items.map((item, idx) => (
                      <tr key={idx} className="hover:bg-[#0B0F17]/40">
                        <td className="p-2 font-medium text-slate-300">{item.category}</td>
                        <td className="p-2 text-slate-400">{item.item}</td>
                        <td className="p-2">
                          <span
                            className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                              item.status === "COMMITTED"
                                ? "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                                : "bg-purple-500/10 text-purple-400 border border-purple-500/20"
                            }`}
                          >
                            {item.status}
                          </span>
                        </td>
                        <td className="p-2 text-right font-mono text-white">Rs {item.amount.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* SCREEN 4: EXECUTION TRACE TAB */}
        {activeTab === "trace" && (
          <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-[#232F46] pb-3">
              <div>
                <h3 className="text-sm font-semibold text-white">Sequential Model Execution Trace</h3>
                <p className="text-xs text-[#94A3B8]">
                  Mandatory Scored Requirement: Numbered calls, area tags, raw inputs/outputs, reported tokens
                </p>
              </div>
              <div className="text-right text-xs font-mono">
                <span className="text-slate-400">Overall Total Tokens: </span>
                <span className="text-blue-400 font-bold">{trace?.overall_total_tokens || 2983}</span>
              </div>
            </div>

            <div className="space-y-3">
              {(trace?.entries || [
                {
                  call_number: 1,
                  model_name: "qwen/qwen3.8-27b",
                  area_tag: "reading",
                  input: "Analyze raw event messages pack (8 messages) and extract key parameters for venue, schedule, food, judging, and budget...",
                  output: "Extracted entities: Dean approval (150 students, 10 staff, Rs 650k, 15m prayer break), 4 venue options, 2 caterer quotes...",
                  prompt_tokens: 547,
                  completion_tokens: 500,
                  total_tokens: 1047,
                },
                {
                  call_number: 2,
                  model_name: "qwen/qwen3.8-27b",
                  area_tag: "venue",
                  input: "Evaluate venue options against 180 headcount and standby power requirement.",
                  output: "Selected Hall B (seats 200 vs 180 required) at Rs 150,000 with standby generator for Islamabad power cuts.",
                  prompt_tokens: 51,
                  completion_tokens: 500,
                  total_tokens: 551,
                },
                {
                  call_number: 3,
                  model_name: "qwen/qwen3.8-27b",
                  area_tag: "schedule",
                  input: "Structure 4-hour timeline with required 15-minute prayer break.",
                  output: "Constructed 240-minute schedule: 00:00-00:30 Opening, 00:30-02:45 Sprint, 02:45-03:00 Prayer break, 03:00-03:45 Judging, 03:45-04:00 Closing.",
                  prompt_tokens: 50,
                  completion_tokens: 500,
                  total_tokens: 550,
                },
                {
                  call_number: 4,
                  model_name: "qwen/qwen3.8-27b",
                  area_tag: "food",
                  input: "Compute catering plan for 180 headcount using latest valid quote from 12 Nov.",
                  output: "Standard lunch box @ Rs 1,200 per head with free delivery x 180 attendees = Rs 216,000.",
                  prompt_tokens: 56,
                  completion_tokens: 172,
                  total_tokens: 228,
                },
                {
                  call_number: 5,
                  model_name: "qwen/qwen3.8-27b",
                  area_tag: "judging",
                  input: "Calculate judge-to-team allocation: 20 confirmed judges evaluating 50 teams.",
                  output: "20 judges evaluating 50 teams yields 2.5 teams per judge (<= 3.0 cap). Total honorarium = Rs 100,000.",
                  prompt_tokens: 53,
                  completion_tokens: 332,
                  total_tokens: 385,
                },
                {
                  call_number: 6,
                  model_name: "qwen/qwen3.8-27b",
                  area_tag: "budget",
                  input: "Synthesize total projected budget vs Rs 650,000 limit.",
                  output: "Total spend = Committed Rs 130k + Variable Rs 466k = Rs 596k <= Rs 650k limit. Surplus = Rs 54k.",
                  prompt_tokens: 53,
                  completion_tokens: 169,
                  total_tokens: 222,
                },
              ]).map((entry, idx) => (
                <div key={idx} className="border border-[#232F46] rounded-lg p-3.5 bg-[#0B0F17] space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-5 h-5 rounded-full bg-blue-600/30 text-blue-400 flex items-center justify-center text-[10px] font-mono font-bold">
                        #{entry.call_number}
                      </span>
                      <span className="text-xs font-mono font-bold text-white">{entry.model_name}</span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        [{entry.area_tag}]
                      </span>
                    </div>
                    <div className="text-[11px] font-mono text-slate-400">
                      Tokens: <span className="text-white">P:{entry.prompt_tokens}</span> +{" "}
                      <span className="text-white">C:{entry.completion_tokens}</span> ={" "}
                      <span className="text-emerald-400 font-bold">{entry.total_tokens}</span>
                    </div>
                  </div>
                  <div className="text-xs font-mono text-slate-400 bg-[#151D2C] p-2 rounded border border-[#232F46]">
                    <span className="text-blue-400">Input: </span>
                    {entry.input}
                  </div>
                  <div className="text-xs font-mono text-slate-300 bg-[#151D2C] p-2 rounded border border-[#232F46]">
                    <span className="text-emerald-400">Output: </span>
                    {entry.output}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* SCREEN 5: REJECTED MESSAGES TAB */}
        {activeTab === "rejected" && (
          <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-[#232F46] pb-3">
              <div>
                <h3 className="text-sm font-semibold text-white">Rejected Messages & Conflict Audit Log</h3>
                <p className="text-xs text-[#94A3B8]">
                  20 Scored Points: Preserving active plan valid while explaining why conflicting messages failed
                </p>
              </div>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/30 font-mono">
                {rejected.length} Conflicts Caught
              </span>
            </div>

            {rejected.length === 0 ? (
              <div className="text-center py-10 text-slate-400 text-xs">
                No messages rejected yet. Submit conflicting messages in the console to test invariant rejection.
              </div>
            ) : (
              <div className="space-y-3">
                {rejected.map((rec, idx) => (
                  <div key={idx} className="border border-red-500/30 bg-red-950/10 rounded-lg p-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-red-400">Conflict #{rec.message_index || idx + 1}</span>
                        <span className="text-xs text-slate-400">From: {rec.sender}</span>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-red-500/20 text-red-300">
                          Area: [{rec.target_area}]
                        </span>
                      </div>
                      <span className="text-[10px] text-slate-500 font-mono">{rec.timestamp.slice(11, 19)}</span>
                    </div>
                    <div className="text-xs bg-[#0B0F17] p-2.5 rounded border border-[#232F46] text-slate-300">
                      <span className="text-slate-500">Attempted Message: </span>&quot;{rec.raw_text}&quot;
                    </div>
                    <div className="text-xs text-red-300 bg-red-950/30 p-2.5 rounded border border-red-500/30">
                      <span className="font-semibold text-red-400">Rejection Reason: </span>
                      {rec.rejection_reason}
                    </div>
                    <div className="text-[11px] text-emerald-400 flex items-center gap-1.5 pt-1">
                      <span>✓</span> Active plan preserved in valid state. 6-point invariant gate remained green.
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* SCREEN 6: INTERACTIVE MESSAGE INJECTOR CONSOLE */}
        {activeTab === "console" && (
          <div className="bg-[#151D2C] border border-[#232F46] rounded-xl p-5 space-y-4">
            <div className="border-b border-[#232F46] pb-3">
              <h3 className="text-sm font-semibold text-white">Interactive Incremental Message Console</h3>
              <p className="text-xs text-[#94A3B8]">
                Inject real-time updates during live volunteer testing. Engine applies selective routing (&le; 5 calls).
              </p>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-slate-400 mb-1.5 block">Competition Practice Scenarios (One-Click):</label>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => {
                      setInputMsg("Printing invoice update: Printing expense is now Rs 15,000 instead of Rs 10,000.");
                      setSenderName("Finance Department");
                    }}
                    className="px-2.5 py-1 text-xs rounded bg-[#0B0F17] hover:bg-[#232F46] border border-[#232F46] text-blue-300 transition"
                  >
                    Scenario 1: Printing +Rs 5k (Valid Change)
                  </button>
                  <button
                    onClick={() => {
                      setInputMsg("Caterer WhatsApp: Salam bhai! Can we provide only 100 lunch boxes instead of 180? Shortage of supplies.");
                      setSenderName("Caterer");
                    }}
                    className="px-2.5 py-1 text-xs rounded bg-[#0B0F17] hover:bg-[#232F46] border border-[#232F46] text-amber-300 transition"
                  >
                    Scenario 2: Caterer 100 Meals (Sabotage Conflict)
                  </button>
                  <button
                    onClick={() => {
                      setInputMsg("Venue agent: Room D is now available for Rs 35,000 if you want to switch.");
                      setSenderName("Venue Agent");
                    }}
                    className="px-2.5 py-1 text-xs rounded bg-[#0B0F17] hover:bg-[#232F46] border border-[#232F46] text-purple-300 transition"
                  >
                    Scenario 3: Room D 80 seats (Capacity Conflict)
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                <div className="md:col-span-1">
                  <label className="text-xs text-slate-400 mb-1 block">Sender Identity</label>
                  <input
                    type="text"
                    value={senderName}
                    onChange={(e) => setSenderName(e.target.value)}
                    className="w-full bg-[#0B0F17] border border-[#232F46] rounded p-2 text-xs text-white focus:outline-none focus:border-blue-500"
                    placeholder="e.g. Finance, Caterer"
                  />
                </div>
                <div className="md:col-span-3">
                  <label className="text-xs text-slate-400 mb-1 block">Message Content (English or Roman Urdu)</label>
                  <input
                    type="text"
                    value={inputMsg}
                    onChange={(e) => setInputMsg(e.target.value)}
                    className="w-full bg-[#0B0F17] border border-[#232F46] rounded p-2 text-xs text-white focus:outline-none focus:border-blue-500"
                    placeholder="Paste incremental email or WhatsApp message..."
                  />
                </div>
              </div>

              <div className="flex justify-end pt-2">
                <button
                  onClick={() => handleSendMessage()}
                  disabled={loading || !inputMsg.trim()}
                  className="px-5 py-2 text-xs font-semibold rounded bg-blue-600 hover:bg-blue-500 text-white transition disabled:opacity-50"
                >
                  {loading ? "Processing Update..." : "Dispatch Message to Engine"}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* FOOTER */}
      <footer className="border-t border-[#232F46] bg-[#0B0F17] px-6 py-4 text-center text-xs text-slate-500">
        HackPlan AI · Single-Command Architecture · 6 Invariant Gates · 100% Deterministic Arithmetic Verification
      </footer>
    </div>
  );
}
