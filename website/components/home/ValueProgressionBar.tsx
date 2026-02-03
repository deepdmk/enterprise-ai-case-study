"use client";

import { cn } from "@/lib/utils";
import Link from "next/link";
import { useState } from "react";

interface ProgressionBox {
  title: string;
  phase: string;
  description: string[];
  href: string;
  color: "navy" | "teal" | "magenta" | "amber";
  height: string;
}

const progressionBoxes: ProgressionBox[] = [
  {
    title: "AI Search",
    phase: "Phase 1: AI Search",
    description: [
      "Search all company data with AI embeddings",
      "so employees find relevant documents more easily",
    ],
    href: "/solution/phase-1",
    color: "navy",
    height: "h-[48px] md:h-[56px]",
  },
  {
    title: "Specialized AI",
    phase: "Phase 2: Specialized AI",
    description: [
      "AI learns your team's specific tasks",
      "giving employees intelligent assistance for the work they prioritize",
    ],
    href: "/solution/phase-2",
    color: "teal",
    height: "h-[56px] md:h-[68px]",
  },
  {
    title: "Division AI",
    phase: "Phase 3: Division AI",
    description: [
      "Each division gets expert AI combining",
      "their specialized assistants into one agent that does many tasks to your standards",
    ],
    href: "/solution/phase-3",
    color: "magenta",
    height: "h-[64px] md:h-[80px]",
  },
  {
    title: "Cross-Divisional AI",
    phase: "Phase 4: Cross-Divisional AI",
    description: [
      "Agents learn how to use information across your divisions",
      "giving access to task capabilities to enhance other divisions' work",
    ],
    href: "/solution/phase-4",
    color: "amber",
    height: "h-[72px] md:h-[92px]",
  },
  {
    title: "Enterprise Orchestrated AI",
    phase: "Phase 5: Enterprise Orchestrated AI",
    description: [
      "Employees across your organization engage through a single AI window",
      "that can leverage data and capabilities across all the enterprise to get them what they need",
      "tailored to your data and your culture",
    ],
    href: "/solution/phase-5",
    color: "teal",
    height: "h-[80px] md:h-[104px]",
  },
];

const productionBox: ProgressionBox = {
  title: "AWS Production Scale",
  phase: "Production Deployment",
  description: [
    "You can run the system independently on your own infrastructure",
    "but it is designed to easily plugin or transfer to other platforms like AWS",
  ],
  href: "/solution/scaling-production",
  color: "navy",
  height: "h-[80px] md:h-[104px]",
};

const colorStyles = {
  navy: {
    bg: "bg-navy",
    bgHover: "hover:bg-navy/90",
    border: "border-white/30",
    text: "text-white",
  },
  teal: {
    bg: "bg-teal",
    bgHover: "hover:bg-teal/90",
    border: "border-teal/30",
    text: "text-white",
  },
  magenta: {
    bg: "bg-magenta",
    bgHover: "hover:bg-magenta/90",
    border: "border-magenta/30",
    text: "text-white",
  },
  amber: {
    bg: "bg-amber",
    bgHover: "hover:bg-amber/90",
    border: "border-amber/30",
    text: "text-white",
  },
};

function Tooltip({
  phase,
  description,
  visible,
}: {
  phase: string;
  description: string[];
  visible: boolean;
}) {
  return (
    <div
      className={cn(
        "absolute left-1/2 -translate-x-1/2 bottom-full mb-3 z-50",
        "w-72 p-4 rounded-lg shadow-xl",
        "bg-gray-900 text-white text-sm",
        "transition-all duration-200",
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2 pointer-events-none"
      )}
    >
      <div className="font-semibold mb-2 text-teal">{phase}</div>
      {description.map((line, i) => (
        <p key={i} className="text-gray-300 leading-relaxed">
          {line}
        </p>
      ))}
      <div className="absolute left-1/2 -translate-x-1/2 top-full w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-gray-900" />
    </div>
  );
}

function ProgressionBoxComponent({ box }: { box: ProgressionBox }) {
  const [isHovered, setIsHovered] = useState(false);
  const styles = colorStyles[box.color];

  return (
    <div className="relative flex-shrink-0 self-end">
      <Tooltip phase={box.phase} description={box.description} visible={isHovered} />
      <Link
        href={box.href}
        className={cn(
          "block w-[120px] md:w-[140px] rounded-lg border-2",
          "flex items-center justify-center px-2",
          "transition-all duration-300 ease-out",
          "hover:shadow-lg hover:-translate-y-1",
          "focus:outline-none focus:ring-2 focus:ring-white/50 focus:ring-offset-2 focus:ring-offset-navy",
          styles.bg,
          styles.bgHover,
          styles.border,
          box.height
        )}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        aria-label={`${box.phase}: ${box.description.join(" ")}`}
      >
        <span className={cn("text-xs md:text-sm font-semibold text-center leading-tight", styles.text)}>
          {box.title}
        </span>
      </Link>
    </div>
  );
}

function DoubleArrowConnector() {
  return (
    <div className="flex flex-col items-center justify-center flex-shrink-0 self-end w-10 h-[80px] md:h-[104px] text-white/70">
      <svg
        className="w-6 h-6"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M5 12h14" />
        <path d="M12 5l7 7-7 7" />
      </svg>
      <svg
        className="w-6 h-6 rotate-180"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M5 12h14" />
        <path d="M12 5l7 7-7 7" />
      </svg>
    </div>
  );
}

interface ValueProgressionBarProps {
  className?: string;
}

export function ValueProgressionBar({ className }: ValueProgressionBarProps) {
  return (
    <div className={cn("w-full", className)}>
      {/* Desktop: Horizontal flow, aligned at bottom */}
      <div className="hidden lg:flex items-end justify-center gap-3">
        {progressionBoxes.map((box, index) => (
          <ProgressionBoxComponent key={index} box={box} />
        ))}
        <DoubleArrowConnector />
        <ProgressionBoxComponent box={productionBox} />
      </div>

      {/* Tablet/Mobile: Horizontal scroll with snap */}
      <div className="lg:hidden overflow-x-auto scrollbar-hide">
        <div className="flex items-end gap-3 pb-4 px-4 snap-x snap-mandatory min-w-max">
          {progressionBoxes.map((box, index) => (
            <div key={index} className="snap-center">
              <ProgressionBoxComponent box={box} />
            </div>
          ))}
          <div className="snap-center">
            <DoubleArrowConnector />
          </div>
          <div className="snap-center">
            <ProgressionBoxComponent box={productionBox} />
          </div>
        </div>
      </div>

      {/* Scroll hint for mobile */}
      <p className="lg:hidden text-center text-white/60 text-xs mt-2">
        Scroll to explore phases →
      </p>
    </div>
  );
}
