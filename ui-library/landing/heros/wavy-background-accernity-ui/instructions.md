npx shadcn@latest add @aceternity/wavy-background-demo

prompt: Help me add the "wavy-background-demo" component from Aceternity UI to my project. Its source files and dependencies are at https://ui.aceternity.com/registry/wavy-background-demo.json. First check that the project uses shadcn/ui, Tailwind CSS v4 and TypeScript.

"use client";
import React from "react";
import { WavyBackground } from "../ui/wavy-background";

export function WavyBackgroundDemo() {
return (
<WavyBackground className="max-w-4xl mx-auto pb-40">
<p className="text-2xl md:text-4xl lg:text-7xl text-white font-bold inter-var text-center">
Hero waves are cool
</p>
<p className="text-base md:text-lg mt-4 text-white font-normal inter-var text-center">
Leverage the power of canvas to create a beautiful hero section
</p>
</WavyBackground>
);
}
