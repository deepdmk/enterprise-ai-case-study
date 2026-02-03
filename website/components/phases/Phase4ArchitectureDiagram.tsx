"use client";

import { cn } from "@/lib/utils";

function AgentIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
    </svg>
  );
}

function NetworkIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="5" r="2" />
      <circle cx="5" cy="19" r="2" />
      <circle cx="19" cy="19" r="2" />
      <path d="M12 7v4M7 17l3-6M17 17l-3-6" />
    </svg>
  );
}

function DataIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <path d="M14 2v6h6M16 13H8M16 17H8" />
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
    <div className="bg-teal/5 border border-teal/20 rounded-lg p-2 text-center min-w-0">
      <div className="text-[10px] text-teal/60 font-medium">Program {number}</div>
      <div className="font-bold text-teal text-xs leading-tight">{title}</div>
      <div className="text-[10px] text-gray-500 mt-0.5">{subtitle}</div>
    </div>
  );
}

export function Phase4ArchitectureDiagram() {
  return (
    <div className="w-full py-4 px-4">
      {/* Title */}
      <div className="text-center mb-6">
        <h4 className="text-base font-bold text-navy mb-1">Agentic Discovery Pipeline</h4>
        <p className="text-xs text-gray-600">90-day A2A experiment generating orchestrator training data</p>
      </div>

      {/* Desktop/Tablet Layout */}
      <div className="hidden md:block">
        <div className="max-w-3xl mx-auto space-y-4">

          {/* Row 1: Input from Phase 3 */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Input from Phase 3</div>
            <div className="flex items-center justify-center gap-3">
              <div className="bg-magenta/10 border border-magenta rounded-lg p-2 text-center flex-1">
                <div className="font-bold text-magenta text-xs">Fundraising MoE</div>
                <div className="text-[10px] text-magenta/70">5 experts</div>
              </div>
              <div className="bg-magenta/10 border border-magenta rounded-lg p-2 text-center flex-1">
                <div className="font-bold text-magenta text-xs">Business Dev MoE</div>
                <div className="text-[10px] text-magenta/70">5 experts</div>
              </div>
              <div className="bg-magenta/10 border border-magenta rounded-lg p-2 text-center flex-1">
                <div className="font-bold text-magenta text-xs">Field Ops MoE</div>
                <div className="text-[10px] text-magenta/70">4 experts</div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 2: Programs 1-2 */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Agent Setup</div>
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ProgramBox number={1} title="A2A Fine-Tuning" subtitle="Add protocol capabilities" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={2} title="Agent Services" subtitle="3 FastAPI services" />
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 3: A2A Agent Network */}
          <div className="bg-teal/5 border-2 border-teal rounded-lg p-4 relative">
            <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
              <span className="text-[10px] font-bold text-teal">A2A AGENT NETWORK</span>
            </div>
            <div className="flex items-center justify-center gap-4 mt-2">
              <div className="bg-teal border border-teal rounded-lg p-2 text-center w-28">
                <AgentIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-xs">Fundraising</div>
                <div className="text-[10px] text-white/70">:8001</div>
              </div>
              <div className="flex flex-col items-center gap-1">
                <div className="text-[9px] text-teal">A2A Protocol</div>
                <NetworkIcon className="text-teal" />
                <div className="text-[9px] text-gray-500">Cascade calls</div>
              </div>
              <div className="bg-teal border border-teal rounded-lg p-2 text-center w-28">
                <AgentIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-xs">Business Dev</div>
                <div className="text-[10px] text-white/70">:8002</div>
              </div>
              <div className="flex flex-col items-center gap-1">
                <div className="text-[9px] text-teal">A2A Protocol</div>
                <NetworkIcon className="text-teal" />
                <div className="text-[9px] text-gray-500">Cascade calls</div>
              </div>
              <div className="bg-teal border border-teal rounded-lg p-2 text-center w-28">
                <AgentIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-xs">Field Ops</div>
                <div className="text-[10px] text-white/70">:8003</div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 4: Discovery Pipeline */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-3 mb-3">
              <ProgramBox number={3} title="Discovery Pipeline" subtitle="90-day experiment" />
            </div>
            {/* 7-Phase Schedule */}
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="text-[10px] font-semibold text-gray-600 mb-2">7-Phase Adaptive Depth Schedule</div>
              <div className="flex gap-1">
                <div className="flex-1 bg-gray-200 rounded p-1 text-center">
                  <div className="text-[9px] font-bold text-gray-700">P1</div>
                  <div className="text-[8px] text-gray-500">d=1</div>
                  <div className="text-[8px] text-gray-400">7d</div>
                </div>
                <div className="flex-1 bg-teal/20 rounded p-1 text-center">
                  <div className="text-[9px] font-bold text-teal">P2</div>
                  <div className="text-[8px] text-teal/70">d=2</div>
                  <div className="text-[8px] text-gray-400">14d</div>
                </div>
                <div className="flex-1 bg-teal/30 rounded p-1 text-center">
                  <div className="text-[9px] font-bold text-teal">P3</div>
                  <div className="text-[8px] text-teal/70">d=3</div>
                  <div className="text-[8px] text-gray-400">14d</div>
                </div>
                <div className="flex-1 bg-amber/20 rounded p-1 text-center">
                  <div className="text-[9px] font-bold text-amber">P4</div>
                  <div className="text-[8px] text-amber/70">d=2</div>
                  <div className="text-[8px] text-gray-400">14d</div>
                </div>
                <div className="flex-1 bg-teal/40 rounded p-1 text-center">
                  <div className="text-[9px] font-bold text-teal">P5</div>
                  <div className="text-[8px] text-teal/70">d=4</div>
                  <div className="text-[8px] text-gray-400">14d</div>
                </div>
                <div className="flex-1 bg-amber/20 rounded p-1 text-center">
                  <div className="text-[9px] font-bold text-amber">P6</div>
                  <div className="text-[8px] text-amber/70">d=2</div>
                  <div className="text-[8px] text-gray-400">12d</div>
                </div>
                <div className="flex-1 bg-navy/20 rounded p-1 text-center">
                  <div className="text-[9px] font-bold text-navy">P7</div>
                  <div className="text-[8px] text-navy/70">adapt</div>
                  <div className="text-[8px] text-gray-400">15d</div>
                </div>
              </div>
              <div className="flex justify-between mt-2 text-[9px] text-gray-500">
                <span>Baseline</span>
                <span>Exploration</span>
                <span className="text-amber">Control</span>
                <span>Deep</span>
                <span className="text-amber">Control</span>
                <span className="text-navy">Adaptive</span>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 5: Analyzer & Output */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ProgramBox number={4} title="Adaptive Analyzer" subtitle="Optimal depths" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1 bg-navy/10 border border-navy rounded-lg p-3 text-center">
                <DataIcon className="mx-auto mb-1 text-navy" />
                <div className="font-bold text-navy text-xs">Phase 5 Training Data</div>
                <div className="text-[10px] text-navy/70">orchestrator_chat.jsonl</div>
                <div className="text-[9px] text-gray-500 mt-1">900 A2A logs → training examples</div>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Mobile Layout */}
      <div className="md:hidden space-y-4">
        {/* Input */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">From Phase 3</div>
          <div className="grid grid-cols-3 gap-2">
            <div className="bg-magenta/10 border border-magenta rounded p-1.5 text-center">
              <div className="font-bold text-magenta text-[10px]">FR MoE</div>
            </div>
            <div className="bg-magenta/10 border border-magenta rounded p-1.5 text-center">
              <div className="font-bold text-magenta text-[10px]">BD MoE</div>
            </div>
            <div className="bg-magenta/10 border border-magenta rounded p-1.5 text-center">
              <div className="font-bold text-magenta text-[10px]">FO MoE</div>
            </div>
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Programs 1-2 */}
        <div className="bg-white border border-gray-200 rounded-lg p-3 space-y-2">
          <ProgramBox number={1} title="A2A Fine-Tuning" subtitle="Add protocol capabilities" />
          <div className="flex justify-center"><Arrow direction="down" /></div>
          <ProgramBox number={2} title="Agent Services" subtitle="3 FastAPI services" />
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Agent Network */}
        <div className="bg-teal/5 border-2 border-teal rounded-lg p-3 relative">
          <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
            <span className="text-[10px] font-bold text-teal">A2A NETWORK</span>
          </div>
          <div className="grid grid-cols-3 gap-2 mt-2">
            <div className="bg-teal rounded p-2 text-center">
              <div className="font-bold text-white text-[10px]">FR :8001</div>
            </div>
            <div className="bg-teal rounded p-2 text-center">
              <div className="font-bold text-white text-[10px]">BD :8002</div>
            </div>
            <div className="bg-teal rounded p-2 text-center">
              <div className="font-bold text-white text-[10px]">FO :8003</div>
            </div>
          </div>
          <div className="text-center mt-2 text-[9px] text-teal">Autonomous A2A collaboration</div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Discovery Pipeline */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <ProgramBox number={3} title="Discovery Pipeline" subtitle="90-day experiment" />
          <div className="mt-3 bg-gray-50 rounded p-2">
            <div className="text-[9px] font-semibold text-gray-600 mb-1">7-Phase Schedule</div>
            <div className="grid grid-cols-7 gap-0.5 text-[8px]">
              <div className="bg-gray-200 rounded p-0.5 text-center">
                <div className="font-bold">1</div>
                <div className="text-gray-500">d1</div>
              </div>
              <div className="bg-teal/20 rounded p-0.5 text-center">
                <div className="font-bold text-teal">2</div>
                <div className="text-teal/70">d2</div>
              </div>
              <div className="bg-teal/30 rounded p-0.5 text-center">
                <div className="font-bold text-teal">3</div>
                <div className="text-teal/70">d3</div>
              </div>
              <div className="bg-amber/20 rounded p-0.5 text-center">
                <div className="font-bold text-amber">4</div>
                <div className="text-amber/70">d2</div>
              </div>
              <div className="bg-teal/40 rounded p-0.5 text-center">
                <div className="font-bold text-teal">5</div>
                <div className="text-teal/70">d4</div>
              </div>
              <div className="bg-amber/20 rounded p-0.5 text-center">
                <div className="font-bold text-amber">6</div>
                <div className="text-amber/70">d2</div>
              </div>
              <div className="bg-navy/20 rounded p-0.5 text-center">
                <div className="font-bold text-navy">7</div>
                <div className="text-navy/70">adp</div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Analyzer & Output */}
        <div className="bg-white border border-gray-200 rounded-lg p-3 space-y-2">
          <ProgramBox number={4} title="Adaptive Analyzer" subtitle="Optimal depths" />
          <div className="flex justify-center"><Arrow direction="down" /></div>
          <div className="bg-navy/10 border border-navy rounded-lg p-2 text-center">
            <div className="font-bold text-navy text-sm">Phase 5 Training Data</div>
            <div className="text-xs text-navy/70">900 A2A logs</div>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap justify-center gap-3 text-[10px]">
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-magenta/20 border border-magenta"></div>
          <span className="text-gray-600">Phase 3 Input</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-teal/10 border border-teal/30"></div>
          <span className="text-gray-600">Programs</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-teal border border-teal"></div>
          <span className="text-gray-600">Agents</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-amber/20 border border-amber"></div>
          <span className="text-gray-600">Control</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-navy/20 border border-navy"></div>
          <span className="text-gray-600">Output</span>
        </div>
      </div>
    </div>
  );
}
