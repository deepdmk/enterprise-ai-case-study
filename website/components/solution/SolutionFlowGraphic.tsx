"use client";

import Link from "next/link";

/**
 * Solution Flow Graphic - Stacked Capabilities View
 *
 * Shows the progressive accumulation of capabilities across phases.
 * Right-aligned staircase where each phase builds from the one below.
 * Each layer is shorter than the previous, showing how capabilities stack.
 */

const phases = [
  {
    number: 0,
    title: "Infrastructure Foundation",
    slug: "phase-0",
    color: "bg-navy",
    borderColor: "border-navy",
    techs: [
      { name: "JSON", color: "bg-gray-700" },
      { name: "YAML", color: "bg-gray-700" },
    ],
  },
  {
    number: 1,
    title: "Unified Embedding Space",
    slug: "phase-1",
    color: "bg-teal",
    borderColor: "border-teal",
    techs: [
      { name: "Sentence-Transformers", color: "bg-teal-700" },
      { name: "ChromaDB", color: "bg-green-700" },
    ],
  },
  {
    number: 2,
    title: "Task-Specific SLMs",
    slug: "phase-2",
    color: "bg-magenta",
    borderColor: "border-magenta",
    techs: [
      { name: "PEFT/LoRA", color: "bg-purple-700" },
      { name: "Unsloth", color: "bg-pink-700" },
    ],
  },
  {
    number: 3,
    title: "MoE Division Agents",
    slug: "phase-3",
    color: "bg-amber",
    borderColor: "border-amber",
    techs: [
      { name: "Mergekit", color: "bg-orange-700" },
      { name: "MoE", color: "bg-amber-700" },
    ],
  },
  {
    number: 4,
    title: "Agentic Discovery",
    slug: "phase-4",
    color: "bg-teal",
    borderColor: "border-teal",
    techs: [
      { name: "A2A Protocol", color: "bg-cyan-700" },
    ],
  },
  {
    number: 5,
    title: "Orchestrated System",
    slug: "phase-5",
    color: "bg-magenta",
    borderColor: "border-magenta",
    techs: [
      { name: "Agno", color: "bg-violet-700" },
    ],
  },
];

// Calculate width percentages for the staircase effect (decreasing as we go up)
const widthClasses = [
  "w-full",           // Phase 0: 100%
  "w-[88%]",          // Phase 1: 88%
  "w-[76%]",          // Phase 2: 76%
  "w-[64%]",          // Phase 3: 64%
  "w-[52%]",          // Phase 4: 52%
  "w-[40%]",          // Phase 5: 40%
];

function TechBadge({ name, color }: { name: string; color: string }) {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white ${color} shadow-sm`}
    >
      {name}
    </span>
  );
}

export function SolutionFlowGraphic() {
  // Reverse phases so we render from top (Phase 5) to bottom (Phase 0)
  const reversedPhases = [...phases].reverse();

  return (
    <div className="w-full">
      <div className="bg-gray-50 rounded-2xl shadow-xl border-2 border-gray-300 p-6 md:p-10">
      {/* Desktop Layout */}
      <div className="hidden md:flex gap-4">
        {/* Staircase - phases stacking */}
        <div className="flex-1 flex flex-col items-end gap-0">
          {reversedPhases.map((phase, idx) => {
            const widthClass = widthClasses[phases.length - 1 - idx];
            const isFirst = idx === 0;
            const isLast = idx === reversedPhases.length - 1;

            return (
              <Link
                key={phase.number}
                href={`/solution/${phase.slug}`}
                className={`${widthClass} group block`}
              >
                <div
                  className={`
                    ${phase.color} text-white p-4
                    ${isFirst ? "rounded-tl-xl rounded-tr-xl" : ""}
                    ${isLast ? "rounded-bl-xl" : ""}
                    border-l-4 border-white/20
                    hover:brightness-110 transition-all duration-200
                    relative
                  `}
                >
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl font-bold opacity-80">{phase.number}</span>
                      <span className="font-semibold">{phase.title}</span>
                    </div>
                    <div className="flex items-center gap-2 flex-wrap justify-end">
                      {phase.techs.map((tech) => (
                        <TechBadge key={tech.name} name={tech.name} color={tech.color} />
                      ))}
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>

        {/* Production - Vertical box on the right */}
        <Link href="/solution/scaling-production" className="block group">
          <div className="bg-gradient-to-b from-navy to-teal text-white px-6 py-8 rounded-xl hover:brightness-110 transition-all duration-200 h-full flex flex-col items-center justify-center text-center min-w-[140px]">
            <span className="text-3xl font-bold opacity-80 mb-3">✓</span>
            <span className="font-bold text-lg mb-4">Scaling Production</span>
            <div className="flex flex-col gap-2">
              <TechBadge name="SageMaker" color="bg-orange-600" />
              <TechBadge name="Bedrock" color="bg-blue-700" />
              <TechBadge name="Aurora" color="bg-indigo-700" />
            </div>
          </div>
        </Link>
      </div>

      {/* Mobile Layout - Simplified stack */}
      <div className="md:hidden">
        <div className="flex flex-col gap-2">
          {reversedPhases.map((phase) => (
            <Link
              key={phase.number}
              href={`/solution/${phase.slug}`}
              className="block"
            >
              <div
                className={`${phase.color} text-white p-3 rounded-lg hover:brightness-110 transition-all duration-200`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-lg font-bold opacity-80">{phase.number}</span>
                  <span className="font-semibold text-sm">{phase.title}</span>
                </div>
                <div className="flex items-center gap-1.5 flex-wrap">
                  {phase.techs.map((tech) => (
                    <TechBadge key={tech.name} name={tech.name} color={tech.color} />
                  ))}
                </div>
              </div>
            </Link>
          ))}

          {/* Production */}
          <Link href="/solution/scaling-production" className="block mt-2">
            <div className="bg-gradient-to-r from-navy to-teal text-white p-3 rounded-lg hover:brightness-110 transition-all duration-200">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-lg font-bold opacity-80">✓</span>
                <span className="font-semibold text-sm">Scaling Production</span>
              </div>
              <div className="flex items-center gap-1.5 flex-wrap">
                <TechBadge name="SageMaker" color="bg-orange-600" />
                <TechBadge name="Bedrock" color="bg-blue-700" />
                <TechBadge name="Aurora" color="bg-indigo-700" />
              </div>
            </div>
          </Link>
        </div>
      </div>
      </div>
      <div className="text-center mt-6">
        <p className="text-gray-700 text-lg font-medium">
          Click any phase to explore the implementation details
        </p>
        <div className="mt-3 animate-bounce">
          <svg
            className="w-6 h-6 mx-auto text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}
