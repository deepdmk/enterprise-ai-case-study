"use client";

import { cn } from "@/lib/utils";

function DatabaseIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
    </svg>
  );
}

function FileIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
      <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
    </svg>
  );
}

function ExperimentIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M9 3h6M12 3v5M5 8h14l-2 13H7L5 8z" />
      <path d="M9 13h6" />
    </svg>
  );
}

function ModelIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <path d="M9 9h6M9 12h6M9 15h4" />
    </svg>
  );
}

function ArrowDown({ className }: { className?: string }) {
  return (
    <svg className={cn("w-4 h-4 text-gray-400", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M12 5v14M5 12l7 7 7-7" />
    </svg>
  );
}

function RegistryBox({
  title,
  subtitle,
  icon,
  color
}: {
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  color: "model" | "data" | "experiment";
}) {
  const colors = {
    model: "bg-navy/10 border-navy text-navy",
    data: "bg-teal/10 border-teal text-teal",
    experiment: "bg-amber/10 border-amber text-amber",
  };

  return (
    <div className={cn("border rounded-lg p-3 text-center flex-1", colors[color])}>
      <div className="flex justify-center mb-1">{icon}</div>
      <div className="font-bold text-sm">{title}</div>
      <div className="text-[10px] opacity-70 mt-0.5">{subtitle}</div>
    </div>
  );
}

function PhaseConsumerBox({ phase, description }: { phase: number; description: string }) {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded px-2 py-1.5 text-center">
      <div className="text-[10px] text-gray-500 font-medium">Phase {phase}</div>
      <div className="text-[9px] text-gray-600">{description}</div>
    </div>
  );
}

export function Phase0ArchitectureDiagram() {
  return (
    <div className="w-full py-4 px-4">
      {/* Title */}
      <div className="text-center mb-6">
        <h4 className="text-base font-bold text-navy mb-1">Three Registry Architecture</h4>
        <p className="text-xs text-gray-600">File-based registries with shared IDs enabling all phases</p>
      </div>

      {/* Desktop/Tablet Layout */}
      <div className="hidden md:block">
        <div className="max-w-3xl mx-auto space-y-4">

          {/* Row 1: JSONStorage Foundation */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Storage Backend</div>
            <div className="flex items-center justify-center">
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
                <FileIcon className="mx-auto mb-1 text-gray-600" />
                <div className="font-bold text-gray-700 text-sm">JSONStorage</div>
                <div className="text-xs text-gray-500 mt-1">Thread-safe file locking</div>
                <div className="flex gap-2 mt-2 justify-center">
                  <span className="bg-white text-gray-600 rounded px-1.5 py-0.5 text-[9px] border border-gray-200">filelock</span>
                  <span className="bg-white text-gray-600 rounded px-1.5 py-0.5 text-[9px] border border-gray-200">Pydantic</span>
                  <span className="bg-white text-gray-600 rounded px-1.5 py-0.5 text-[9px] border border-gray-200">structlog</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-center"><ArrowDown /></div>

          {/* Row 2: Three Registries */}
          <div className="bg-navy/5 border-2 border-navy rounded-lg p-4 relative">
            <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
              <span className="text-[10px] font-bold text-navy">THREE REGISTRIES</span>
            </div>
            <div className="flex items-stretch gap-3 mt-2">
              <RegistryBox
                title="DataRegistry"
                subtitle="Tracks datasets"
                icon={<DatabaseIcon className="text-teal" />}
                color="data"
              />
              <RegistryBox
                title="ModelRegistry"
                subtitle="Versions models"
                icon={<ModelIcon className="text-navy" />}
                color="model"
              />
              <RegistryBox
                title="ExperimentTracker"
                subtitle="Logs training runs"
                icon={<ExperimentIcon className="text-amber" />}
                color="experiment"
              />
            </div>

            {/* Shared IDs connector */}
            <div className="mt-4 bg-white border border-gray-200 rounded-lg p-2 text-center">
              <div className="text-[10px] text-gray-500 font-medium mb-1">Shared ID Format</div>
              <code className="text-xs text-navy bg-navy/5 px-2 py-1 rounded">
                {"{phase}/{unit}/{task}/{version}"}
              </code>
              <div className="text-[9px] text-gray-500 mt-1">e.g., 2/fundraising/portfolio-analysis/v1.0.0</div>
            </div>
          </div>

          <div className="flex justify-center"><ArrowDown /></div>

          {/* Row 3: Phase Consumers */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Enables All Phases</div>
            <div className="grid grid-cols-5 gap-2">
              <PhaseConsumerBox phase={1} description="Embeddings" />
              <PhaseConsumerBox phase={2} description="Task SLMs" />
              <PhaseConsumerBox phase={3} description="MoE Routing" />
              <PhaseConsumerBox phase={4} description="Discovery" />
              <PhaseConsumerBox phase={5} description="Orchestrator" />
            </div>
            <div className="mt-3 flex justify-center gap-4 text-[10px] text-gray-500">
              <span>Register datasets</span>
              <span>•</span>
              <span>Track models</span>
              <span>•</span>
              <span>Log experiments</span>
              <span>•</span>
              <span>Query lineage</span>
            </div>
          </div>

          {/* Key insight callout */}
          <div className="bg-navy/5 border border-navy/30 rounded-lg p-3">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-navy flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 16v-4M12 8h.01" />
              </svg>
              <div className="flex-1 min-w-0">
                <div className="font-bold text-navy text-sm">Zero-Cost Foundation</div>
                <p className="text-xs text-gray-600 mt-1">
                  File-based storage with thread-safe locking—no database infrastructure required. 151 passing tests validate production-ready reliability. Everything is traceable through shared IDs.
                </p>
                <div className="mt-2 flex flex-wrap items-center gap-2 text-[10px]">
                  <span className="bg-navy/10 text-navy px-2 py-0.5 rounded">$0 cost</span>
                  <span className="bg-navy/10 text-navy px-2 py-0.5 rounded">~2 hours setup</span>
                  <span className="bg-navy/10 text-navy px-2 py-0.5 rounded">151 tests passing</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Mobile Layout */}
      <div className="md:hidden space-y-4">
        {/* Storage */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Storage</div>
          <div className="bg-gray-100 border border-gray-300 rounded-lg p-2 text-center">
            <FileIcon className="mx-auto mb-1 text-gray-600" />
            <div className="font-bold text-gray-700 text-sm">JSONStorage</div>
            <div className="text-xs text-gray-500">Thread-safe file locking</div>
          </div>
        </div>

        <div className="flex justify-center"><ArrowDown /></div>

        {/* Registries */}
        <div className="bg-navy/5 border-2 border-navy rounded-lg p-3 relative">
          <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
            <span className="text-[10px] font-bold text-navy">3 REGISTRIES</span>
          </div>
          <div className="space-y-2 mt-2">
            <div className="bg-teal/10 border border-teal rounded-lg p-2 text-center">
              <div className="font-bold text-teal text-sm">DataRegistry</div>
              <div className="text-xs text-teal/70">Tracks datasets + lineage</div>
            </div>
            <div className="bg-navy/10 border border-navy rounded-lg p-2 text-center">
              <div className="font-bold text-navy text-sm">ModelRegistry</div>
              <div className="text-xs text-navy/70">Versions models + metrics</div>
            </div>
            <div className="bg-amber/10 border border-amber rounded-lg p-2 text-center">
              <div className="font-bold text-amber text-sm">ExperimentTracker</div>
              <div className="text-xs text-amber/70">Logs training runs</div>
            </div>
          </div>

          <div className="mt-3 bg-white border border-gray-200 rounded p-2 text-center">
            <div className="text-[10px] text-gray-500 font-medium">Shared ID Format</div>
            <code className="text-[10px] text-navy">{"{phase}/{unit}/{task}/{version}"}</code>
          </div>
        </div>

        <div className="flex justify-center"><ArrowDown /></div>

        {/* Phase Consumers */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Enables</div>
          <div className="grid grid-cols-5 gap-1">
            <div className="bg-gray-50 border border-gray-200 rounded p-1 text-center">
              <div className="text-[10px] font-bold text-gray-700">P1</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-1 text-center">
              <div className="text-[10px] font-bold text-gray-700">P2</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-1 text-center">
              <div className="text-[10px] font-bold text-gray-700">P3</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-1 text-center">
              <div className="text-[10px] font-bold text-gray-700">P4</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-1 text-center">
              <div className="text-[10px] font-bold text-gray-700">P5</div>
            </div>
          </div>
        </div>

        {/* Key insight */}
        <div className="bg-navy/5 border border-navy/30 rounded-lg p-3">
          <div className="font-bold text-navy text-sm">Zero-Cost Foundation</div>
          <p className="text-xs text-gray-600 mt-1">
            $0 cost • ~2 hours setup • 151 tests passing
          </p>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap justify-center gap-3 text-[10px]">
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-gray-200 border border-gray-300"></div>
          <span className="text-gray-600">Storage</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-teal/20 border border-teal"></div>
          <span className="text-gray-600">Data</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-navy/20 border border-navy"></div>
          <span className="text-gray-600">Models</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-amber/20 border border-amber"></div>
          <span className="text-gray-600">Experiments</span>
        </div>
      </div>
    </div>
  );
}
