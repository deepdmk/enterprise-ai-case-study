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

function VectorIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="10" />
      <path d="M12 2v20M2 12h20" />
      <circle cx="12" cy="12" r="4" fill="currentColor" opacity="0.3" />
    </svg>
  );
}

function BrowserIcon({ className }: { className?: string }) {
  return (
    <svg className={cn("w-5 h-5", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="2" y="3" width="20" height="18" rx="2" />
      <line x1="2" y1="9" x2="22" y2="9" />
      <circle cx="6" cy="6" r="1" fill="currentColor" />
      <circle cx="10" cy="6" r="1" fill="currentColor" />
    </svg>
  );
}

function Arrow({ direction = "right", className }: { direction?: "right" | "down"; className?: string }) {
  if (direction === "down") {
    return (
      <svg className={cn("w-4 h-4 text-gray-400", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 5v14M5 12l7 7 7-7" />
      </svg>
    );
  }
  return (
    <svg className={cn("w-4 h-4 text-gray-400", className)} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M5 12h14M12 5l7 7-7 7" />
    </svg>
  );
}

function ProgramBox({ number, title, subtitle }: { number: number; title: string; subtitle: string }) {
  return (
    <div className="bg-navy/5 border border-navy/20 rounded-lg p-2 text-center min-w-0">
      <div className="text-[10px] text-navy/60 font-medium">Program {number}</div>
      <div className="font-bold text-navy text-xs leading-tight">{title}</div>
      <div className="text-[10px] text-gray-500 mt-0.5">{subtitle}</div>
    </div>
  );
}

export function Phase1ArchitectureDiagram() {
  return (
    <div className="w-full py-4 px-4">
      {/* Title */}
      <div className="text-center mb-6">
        <h4 className="text-base font-bold text-navy mb-1">Data Pipeline Architecture</h4>
        <p className="text-xs text-gray-600">Four-program pipeline from source databases to semantic search</p>
      </div>

      {/* Desktop/Tablet Layout - Two Row Grid */}
      <div className="hidden md:block">
        <div className="max-w-3xl mx-auto space-y-6">

          {/* Row 1: Training Pipeline */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Training Pipeline</div>
            <div className="flex items-center gap-2">
              {/* Source DBs */}
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-2 text-center flex-shrink-0 w-24">
                <DatabaseIcon className="mx-auto mb-1 text-gray-600" />
                <div className="font-bold text-gray-700 text-xs">PostgreSQL</div>
                <div className="text-[10px] text-gray-500">3 Databases</div>
              </div>

              <Arrow direction="right" />

              {/* Program 1 */}
              <div className="flex-1 min-w-0">
                <ProgramBox number={1} title="Dataset Generator" subtitle="Extract + Chunk" />
              </div>

              <Arrow direction="right" />

              {/* Training Data */}
              <div className="bg-amber/10 border border-amber/40 rounded-lg p-2 text-center flex-shrink-0 w-24">
                <div className="font-bold text-amber text-xs">Training Data</div>
                <div className="text-[10px] text-amber/70 mt-0.5">train.parquet</div>
                <div className="text-[10px] text-amber/70">val.parquet</div>
              </div>

              <Arrow direction="right" />

              {/* Program 2 */}
              <div className="flex-1 min-w-0">
                <ProgramBox number={2} title="Fine-Tuning" subtitle="Sentence-Transformers" />
              </div>

              <Arrow direction="right" />

              {/* Model Output */}
              <div className="bg-teal border border-teal rounded-lg p-2 text-center flex-shrink-0 w-28">
                <div className="font-bold text-white text-xs">enterprise-embed-v1</div>
                <div className="text-[10px] text-white/80 mt-0.5">Fine-tuned Model</div>
              </div>
            </div>
          </div>

          {/* Row 2: Ingestion & Search Pipeline */}
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Ingestion & Search Pipeline</div>
            <div className="flex items-center gap-2">
              {/* Source DBs */}
              <div className="bg-gray-100 border border-gray-300 rounded-lg p-2 text-center flex-shrink-0 w-24">
                <DatabaseIcon className="mx-auto mb-1 text-gray-600" />
                <div className="font-bold text-gray-700 text-xs">PostgreSQL</div>
                <div className="text-[10px] text-gray-500">Live Data</div>
              </div>

              <Arrow direction="right" />

              {/* Program 3 */}
              <div className="flex-1 min-w-0">
                <ProgramBox number={3} title="Ingestion" subtitle="Chunk + Embed" />
              </div>

              <Arrow direction="right" />

              {/* ChromaDB - Key Design */}
              <div className="bg-teal/10 border-2 border-teal rounded-lg p-2 text-center flex-shrink-0 relative">
                <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-1">
                  <span className="text-[9px] font-bold text-teal">KEY DESIGN</span>
                </div>
                <VectorIcon className="mx-auto mb-1 text-teal" />
                <div className="font-bold text-teal text-xs">ChromaDB</div>
                <div className="flex gap-1 mt-1 justify-center">
                  <span className="bg-teal/20 text-teal rounded px-1 py-0.5 text-[9px]">Embeddings</span>
                  <span className="bg-teal/20 text-teal rounded px-1 py-0.5 text-[9px]">Metadata</span>
                </div>
                <div className="text-[9px] text-teal/60 mt-1">Embeddings only</div>
              </div>

              <Arrow direction="right" />

              {/* Program 4 */}
              <div className="flex-1 min-w-0">
                <ProgramBox number={4} title="Search Interface" subtitle="Gradio UI" />
              </div>

              <Arrow direction="right" />

              {/* User Browser */}
              <div className="bg-navy border border-navy rounded-lg p-2 text-center flex-shrink-0 w-24">
                <BrowserIcon className="mx-auto mb-1 text-white" />
                <div className="font-bold text-white text-xs">User Browser</div>
                <div className="text-[10px] text-white/70">localhost:7860</div>
              </div>
            </div>
          </div>

          {/* Parent Document Retrieval Callout */}
          <div className="bg-amber/5 border border-amber/30 rounded-lg p-3">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-amber flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 16v-4M12 8h.01" />
              </svg>
              <div className="flex-1 min-w-0">
                <div className="font-bold text-navy text-sm">Parent Document Retrieval Pattern</div>
                <p className="text-xs text-gray-600 mt-1">
                  ChromaDB stores only embeddings and metadata. Full document text is retrieved from source PostgreSQL databases at query time, keeping the vector database lean while ensuring data consistency.
                </p>
                <div className="mt-2 flex flex-wrap items-center gap-1 text-[10px]">
                  <span className="bg-navy text-white px-2 py-0.5 rounded">Search Results</span>
                  <span className="text-gray-400">→</span>
                  <span className="bg-teal/20 text-teal px-2 py-0.5 rounded">Metadata</span>
                  <span className="text-gray-400">→</span>
                  <span className="bg-gray-200 text-gray-700 px-2 py-0.5 rounded">PostgreSQL</span>
                  <span className="text-gray-400">→</span>
                  <span className="bg-amber/30 text-amber px-2 py-0.5 rounded">Full Document</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Layout - Vertical Stack */}
      <div className="md:hidden space-y-6">
        {/* Training Pipeline */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Training Pipeline</div>
          <div className="space-y-3">
            {/* Source DBs */}
            <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
              <DatabaseIcon className="mx-auto mb-1 text-gray-600" />
              <div className="font-bold text-gray-700 text-sm">PostgreSQL</div>
              <div className="text-xs text-gray-500">3 Source Databases</div>
            </div>

            <div className="flex justify-center"><Arrow direction="down" /></div>

            <ProgramBox number={1} title="Dataset Generator" subtitle="Extract + Chunk" />

            <div className="flex justify-center"><Arrow direction="down" /></div>

            <div className="bg-amber/10 border border-amber/40 rounded-lg p-3 text-center">
              <div className="font-bold text-amber text-sm">Training Data</div>
              <div className="text-xs text-amber/70">train.parquet, val.parquet</div>
            </div>

            <div className="flex justify-center"><Arrow direction="down" /></div>

            <ProgramBox number={2} title="Fine-Tuning" subtitle="Sentence-Transformers" />

            <div className="flex justify-center"><Arrow direction="down" /></div>

            <div className="bg-teal border border-teal rounded-lg p-3 text-center">
              <div className="font-bold text-white text-sm">enterprise-embed-v1</div>
              <div className="text-xs text-white/80">Fine-tuned Model</div>
            </div>
          </div>
        </div>

        {/* Ingestion & Search Pipeline */}
        <div className="bg-white border border-gray-200 rounded-lg p-3">
          <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Ingestion & Search Pipeline</div>
          <div className="space-y-3">
            <div className="bg-gray-100 border border-gray-300 rounded-lg p-3 text-center">
              <DatabaseIcon className="mx-auto mb-1 text-gray-600" />
              <div className="font-bold text-gray-700 text-sm">PostgreSQL</div>
              <div className="text-xs text-gray-500">Live Data</div>
            </div>

            <div className="flex justify-center"><Arrow direction="down" /></div>

            <ProgramBox number={3} title="Ingestion" subtitle="Chunk + Embed" />

            <div className="flex justify-center"><Arrow direction="down" /></div>

            {/* ChromaDB */}
            <div className="bg-teal/10 border-2 border-teal rounded-lg p-3 text-center relative">
              <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-white px-2">
                <span className="text-[10px] font-bold text-teal">KEY DESIGN</span>
              </div>
              <VectorIcon className="mx-auto mb-1 text-teal" />
              <div className="font-bold text-teal text-sm">ChromaDB</div>
              <div className="flex gap-2 mt-2 justify-center">
                <span className="bg-teal/20 text-teal rounded px-2 py-1 text-xs">Embeddings</span>
                <span className="bg-teal/20 text-teal rounded px-2 py-1 text-xs">Metadata</span>
              </div>
              <div className="text-xs text-teal/60 mt-1">Embeddings only</div>
            </div>

            <div className="flex justify-center"><Arrow direction="down" /></div>

            <ProgramBox number={4} title="Search Interface" subtitle="Gradio UI" />

            <div className="flex justify-center"><Arrow direction="down" /></div>

            <div className="bg-navy border border-navy rounded-lg p-3 text-center">
              <BrowserIcon className="mx-auto mb-1 text-white" />
              <div className="font-bold text-white text-sm">User Browser</div>
              <div className="text-xs text-white/70">localhost:7860</div>
            </div>
          </div>
        </div>

        {/* Parent Document Retrieval */}
        <div className="bg-amber/5 border border-amber/30 rounded-lg p-3">
          <div className="flex items-start gap-2">
            <svg className="w-5 h-5 text-amber flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 16v-4M12 8h.01" />
            </svg>
            <div>
              <div className="font-bold text-navy text-sm">Parent Document Retrieval</div>
              <p className="text-xs text-gray-600 mt-1">
                Text retrieved from source databases at query time via metadata.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap justify-center gap-3 text-[10px]">
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-gray-200 border border-gray-300"></div>
          <span className="text-gray-600">Source</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-navy/10 border border-navy/30"></div>
          <span className="text-gray-600">Programs</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-amber/20 border border-amber"></div>
          <span className="text-gray-600">Data</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-teal border border-teal"></div>
          <span className="text-gray-600">Vector DB</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-2.5 h-2.5 rounded bg-navy border border-navy"></div>
          <span className="text-gray-600">UI</span>
        </div>
      </div>
    </div>
  );
}
