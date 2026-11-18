install and set up assistant-ui with `npx assistant-ui@latest setup --products elements/chart`

"use client";

import type { ToolCallMessagePartComponent } from "@assistant-ui/react";
import { Chart } from "@/components/assistant-ui/elements/chart";

type PlotMetricArgs = { label: string; points: number[] };
type PlotMetricResult = { value: string; delta?: string };

export const PlotMetricToolUI: ToolCallMessagePartComponent<
PlotMetricArgs,
PlotMetricResult

> = ({ args, result }) => {
> const points = args.points ?? [];
> return (

    <Chart
      label={args.label ?? ""}
      value={result?.value ?? "…"}
      delta={result?.delta}
      points={points}
      visibleCount={points.length}
      variant="area"
    />

);
};

import { AssistantRuntimeProvider, AuiConfig, Tools } from "@assistant-ui/react";
import { useChatRuntime } from "@assistant-ui/ai-sdk";
import { toolkit } from "./toolkit";

export function MyRuntimeProvider({ children }: { children: React.ReactNode }) {
const runtime = useChatRuntime();
const config = AuiConfig({ tools: Tools({ toolkit }) });
return (
<AssistantRuntimeProvider runtime={runtime} config={config}>
{children}
</AssistantRuntimeProvider>
);
}

<div data-slot="chart">
  <div>{/* label, delta */}</div>
  <span>{/* value */}</span>
  <svg>{/* baseline, then an area+line, a line, or bars depending on variant */}</svg>
</div>
