"use client";

import { cn } from "@/lib/utils";

function DataIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
    </svg>
  );
}

function ModelIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M12 2L2 7l10 5 10-5-10-5z" />
      <path d="M2 17l10 5 10-5M2 12l10 5 10-5" />
    </svg>
  );
}

function RegistryIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <path d="M3 9h18M9 21V9" />
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
    <div className="bg-amber/5 border border-amber/20 rounded-lg p-2 text-center min-w-0">
      <div className="text-[10px] text-amber/60 font-medium">Program {number}</div>
      <div className="font-bold text-amber text-xs leading-tight">{title}</div>
      <div className="text-[10px] text-gray-500 mt-0.5">{subtitle}</div>
    </div>
  );
}

export function Phase2ArchitectureDiagram() {
  return (
    <div className="w-full py-4 px-4">
      {/* Title */}
      <div className="text-center mb-6">
        <h4 className="text-base font-bold text-navy mb-1">Task SLM Training Pipeline</h4>
        <p className="text-xs text-gray-600">Fine-tune 14 task-specific models using Unsloth + LoRA</p>
      </div>

      {/* Desktop/Tablet Layout */}
      <div className="hidden md:block">
        <div className="max-w-3xl mx-auto space-y-4">

          {/* Row 1: Input Data */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Training Data Input</div>
            <div className="flex items-center justify-center gap-4">
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
                <DataIcon className="mx-auto mb-1 text-gray-600" />
                <div className="font-bold text-gray-700 text-sm">Task Examples</div>
                <div className="text-xs text-gray-500 mt-1">500-2000 examples per task</div>
                <div className="text-[10px] text-gray-400 mt-1">JSONL format (instruction → output)</div>
              </div>
              <div className="text-center">
                <div className="text-[10px] text-gray-500 mb-1">Base Model</div>
                <div className="bg-navy/10 border border-navy/30 rounded px-2 py-1">
                  <span className="text-[10px] font-mono text-navy">Llama 3.1 8B (4-bit)</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 2: Training Pipeline */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Training Pipeline (per task)</div>
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ProgramBox number={1} title="Data Prep" subtitle="Format & validate" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={2} title="Fine-Tuning" subtitle="Unsloth + LoRA" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={3} title="Evaluation" subtitle="Test & metrics" />
              </div>
              <Arrow direction="right" />
              <div className="flex-1">
                <ProgramBox number={4} title="Registry" subtitle="Version & export" />
              </div>
            </div>
            <div className="mt-3 flex justify-center gap-4 text-[10px] text-gray-500">
              <span>~1 hour per model</span>
              <span>•</span>
              <span>~$214 compute</span>
              <span>•</span>
              <span>LoRA adapters (~40MB)</span>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 3: 14 Task SLMs */}
          <div className="bg-amber/5 border-2 border-amber rounded-lg p-4 relative">
            <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
              <span className="text-[10px] font-bold text-amber">14 TASK SLMs</span>
            </div>
            <div className="grid grid-cols-3 gap-3 mt-2">
              {/* Fundraising */}
              <div className="bg-teal/10 border border-teal rounded-lg p-3">
                <div className="font-bold text-teal text-xs text-center mb-2">Fundraising</div>
                <div className="space-y-1 text-[9px] text-teal/80">
                  <div className="bg-teal/10 rounded px-1.5 py-0.5">Investor Profiling</div>
                  <div className="bg-teal/10 rounded px-1.5 py-0.5">Fit Assessment</div>
                  <div className="bg-teal/10 rounded px-1.5 py-0.5">Capacity Analysis</div>
                  <div className="bg-teal/10 rounded px-1.5 py-0.5">Engagement Strategy</div>
                  <div className="bg-teal/10 rounded px-1.5 py-0.5">Portfolio Synthesis</div>
                </div>
                <div className="text-center mt-2 text-[10px] text-teal font-medium">5 models</div>
              </div>

              {/* Business Development */}
              <div className="bg-amber/10 border border-amber rounded-lg p-3">
                <div className="font-bold text-amber text-xs text-center mb-2">Business Dev</div>
                <div className="space-y-1 text-[9px] text-amber/80">
                  <div className="bg-amber/10 rounded px-1.5 py-0.5">RFP Analysis</div>
                  <div className="bg-amber/10 rounded px-1.5 py-0.5">Competitive Positioning</div>
                  <div className="bg-amber/10 rounded px-1.5 py-0.5">Proposal Drafting</div>
                  <div className="bg-amber/10 rounded px-1.5 py-0.5">Win Probability</div>
                  <div className="bg-amber/10 rounded px-1.5 py-0.5">Funder Priorities</div>
                </div>
                <div className="text-center mt-2 text-[10px] text-amber font-medium">5 models</div>
              </div>

              {/* Field Operations */}
              <div className="bg-navy/10 border border-navy rounded-lg p-3">
                <div className="font-bold text-navy text-xs text-center mb-2">Field Ops</div>
                <div className="space-y-1 text-[9px] text-navy/80">
                  <div className="bg-navy/10 rounded px-1.5 py-0.5">Market Assessment</div>
                  <div className="bg-navy/10 rounded px-1.5 py-0.5">Project Performance</div>
                  <div className="bg-navy/10 rounded px-1.5 py-0.5">Capacity Mapping</div>
                  <div className="bg-navy/10 rounded px-1.5 py-0.5">Demand Forecasting</div>
                </div>
                <div className="text-center mt-2 text-[10px] text-navy font-medium">4 models</div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><Arrow direction="down" /></div>

          {/* Row 4: Output to Phase 3 */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Output to Phase 3</div>
            <div className="flex items-center justify-center gap-4">
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
                <RegistryIcon className="mx-auto mb-1 text-gray-600" />
                <div className="font-bold text-gray-700 text-sm">Model Registry</div>
                <div className="text-xs text-gray-500 mt-1">14 registered adapters</div>
              </div>
              <Arrow direction="right" />
              <div className="bg-magenta/10 border border-magenta rounded-lg p-3 text-center">
                <ModelIcon className="mx-auto mb-1 text-magenta" />
                <div className="font-bold text-magenta text-sm">Phase 3 MoE</div>
                <div className="text-xs text-magenta/70 mt-1">Expert merge input</div>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Mobile Layout */}
      <div className="md:hidden space-y-4">
        {/* Input */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Input</div>
          <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
            <DataIcon className="mx-auto mb-1 text-gray-600" />
            <div className="font-bold text-gray-700 text-sm">Task Examples</div>
            <div className="text-xs text-gray-500">500-2000 per task • Llama 3.1 8B base</div>
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Programs */}
        <div className="bg-white border border-gray-200 rounded-lg p-3 space-y-2">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Training Pipeline</div>
          <div className="grid grid-cols-2 gap-2">
            <ProgramBox number={1} title="Data Prep" subtitle="Format & validate" />
            <ProgramBox number={2} title="Fine-Tuning" subtitle="Unsloth + LoRA" />
            <ProgramBox number={3} title="Evaluation" subtitle="Test & metrics" />
            <ProgramBox number={4} title="Registry" subtitle="Version & export" />
          </div>
          <div className="text-center text-[10px] text-gray-500 mt-2">
            ~1 hour • ~$214 compute per model
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* 14 Task SLMs */}
        <div className="bg-amber/5 border-2 border-amber rounded-lg p-3 relative">
          <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
            <span className="text-[10px] font-bold text-amber">14 TASK SLMs</span>
          </div>
          <div className="space-y-2 mt-2">
            <div className="bg-teal/10 border border-teal rounded-lg p-2 text-center">
              <div className="font-bold text-teal text-sm">Fundraising</div>
              <div className="text-xs text-teal/70">5 models: profiling, fit, capacity, engagement, portfolio</div>
            </div>
            <div className="bg-amber/10 border border-amber rounded-lg p-2 text-center">
              <div className="font-bold text-amber text-sm">Business Dev</div>
              <div className="text-xs text-amber/70">5 models: RFP, competitive, proposal, win prob, priorities</div>
            </div>
            <div className="bg-navy/10 border border-navy rounded-lg p-2 text-center">
              <div className="font-bold text-navy text-sm">Field Ops</div>
              <div className="text-xs text-navy/70">4 models: market, performance, capacity, forecasting</div>
            </div>
          </div>
        </div>

        <div className="flex justify-center"><Arrow direction="down" /></div>

        {/* Output */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Output</div>
          <div className="flex items-center justify-center gap-2">
            <div className="bg-gray-100 border border-gray-300 rounded-lg p-2 text-center flex-1">
              <div className="font-bold text-gray-700 text-xs">Registry</div>
              <div className="text-[10px] text-gray-500">14 adapters</div>
            </div>
            <Arrow direction="right" />
            <div className="bg-magenta/10 border border-magenta rounded-lg p-2 text-center flex-1">
              <div className="font-bold text-magenta text-xs">Phase 3</div>
              <div className="text-[10px] text-magenta/70">MoE input</div>
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
          <div className="w-2.5 h-2.5 rounded bg-amber/10 border border-amber/30"></div>
          <span className="text-gray-600">Programs</span>
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
