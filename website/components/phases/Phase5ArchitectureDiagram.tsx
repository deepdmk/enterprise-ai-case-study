"use client";

import { cn } from "@/lib/utils";

function DataIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <path d="M14 2v6h6M16 13H8M16 17H8" />
    </svg>
  );
}

function BrainIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M12 2a4 4 0 014 4c0 1.1-.9 2-2 2h-4a2 2 0 01-2-2 4 4 0 014-4z" />
      <path d="M8 8v2a4 4 0 004 4h0a4 4 0 004-4V8" />
      <path d="M6 14a4 4 0 004 4h4a4 4 0 004-4" />
      <path d="M10 18v4M14 18v4" />
    </svg>
  );
}

function UserIcon({ className }: { className?: string }) {
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

export function Phase5ArchitectureDiagram() {
  return (
    <div className="w-full py-4 px-4">
      {/* Title */}
      <div className="text-center mb-6">
        <h4 className="text-base font-bold text-navy mb-1">Orchestrated Agentic System</h4>
        <p className="text-xs text-gray-600">Learned routing trained on Phase 4 discovery data</p>
      </div>

      {/* Desktop/Tablet Layout */}
      <div className="hidden md:block">
        <div className="max-w-3xl mx-auto space-y-4">

          {/* Row 1: Input from Phase 4 */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Input from Phase 4</div>
            <div className="flex items-center justify-center">
              <div className="bg-teal/10 border border-teal rounded-lg p-3 text-center">
                <DataIcon className="mx-auto mb-1 text-teal" />
                <div className="font-bold text-teal text-sm">Discovery Data</div>
                <div className="text-xs text-teal/70 mt-1">90-day A2A logs</div>
                <div className="text-[10px] text-gray-500 mt-1">900 interactions → 71K training examples</div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 2: Training Pipeline */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Training Pipeline</div>
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ProgramBox number={1} title="Data Conversion" subtitle="Logs → ChatML" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={2} title="SLM Fine-tuning" subtitle="LoRA on Qwen2.5-7B" />
              </div>
            </div>
            <div className="mt-3 flex justify-center gap-4 text-[10px] text-gray-500">
              <span>~$20-50 training cost</span>
              <span>•</span>
              <span>4-6 hours on A100</span>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 3: Deployment */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Deployment</div>
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ProgramBox number={3} title="Inference Server" subtitle="vLLM / TGI" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={4} title="Orchestrator Service" subtitle="FastAPI + Agno" />
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 4: Orchestrated System */}
          <div className="bg-magenta/5 border-2 border-magenta rounded-lg p-4 relative">
            <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
              <span className="text-[10px] font-bold text-magenta">ORCHESTRATED SYSTEM</span>
            </div>

            <div className="mt-2 grid grid-cols-5 gap-3 items-center">
              {/* Phase 1 Embedding */}
              <div className="bg-navy/10 border border-navy rounded-lg p-2 text-center">
                <div className="text-[9px] text-navy/60 font-medium">Phase 1</div>
                <div className="font-bold text-navy text-[10px]">Embedding</div>
                <div className="text-[9px] text-navy/70">RAG</div>
              </div>

              {/* Orchestrator in center */}
              <div className="col-span-3 bg-magenta border border-magenta rounded-lg p-3 text-center">
                <BrainIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-sm">Orchestrator</div>
                <div className="text-[10px] text-white/80">Qwen2.5-7B (fine-tuned)</div>
                <div className="text-[9px] text-white/60 mt-1">Learned routing • 94% accuracy • ~150ms</div>
              </div>

              {/* User Access */}
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-2 text-center">
                <UserIcon className="mx-auto mb-1 text-gray-600" />
                <div className="font-bold text-gray-700 text-[10px]">Single</div>
                <div className="text-[9px] text-gray-500">Window</div>
              </div>
            </div>

            {/* Agents row */}
            <div className="mt-3 flex items-center justify-center gap-2">
              <div className="text-[9px] text-gray-500">Coordinates:</div>
              <div className="bg-teal/20 border border-teal/40 rounded px-2 py-1 text-center">
                <div className="font-bold text-teal text-[10px]">Fundraising</div>
                <div className="text-[9px] text-teal/70">Agent</div>
              </div>
              <div className="bg-amber/20 border border-amber/40 rounded px-2 py-1 text-center">
                <div className="font-bold text-amber text-[10px]">Business Dev</div>
                <div className="text-[9px] text-amber/70">Agent</div>
              </div>
              <div className="bg-navy/20 border border-navy/40 rounded px-2 py-1 text-center">
                <div className="font-bold text-navy text-[10px]">Field Ops</div>
                <div className="text-[9px] text-navy/70">Agent</div>
              </div>
            </div>
          </div>

          {/* Key insight callout */}
          <div className="bg-magenta/5 border border-magenta/30 rounded-lg p-3">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-magenta flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 16v-4M12 8h.01" />
              </svg>
              <div className="flex-1 min-w-0">
                <div className="font-bold text-navy text-sm">Single-Window Enterprise AI</div>
                <p className="text-xs text-gray-600 mt-1">
                  Users make requests without knowing which agents, models, or divisions are involved. The orchestrator handles coordination automatically using patterns learned from Phase 4&apos;s discovery.
                </p>
                <div className="mt-2 flex flex-wrap items-center gap-2 text-[10px]">
                  <span className="bg-navy/10 text-navy px-2 py-0.5 rounded">Model-agnostic</span>
                  <span className="bg-navy/10 text-navy px-2 py-0.5 rounded">Local → Cloud portable</span>
                  <span className="bg-navy/10 text-navy px-2 py-0.5 rounded">$163.1K Direct Investment</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Mobile Layout */}
      <div className="md:hidden space-y-4">
        {/* Input */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">From Phase 4</div>
          <div className="bg-teal/10 border border-teal rounded-lg p-2 text-center">
            <div className="font-bold text-teal text-sm">Discovery Data</div>
            <div className="text-xs text-teal/70">90-day logs → 71K examples</div>
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Training */}
        <div className="bg-white border border-gray-200 rounded-lg p-3 space-y-2">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Training</div>
          <ProgramBox number={1} title="Data Conversion" subtitle="Logs → ChatML" />
          <div className="flex justify-center"><Arrow direction="down" /></div>
          <ProgramBox number={2} title="SLM Fine-tuning" subtitle="LoRA on Qwen2.5-7B" />
          <div className="text-center text-[10px] text-gray-500 mt-2">~$20-50 • 4-6 hours</div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Deployment */}
        <div className="bg-white border border-gray-200 rounded-lg p-3 space-y-2">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Deployment</div>
          <ProgramBox number={3} title="Inference Server" subtitle="vLLM / TGI" />
          <div className="flex justify-center"><Arrow direction="down" /></div>
          <ProgramBox number={4} title="Orchestrator Service" subtitle="FastAPI + Agno" />
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Orchestrated System */}
        <div className="bg-magenta/5 border-2 border-magenta rounded-lg p-3 relative">
          <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
            <span className="text-[10px] font-bold text-magenta">ORCHESTRATED SYSTEM</span>
          </div>

          <div className="mt-2 space-y-3">
            {/* Orchestrator */}
            <div className="bg-magenta border border-magenta rounded-lg p-3 text-center">
              <BrainIcon className="mx-auto mb-1 text-white" />
              <div className="font-bold text-white text-sm">Orchestrator</div>
              <div className="text-xs text-white/80">Qwen2.5-7B • 94% accuracy</div>
            </div>

            {/* Agents */}
            <div className="grid grid-cols-3 gap-2">
              <div className="bg-teal/20 border border-teal/40 rounded p-1.5 text-center">
                <div className="font-bold text-teal text-[10px]">FR</div>
              </div>
              <div className="bg-amber/20 border border-amber/40 rounded p-1.5 text-center">
                <div className="font-bold text-amber text-[10px]">BD</div>
              </div>
              <div className="bg-navy/20 border border-navy/40 rounded p-1.5 text-center">
                <div className="font-bold text-navy text-[10px]">FO</div>
              </div>
            </div>

            {/* RAG + User */}
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-navy/10 border border-navy rounded p-1.5 text-center">
                <div className="font-bold text-navy text-[10px]">Phase 1 RAG</div>
              </div>
              <div className="bg-gray-100 border border-gray-300 rounded p-1.5 text-center">
                <div className="font-bold text-gray-700 text-[10px]">Single Window</div>
              </div>
            </div>
          </div>
        </div>

        {/* Key insight */}
        <div className="bg-magenta/5 border border-magenta/30 rounded-lg p-3">
          <div className="font-bold text-navy text-sm">Single-Window Enterprise AI</div>
          <p className="text-xs text-gray-600 mt-1">
            Learned routing from discovery. $163.1K total Direct Investment.
          </p>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap justify-center gap-3 text-[10px]">
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-teal/20 border border-teal"></div>
          <span className="text-gray-600">Phase 4 Input</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-magenta/10 border border-magenta/30"></div>
          <span className="text-gray-600">Programs</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-magenta border border-magenta"></div>
          <span className="text-gray-600">Orchestrator</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-navy/20 border border-navy"></div>
          <span className="text-gray-600">RAG</span>
        </div>
      </div>
    </div>
  );
}
