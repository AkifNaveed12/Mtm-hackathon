import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HackPlan AI · Event operations",
  description:
    "Plan, validate, and manage physical events with a transparent AI workflow.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body>{children}</body>
    </html>
  );
}
