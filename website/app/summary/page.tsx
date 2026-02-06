import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout";
import { PageNav } from "@/components/layout/PageNav";
import Link from "next/link";

export const metadata = {
  title: "Case Study Overview",
  description:
    "A phased transformation delivering value at every milestone without $2M gambles or vendor lock-in. How a mid-market organization can build strategic AI capabilities through incremental deployment and bounded risk.",
};

export default function SummaryPage() {
  return (
    <>
      <PageHeader
        title="Building Unique AI Capabilities Through the Company's Data and People"
        subtitle="A phased transformation delivering value at every milestone without $2M gambles or vendor lock-in"
      />
      <PageNav current="/summary" />

      {/* ==================== KEY METRICS STRIP ==================== */}
      <section className="py-8 bg-navy/5 border-b border-navy/10">
        <Container>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-3xl md:text-4xl font-bold text-navy">$163.1K</div>
              <div className="text-sm text-gray-600 mt-1">Direct Investment</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold text-teal">6 phases</div>
              <div className="text-sm text-gray-600 mt-1">With Exit Optionality</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold text-amber">18 months</div>
              <div className="text-sm text-gray-600 mt-1">Full System Timeline</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold text-magenta">$11,100</div>
              <div className="text-sm text-gray-600 mt-1">Infrastructure Cost</div>
            </div>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 1: THE CHALLENGE ==================== */}
      <section className="py-16 bg-navy text-white border-t-4 border-amber">
        <Container>
          <h2 className="text-3xl md:text-4xl font-bold mb-8">The Challenge</h2>

          {/* The Stakes */}
          <div className="mb-10">
            <h3 className="text-xl font-semibold mb-4 text-amber">The Stakes</h3>
            <p className="text-lg text-white/90 mb-4">
              The organization faces a sudden sector upheaval creating three compounding crises:
            </p>
            <ul className="space-y-2 text-white/80">
              <li className="flex items-start gap-3">
                <span className="text-amber font-bold">1.</span>
                <span><strong className="text-white">Competitive survival pressure</strong> from market consolidation forcing competitors into each other&apos;s spaces</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-amber font-bold">2.</span>
                <span><strong className="text-white">Financial crisis</strong> with projected 50% revenue decline over two years</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-amber font-bold">3.</span>
                <span><strong className="text-white">Deep organizational skepticism</strong> from a failed transformation and staff reductions</span>
              </li>
            </ul>
          </div>

          {/* The Dilemma */}
          <div className="mb-10">
            <h3 className="text-xl font-semibold mb-4 text-amber">The Dilemma</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white/10 rounded-lg p-5">
                <h4 className="font-semibold text-amber mb-2">Competitive Survival</h4>
                <p className="text-white/80 text-sm">
                  Unable to compete on price or speed, the organization had to leverage its core strengths: institutional knowledge, client relationships, and contextual expertise built over decades. But this knowledge was fragmented across regions and divisions — locked away while competitors gained ground.
                </p>
              </div>
              <div className="bg-white/10 rounded-lg p-5">
                <h4 className="font-semibold text-amber mb-2">Financial &amp; Timing Mismatch</h4>
                <p className="text-white/80 text-sm">
                  Traditional AI platforms require 3-4 years to deliver ROI. But with 50% revenue decline projected over two years, the organization was fighting for survival. By the time a vendor platform delivered value, the market might have consolidated. The C-suite couldn&apos;t approve $2M+ upfront bets; the board demanded proof of prudent spending, not multi-year gambles.
                </p>
              </div>
              <div className="bg-white/10 rounded-lg p-5">
                <h4 className="font-semibold text-amber mb-2">Change Fatigue</h4>
                <p className="text-white/80 text-sm">
                  A failed top-down transformation had damaged trust. Staff felt it added burden rather than relief, and layoffs left remaining employees overwhelmed. In a decentralized, relational culture, you cannot mandate adoption. Any solution requiring &ldquo;trust us, this will help&rdquo; would fail.
                </p>
              </div>
            </div>
          </div>

          {/* The Question */}
          <div className="bg-amber/20 border-l-4 border-amber rounded-r-lg p-6 mb-8">
            <h3 className="text-lg font-semibold mb-2 text-amber">The Question</h3>
            <p className="text-lg text-white italic">
              How can an organization deploy enterprise AI to leverage its institutional knowledge advantage, deliver immediate ROI, and rebuild trust with change-fatigued international teams — without top-down mandates, multi-million dollar investments, or degrading its competitive advantage?
            </p>
          </div>

          <Link
            href="/challenge"
            className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-amber/10 hover:text-white text-navy font-semibold rounded-lg transition-colors"
          >
            See the full challenge analysis
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </Container>
      </section>

      {/* ==================== SECTION 2: THE APPROACH ==================== */}
      <section className="py-16 bg-white border-t-4 border-teal">
        <Container>
          <h2 className="text-3xl md:text-4xl font-bold text-navy mb-8">The Approach</h2>

          <div className="space-y-6 mb-10">
            {/* Strategic Analysis */}
            <div className="bg-teal/5 border border-gray-200 border-t-4 border-t-teal rounded-lg p-6">
              <h3 className="text-lg font-bold text-navy mb-3">Strategic Analysis</h3>
              <p className="text-gray-700 mb-3">
                Three independent analyses defined the situation: stakeholder consultations to reveal needs, organizational assessment (7S + SWOT) to expose cultural and capability realities, and competitive analysis (Five Forces) to identify market imperatives. Together, these produced 19 Critical to Quality requirements that any solution must satisfy.
              </p>
            </div>

            {/* Strategy Selection */}
            <div className="bg-teal/5 border border-gray-200 border-t-4 border-t-teal rounded-lg p-6">
              <h3 className="text-lg font-bold text-navy mb-3">Strategy Selection</h3>
              <p className="text-gray-700 mb-3">
                Strategic alternatives were evaluated against all 19 CTQs using Pugh Matrix analysis. The selected approach: <strong className="text-navy">Phased Internal Build</strong> — proprietary AI built internally with existing staff through progressive deployment and self-initiated adoption. This approach satisfies stakeholder, competitive, and organizational requirements simultaneously.
              </p>
            </div>

            {/* Transformation Planning */}
            <div className="bg-teal/5 border border-gray-200 border-t-4 border-t-teal rounded-lg p-6">
              <h3 className="text-lg font-bold text-navy mb-3">Transformation Planning</h3>
              <p className="text-gray-700 mb-3">
                The strategic approach alone couldn&apos;t satisfy all 19 CTQs. Many depended on how the transformation was timed and implemented. Three Horizons provided staging with decision points, Roadmap integrated technical and change management workstreams, and Balanced Scorecard enabled data-driven decisions at each phase boundary.
              </p>
              <p className="text-gray-700">
                The result: an <strong className="text-navy">18-month, six-phase implementation plan</strong> that builds progressively from bottom-up value, delivers ROI at every phase, and preserves optionality throughout so the organization can stop at any point and retain the value already created.
              </p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              href="/strategy"
              className="inline-flex items-center justify-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
            >
              See the full strategic analysis
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
            <Link
              href="/transformation"
              className="inline-flex items-center justify-center px-6 py-3 bg-transparent hover:bg-teal/10 text-teal font-semibold rounded-lg border-2 border-teal transition-colors"
            >
              See the transformation framework
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 3: THE SOLUTION ==================== */}
      <section className="py-16 bg-slate-100 border-t-4 border-navy">
        <Container>
          <h2 className="text-3xl md:text-4xl font-bold text-navy mb-4">The Solution</h2>
          <p className="text-lg text-gray-700 mb-8 max-w-3xl">
            Six phases of progressive capability building with value delivered at each stage and optionality maintained throughout.
          </p>

          {/* Core Strategy Card */}
          <div className="bg-white border-l-4 border-navy rounded-r-lg shadow-md p-6 mb-10">
            <h3 className="text-lg font-bold text-navy mb-3">Core Strategy: Invert the Playbook</h3>
            <p className="text-gray-700 mb-3">
              Rather than mandating a platform from headquarters, we start where the burden is worst: overwhelmed teams struggling to find institutional knowledge trapped in silos across regions and divisions. Build immediate relief first, then let demonstrated value drive organic adoption.
            </p>
            <p className="text-gray-600 text-sm">
              Each phase builds on proven success, not projected ROI. The organization can stop at any point, keep everything already built, and face no sunk cost.
            </p>
          </div>

          {/* Six-Phase Implementation */}
          <h3 className="text-xl font-bold text-navy mb-4">Six-Phase Implementation</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {/* Phase 0 */}
            <div className="bg-white border border-gray-200 border-t-4 border-t-gray-400 rounded-lg shadow-md p-5">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Phase 0</span>
              <h4 className="text-lg font-bold text-navy mt-1 mb-2">Infrastructure Foundation</h4>
              <p className="text-sm text-gray-600 mb-2">Data pipeline and staging infrastructure</p>
              <p className="text-sm text-gray-500">
                Foundational registries that track models, datasets, and experiments enabling systematic learning across all phases.
              </p>
            </div>

            {/* Phase 1 */}
            <div className="bg-white border border-gray-200 border-t-4 border-t-teal rounded-lg shadow-md p-5">
              <span className="text-xs font-semibold text-teal uppercase tracking-wide">Phase 1</span>
              <h4 className="text-lg font-bold text-navy mt-1 mb-2">Unified Embedding Space</h4>
              <p className="text-sm text-gray-600 mb-2">Shared semantic infrastructure</p>
              <p className="text-sm text-gray-500">
                Employees find relevant documents across any division, country, or language through AI-powered semantic search.
              </p>
            </div>

            {/* Phase 2 */}
            <div className="bg-white border border-gray-200 border-t-4 border-t-amber rounded-lg shadow-md p-5">
              <span className="text-xs font-semibold text-amber uppercase tracking-wide">Phase 2</span>
              <h4 className="text-lg font-bold text-navy mt-1 mb-2">Task-Specific SLMs</h4>
              <p className="text-sm text-gray-600 mb-2">Fine-tuned small language models</p>
              <p className="text-sm text-gray-500">
                Employees get intelligent assistance for the work they prioritize, from 15 models trained on the organization&apos;s workflows.
              </p>
            </div>

            {/* Phase 3 */}
            <div className="bg-white border border-gray-200 border-t-4 border-t-magenta rounded-lg shadow-md p-5">
              <span className="text-xs font-semibold text-magenta uppercase tracking-wide">Phase 3</span>
              <h4 className="text-lg font-bold text-navy mt-1 mb-2">MoE Division Agents</h4>
              <p className="text-sm text-gray-600 mb-2">Mixture-of-Experts models</p>
              <p className="text-sm text-gray-500">
                Each division gets expert AI that handles many tasks to the organization&apos;s standards, combining specialized assistants into one agent.
              </p>
            </div>

            {/* Phase 4 */}
            <div className="bg-white border border-gray-200 border-t-4 border-t-teal rounded-lg shadow-md p-5">
              <span className="text-xs font-semibold text-teal uppercase tracking-wide">Phase 4</span>
              <h4 className="text-lg font-bold text-navy mt-1 mb-2">Agentic Discovery</h4>
              <p className="text-sm text-gray-600 mb-2">A2A protocol for collaboration</p>
              <p className="text-sm text-gray-500">
                Agents learn to use information across divisions, sharing capabilities to enhance each other&apos;s work.
              </p>
            </div>

            {/* Phase 5 */}
            <div className="bg-white border border-gray-200 border-t-4 border-t-navy rounded-lg shadow-md p-5">
              <span className="text-xs font-semibold text-navy uppercase tracking-wide">Phase 5</span>
              <h4 className="text-lg font-bold text-navy mt-1 mb-2">Orchestrated System</h4>
              <p className="text-sm text-gray-600 mb-2">SLM orchestrator</p>
              <p className="text-sm text-gray-500">
                Employees engage through a single AI window that leverages data and capabilities across the enterprise, tailored to the organization&apos;s knowledge.
              </p>
            </div>
          </div>

          <Link
            href="/solution"
            className="inline-flex items-center justify-center px-6 py-3 bg-navy hover:bg-navy/90 text-white font-semibold rounded-lg transition-colors"
          >
            See the detailed implementation
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </Container>
      </section>

      {/* ==================== SECTION 4: THE RESULTS ==================== */}
      <section className="py-16 bg-teal/10 border-t-4 border-teal">
        <Container>
          <h2 className="text-3xl md:text-4xl font-bold text-navy mb-8">The Results</h2>

          {/* Investment Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
            <div className="bg-white border border-gray-200 rounded-lg shadow-md p-6 text-center">
              <div className="text-3xl font-bold text-navy mb-1">$11,100</div>
              <div className="text-sm font-semibold text-gray-700">Infrastructure</div>
              <p className="text-xs text-gray-500 mt-1">GPU compute, storage, vector DB, monitoring</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg shadow-md p-6 text-center">
              <div className="text-3xl font-bold text-navy mb-1">$152,000</div>
              <div className="text-sm font-semibold text-gray-700">Training Programs</div>
              <p className="text-xs text-gray-500 mt-1">User training, change management for 8,000 staff</p>
            </div>
            <div className="bg-teal/10 border-2 border-teal rounded-lg shadow-md p-6 text-center">
              <div className="text-3xl font-bold text-teal mb-1">$163,100</div>
              <div className="text-sm font-semibold text-gray-700">Total Direct Investment</div>
              <p className="text-xs text-gray-500 mt-1">vs. $2M–$7M for vendor platforms</p>
            </div>
          </div>

          {/* Strategic Value */}
          <h3 className="text-xl font-bold text-navy mb-4">Strategic Value Delivered</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-10">
            <div className="bg-white border border-gray-200 border-t-4 border-t-teal rounded-lg shadow-md p-5">
              <h4 className="font-bold text-navy mb-2">Optionality at Every Phase</h4>
              <p className="text-sm text-gray-600">
                Each phase delivers standalone value and ROI. Stop at Phase 1 ($62,400), Phase 2 ($106,000), or Phase 3 ($137,200) with working AI capabilities. No all-or-nothing commitment.
              </p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-navy rounded-lg shadow-md p-5">
              <h4 className="font-bold text-navy mb-2">Bounded Risk Per Phase</h4>
              <p className="text-sm text-gray-600">
                Maximum exposure at any decision point is the cost of the current phase. Largest single phase requires $62,400.
              </p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-amber rounded-lg shadow-md p-5">
              <h4 className="font-bold text-navy mb-2">Competitive Moat</h4>
              <p className="text-sm text-gray-600">
                Models trained on organizational data create capabilities competitors cannot purchase. Proprietary knowledge becomes proprietary AI.
              </p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-magenta rounded-lg shadow-md p-5">
              <h4 className="font-bold text-navy mb-2">Deployment Flexibility</h4>
              <p className="text-sm text-gray-600">
                Deploys to any environment: local infrastructure, AWS/Azure cloud, or hybrid. No vendor lock-in.
              </p>
            </div>
          </div>

          {/* What This Proves */}
          <h3 className="text-xl font-bold text-navy mb-4">What This Proves</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white border border-gray-200 border-t-4 border-t-teal rounded-lg shadow-md p-5">
              <h4 className="font-bold text-navy mb-2 text-center">Enterprise AI doesn&apos;t require enterprise budgets</h4>
              <p className="text-sm text-gray-600">
                A complete, production-ready system for $163,100 versus $2M-$7M for vendor platforms. Fine-tuned small models put enterprise AI within reach of mid-market organizations previously priced out.
              </p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-navy rounded-lg shadow-md p-5">
              <h4 className="font-bold text-navy mb-2 text-center">Bottom-up discovery builds stronger AI</h4>
              <p className="text-sm text-gray-600">
                Starting with the people where value is created—letting them identify use cases and build out from there—produces AI capabilities shaped by immediate business value that can be leveraged into emergent capabilities for market differentiation and ultimately disruption.
              </p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-amber rounded-lg shadow-md p-5">
              <h4 className="font-bold text-navy mb-2 text-center">Proprietary data becomes advantage</h4>
              <p className="text-sm text-gray-600">
                Training on organizational knowledge creates AI capabilities competitors cannot replicate, preserving and amplifying institutional knowledge rather than commoditizing it.
              </p>
            </div>
          </div>

          <Link
            href="/results"
            className="inline-flex items-center justify-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
          >
            See the full results
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </Container>
      </section>

      {/* ==================== TRANSPARENCY NOTE ==================== */}
      <section className="py-8 bg-gray-100">
        <Container>
          <p className="text-sm text-gray-500 text-center max-w-4xl mx-auto">
            This is a portfolio demonstration project showcasing the complete design and implementation of an enterprise AI system. The technical implementation is actual and deployment-ready. Business context (the $1.3B international organization) provides realistic constraints and requirements. Direct investment figures are based on actual infrastructure costs and industry-standard training program estimates.
          </p>
          <p className="text-sm text-gray-400 text-center mt-4">
            &copy; 2025 Daniel Dimick. Licensed under{" "}
            <a
              href="https://creativecommons.org/licenses/by-nc/4.0/"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-gray-600"
            >
              CC BY-NC 4.0
            </a>{" "}
            for educational use.
          </p>
        </Container>
      </section>
    </>
  );
}
