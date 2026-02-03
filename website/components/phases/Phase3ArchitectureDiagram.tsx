"use client";

import { cn } from "@/lib/utils";

function AdapterIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M9 9h6M9 12h6M9 15h4" />
    </svg>
  );
}

function MoEIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="6" r="3" />
      <circle cx="6" cy="18" r="3" />
      <circle cx="18" cy="18" r="3" />
      <path d="M12 9v3M9 15l-1.5-3M15 15l1.5-3" />
    </svg>
  );
}

function AgentIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
    </svg>
  );
}

function Arrow({ direction = "down", className }: { direction?: "down" | "right"; className?: string }) {
  if (direction === "right") {
    return (
      <svg className={cn("w-4 h-4 text-gray-400", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M5 12h14M12 5l7 7-7 7" />
      </svg>
    );
  }
  return (
    <svg className={cn("w-4 h-4 text-gray-400", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M12 5v14M5 12l7 7 7-7" />
    </svg>
  );
}

function ProgramBox({ number, title, subtitle }: { number: number; title: string; subtitle: string }) {
  return (
    <div className="bg-magenta/5 border border-magenta/20 rounded-lg p-2 text-center min-w-0">
      <div className="text-[10px] text-magenta/60 font-medium">Program {number}</div>
      <div className="font-bold text-magenta text-xs leading-tight">{title}</div>
      <div className="text-[10px] text-gray-500 mt-0.5">{subtitle}</div>
    </div>
  );
}

function UnitBox({
  title,
  experts,
  color
}: {
  title: string;
  experts: number;
  color: "fundraising" | "bizdev" | "fieldops";
}) {
  const colors = {
    fundraising: "bg-teal/10 border-teal text-teal",
    bizdev: "bg-amber/10 border-amber text-amber",
    fieldops: "bg-navy/10 border-navy text-navy",
  };

  return (
    <div className={cn("border rounded-lg p-2 text-center flex-1", colors[color])}>
      <div className="font-bold text-xs">{title}</div>
      <div className="text-[10px] opacity-80">{experts} experts</div>
    </div>
  );
}

export function Phase3ArchitectureDiagram() {
  return (
    <div className="w-full py-4 px-4">
      {/* Title */}
      <div className="text-center mb-6">
        <h4 className="text-base font-bold text-navy mb-1">MoE Merge Pipeline</h4>
        <p className="text-xs text-gray-600">14 task models consolidated into 3 division agents</p>
      </div>

      {/* Desktop/Tablet Layout */}
      <div className="hidden md:block">
        <div className="max-w-3xl mx-auto space-y-4">

          {/* Row 1: Phase 2 Input */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Input from Phase 2</div>
            <div className="flex items-center justify-center gap-6">
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
                <AdapterIcon className="mx-auto mb-1 text-gray-600" />
                <div className="font-bold text-gray-700 text-sm">Phase 2 Exports</div>
                <div className="text-xs text-gray-500 mt-1">14 LoRA adapters across 3 units</div>
                <div className="flex gap-1 mt-2 justify-center">
                  <span className="bg-teal/20 text-teal rounded px-1.5 py-0.5 text-[9px]">5 FR</span>
                  <span className="bg-amber/20 text-amber rounded px-1.5 py-0.5 text-[9px]">5 BD</span>
                  <span className="bg-navy/20 text-navy rounded px-1.5 py-0.5 text-[9px]">4 FO</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 2: Merge Pipeline */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Merge Pipeline</div>
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ProgramBox number={1} title="Import" subtitle="Organize by unit" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={2} title="Config Gen" subtitle="3 MoE configs" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={3} title="mergekit-moe" subtitle="3 separate merges" />
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 3: MoE Models */}
          <div className="bg-magenta/5 border-2 border-magenta rounded-lg p-4 relative">
            <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
              <span className="text-[10px] font-bold text-magenta">3 DIVISION MoE MODELS</span>
            </div>
            <div className="flex items-center gap-3 mt-2">
              <div className="flex-1 bg-teal/10 border border-teal rounded-lg p-3 text-center">
                <MoEIcon className="mx-auto mb-1 text-teal" />
                <div className="font-bold text-teal text-xs">Fundraising</div>
                <div className="text-[10px] text-teal/70">MoE (5 experts)</div>
                <div className="text-[9px] text-gray-500 mt-1">2-of-5 routing</div>
              </div>
              <div className="flex-1 bg-amber/10 border border-amber rounded-lg p-3 text-center">
                <MoEIcon className="mx-auto mb-1 text-amber" />
                <div className="font-bold text-amber text-xs">Business Dev</div>
                <div className="text-[10px] text-amber/70">MoE (5 experts)</div>
                <div className="text-[9px] text-gray-500 mt-1">2-of-5 routing</div>
              </div>
              <div className="flex-1 bg-navy/10 border border-navy rounded-lg p-3 text-center">
                <MoEIcon className="mx-auto mb-1 text-navy" />
                <div className="font-bold text-navy text-xs">Field Ops</div>
                <div className="text-[10px] text-navy/70">MoE (4 experts)</div>
                <div className="text-[9px] text-gray-500 mt-1">2-of-4 routing</div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 4: Export */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ProgramBox number={5} title="Export" subtitle="3 packages for Phase 4" />
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 5: Phase 4 Output */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Output to Phase 4</div>
            <div className="flex items-center gap-3">
              <div className="flex-1 bg-teal border border-teal rounded-lg p-2 text-center">
                <AgentIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-xs">Fundraising</div>
                <div className="text-[10px] text-white/70">A2A Agent</div>
              </div>
              <div className="flex-1 bg-amber border border-amber rounded-lg p-2 text-center">
                <AgentIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-xs">Business Dev</div>
                <div className="text-[10px] text-white/70">A2A Agent</div>
              </div>
              <div className="flex-1 bg-navy border border-navy rounded-lg p-2 text-center">
                <AgentIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-xs">Field Ops</div>
                <div className="text-[10px] text-white/70">A2A Agent</div>
              </div>
            </div>
            <div className="text-center mt-3">
              <span className="text-xs text-gray-500">Phase 4 Agentic Network</span>
            </div>
          </div>

        </div>
      </div>

      {/* Mobile Layout */}
      <div className="md:hidden space-y-4">
        {/* Phase 2 Input */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Input</div>
          <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
            <AdapterIcon className="mx-auto mb-1 text-gray-600" />
            <div className="font-bold text-gray-700 text-sm">Phase 2 Exports</div>
            <div className="text-xs text-gray-500">14 LoRA adapters</div>
            <div className="flex gap-1 mt-2 justify-center">
              <span className="bg-teal/20 text-teal rounded px-1.5 py-0.5 text-[9px]">5 FR</span>
              <span className="bg-amber/20 text-amber rounded px-1.5 py-0.5 text-[9px]">5 BD</span>
              <span className="bg-navy/20 text-navy rounded px-1.5 py-0.5 text-[9px]">4 FO</span>
            </div>
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Programs */}
        <div className="bg-white border border-gray-200 rounded-lg p-3 space-y-2">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Merge Pipeline</div>
          <ProgramBox number={1} title="Import" subtitle="Organize by unit" />
          <div className="flex justify-center"><Arrow direction="down" /></div>
          <ProgramBox number={2} title="Config Gen" subtitle="3 MoE configs" />
          <div className="flex justify-center"><Arrow direction="down" /></div>
          <ProgramBox number={3} title="mergekit-moe" subtitle="3 separate merges" />
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* MoE Models */}
        <div className="bg-magenta/5 border-2 border-magenta rounded-lg p-3 relative">
          <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
            <span className="text-[10px] font-bold text-magenta">3 MoE MODELS</span>
          </div>
          <div className="space-y-2 mt-2">
            <div className="bg-teal/10 border border-teal rounded-lg p-2 text-center">
              <div className="font-bold text-teal text-sm">Fundraising MoE</div>
              <div className="text-xs text-teal/70">5 experts, 2-of-5 routing</div>
            </div>
            <div className="bg-amber/10 border border-amber rounded-lg p-2 text-center">
              <div className="font-bold text-amber text-sm">Business Dev MoE</div>
              <div className="text-xs text-amber/70">5 experts, 2-of-5 routing</div>
            </div>
            <div className="bg-navy/10 border border-navy rounded-lg p-2 text-center">
              <div className="font-bold text-navy text-sm">Field Ops MoE</div>
              <div className="text-xs text-navy/70">4 experts, 2-of-4 routing</div>
            </div>
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Export */}
        <ProgramBox number={5} title="Export" subtitle="3 packages for Phase 4" />

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* A2A Agents */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Phase 4 Agents</div>
          <div className="grid grid-cols-3 gap-2">
            <div className="bg-teal border border-teal rounded-lg p-2 text-center">
              <div className="font-bold text-white text-[10px]">Fundraising</div>
            </div>
            <div className="bg-amber border border-amber rounded-lg p-2 text-center">
              <div className="font-bold text-white text-[10px]">Biz Dev</div>
            </div>
            <div className="bg-navy border border-navy rounded-lg p-2 text-center">
              <div className="font-bold text-white text-[10px]">Field Ops</div>
            </div>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap justify-center gap-3 text-[10px]">
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-gray-200 border border-gray-300"></div>
          <span className="text-gray-600">Input/Output</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-magenta/10 border border-magenta/30"></div>
          <span className="text-gray-600">Programs</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-magenta/20 border border-magenta"></div>
          <span className="text-gray-600">MoE Models</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-teal border border-teal"></div>
          <span className="text-gray-600">FR</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-amber border border-amber"></div>
          <span className="text-gray-600">BD</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-navy border border-navy"></div>
          <span className="text-gray-600">FO</span>
        </div>
      </div>
    </div>
  );
}
