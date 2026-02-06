import { Container } from '@/components/layout/Container'
import { Card } from '@/components/ui/Card'
import Link from 'next/link'

export const metadata = {
  title: 'Case Study Overview',
  description: 'A phased transformation delivering value at every milestone without $2M gambles or vendor lock-in. How a mid-market organization built strategic AI capabilities through incremental deployment and bounded risk.',
}

export default function SummaryPage() {
  return (
    <div className="relative">
      {/* 1. Hero Title */}
      <div className="bg-navy text-white py-16">
        <Container>
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Building Unique AI Capabilities Through the Company&apos;s Data and People
          </h1>
          <p className="text-xl text-white/80">
            A phased transformation delivering value at every milestone without $2M gambles or vendor lock-in
          </p>
        </Container>
      </div>

      {/* Hero Metrics */}
      <section className="bg-gradient-to-br from-slate-900 to-slate-800 py-16">
        <Container>
          {/* 4 Metric Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {/* Card 1: Direct Investment */}
            <Card className="p-8 text-center bg-white/95 border-white shadow-lg hover:shadow-xl transition-colors">
              <div className="mb-4">
                <svg className="w-12 h-12 mx-auto text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="text-5xl font-bold text-gray-900 mb-2">$163.1K</div>
              <div className="text-base font-semibold text-gray-700 mb-2">Direct Investment</div>
              <div className="text-base text-gray-500">$11,100 infrastructure + $152K training programs across 6 phases</div>
            </Card>

            {/* Card 2: Infrastructure Cost */}
            <Card className="p-8 text-center bg-white/95 border-white shadow-lg hover:shadow-xl transition-colors">
              <div className="mb-4">
                <svg className="w-12 h-12 mx-auto text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div className="text-5xl font-bold text-gray-900 mb-2">$11,100</div>
              <div className="text-base font-semibold text-gray-700 mb-2">Infrastructure Cost</div>
              <div className="text-base text-gray-500">Compute, storage, and tooling vs. $2M-$7M for vendor platforms</div>
            </Card>

            {/* Card 3: Phases */}
            <Card className="p-8 text-center bg-white/95 border-white shadow-lg hover:shadow-xl transition-colors">
              <div className="mb-4">
                <svg className="w-12 h-12 mx-auto text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="text-5xl font-bold text-gray-900 mb-2">6 phases</div>
              <div className="text-base font-semibold text-gray-700 mb-2">With Exit Optionality</div>
              <div className="text-base text-gray-500">Stop at any phase, retain value. No all-or-nothing bets.</div>
            </Card>

            {/* Card 4: Timeline */}
            <Card className="p-8 text-center bg-white/95 border-white shadow-lg hover:shadow-xl transition-colors">
              <div className="mb-4">
                <svg className="w-12 h-12 mx-auto text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="text-5xl font-bold text-gray-900 mb-2">18 months</div>
              <div className="text-base font-semibold text-gray-700 mb-2">Full System Timeline</div>
              <div className="text-base text-gray-500">Value from Phase 1 onward vs. 3-4 year vendor ROI timelines</div>
            </Card>
          </div>

          {/* Hero CTAs - Four Page Navigation Links */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center flex-wrap">
            <Link
              href="/challenge"
              className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-slate-100 text-slate-900 font-semibold rounded-lg transition-colors"
            >
              Explore the Challenge
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
            <Link
              href="/strategy"
              className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-slate-100 text-slate-900 font-semibold rounded-lg transition-colors"
            >
              Explore the Strategy
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
            <Link
              href="/solution"
              className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-slate-100 text-slate-900 font-semibold rounded-lg transition-colors"
            >
              Explore the Solution
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
            <Link
              href="/results"
              className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-slate-100 text-slate-900 font-semibold rounded-lg transition-colors"
            >
              Explore the Results
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </Container>
      </section>

      {/* 2. Challenge Section */}
      <div className="bg-red-900 py-12 relative">
        <div className="absolute inset-y-0 left-0 w-1/6 bg-gradient-to-r from-black/40 to-transparent pointer-events-none"></div>
        <div className="absolute inset-y-0 right-0 w-1/6 bg-gradient-to-l from-black/40 to-transparent pointer-events-none"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <section id="challenge">
            <h1 className="text-4xl md:text-5xl font-bold mb-8 text-white text-center">The Challenge</h1>

            {/* The Stakes */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-3 text-white">The Stakes</h2>
              <p className="text-lg text-white">
                The organization faced a sudden sector upheaval and dramatic market shift that created three compounding crises: competitive survival pressure from market consolidation, a financial crisis with projected 50% revenue decline, and deep organizational skepticism from a failed transformation and staff reductions. The Board demanded quarterly AI progress while the C-Suite required zero-risk investments. Project teams resisted any headquarters mandate while customers rejected AI being imposed on them. Traditional AI approaches could not satisfy these contradictory demands.
              </p>
            </div>

            {/* The Dilemma */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-3 text-white">The Dilemma</h2>
              <div className="space-y-3 text-lg text-white">
                <p><strong>Competitive Survival.</strong> Market consolidation forced competitors into each other&apos;s spaces. The organization&apos;s only defensible advantage, institutional knowledge across 115 countries, was trapped in silos while new entrants leveraged AI to compete without institutional baggage.</p>
                <p><strong>Financial and Timing Mismatch.</strong> Board demanded quarterly AI results while traditional platforms require 3-4 year ROI timelines. C-suite couldn&apos;t approve $2M+ bets upfront. By the time a vendor platform delivered ROI, the market might have consolidated.</p>
                <p><strong>Organizational Skepticism and Change Fatigue.</strong> A failed top-down transformation had damaged trust. Change-fatigued staff, overwhelmed post-layoffs, had zero appetite for &ldquo;another corporate initiative.&rdquo; 70% international workforce meant HQ mandates were culturally non-viable.</p>
              </div>
            </div>

            {/* The Question */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold mb-3 text-white">The Question</h2>
              <p className="text-xl text-white italic">
                How could an organization deploy enterprise AI to leverage its institutional knowledge advantage, deliver immediate ROI, and rebuild trust with change-fatigued international teams, without top-down mandates, multi-million dollar investments, or degrading its competitive advantage?
              </p>
            </div>

            {/* Section CTA */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/challenge"
                className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-red-50 text-gray-900 font-semibold rounded-lg shadow-lg transition-colors"
              >
                See the full challenge analysis
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          </section>
        </div>
      </div>

      {/* 3. The Approach Section */}
      <div className="bg-purple-900 py-12 relative">
        <div className="absolute inset-y-0 left-0 w-1/6 bg-gradient-to-r from-black/40 to-transparent pointer-events-none"></div>
        <div className="absolute inset-y-0 right-0 w-1/6 bg-gradient-to-l from-black/40 to-transparent pointer-events-none"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <section>
            <h1 className="text-4xl md:text-5xl font-bold mb-8 text-white text-center">The Approach</h1>

            {/* Strategic Analysis */}
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-2 text-white">Strategic Analysis</h2>
              <p className="text-lg text-white">
                We conducted three independent analyses to define the situation: stakeholder consultations to reveal needs, organizational assessment (7S + SWOT) to expose cultural and capability realities, and competitive analysis (Five Forces) to identify market imperatives. Together, these produced 19 Critical to Quality requirements that any solution must satisfy.
              </p>
            </div>

            {/* Strategy Selection */}
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-2 text-white">Strategy Selection</h2>
              <p className="text-lg text-white">
                We evaluated strategic alternatives against all 19 CTQs using Pugh Matrix analysis and selected Phased Internal Build: proprietary AI built internally with existing staff through progressive deployment and self-initiated adoption. This approach satisfies stakeholder, competitive, and organizational requirements simultaneously.
              </p>
            </div>

            {/* Transformation Planning */}
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-2 text-white">Transformation Planning</h2>
              <p className="text-lg text-white">
                The strategic approach alone couldn&apos;t satisfy all 19 CTQs. Many depended on how the transformation was timed and implemented. We applied Three Horizons for staging with decision points, Roadmap for integrating technical and change management, and Balanced Scorecard for data-driven decisions at each phase boundary. The result: an 18-month, six-phase implementation plan that builds progressively from bottom-up value, delivers ROI at every phase, and preserves optionality throughout so the organization can stop at any point and retain the value already created.
              </p>
            </div>

            {/* Section CTAs */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/strategy"
                className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-purple-50 text-gray-900 font-semibold rounded-lg shadow-lg transition-colors"
              >
                See the full strategic analysis
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
              <Link
                href="/transformation"
                className="inline-flex items-center justify-center px-6 py-3 bg-purple-800 hover:bg-purple-700 text-white font-semibold rounded-lg border-2 border-purple-700 transition-colors"
              >
                See the transformation framework
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          </section>
        </div>
      </div>

      {/* 4. Solution Section */}
      <div className="bg-blue-900 py-12 relative">
        <div className="absolute inset-y-0 left-0 w-1/6 bg-gradient-to-r from-black/40 to-transparent pointer-events-none"></div>
        <div className="absolute inset-y-0 right-0 w-1/6 bg-gradient-to-l from-black/40 to-transparent pointer-events-none"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <section id="solution">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 text-white text-center">
            The Solution
          </h1>

          <h3 className="text-2xl font-bold mb-2 text-white">
            Building from the Core: Phased Transformation with Incremental Trust
          </h3>
          <p className="text-lg text-blue-100 mb-6">
            Six phases of progressive capability building with value delivered at each stage and optionality maintained throughout.
          </p>

          {/* Core Strategy */}
          <Card className="p-6 bg-white border-white shadow-lg mb-6">
            <div className="prose prose-lg max-w-none">
              <p className="mb-3">
                We inverted the traditional enterprise AI playbook. Rather than mandating a platform from headquarters and asking staff to trust that value would come in 3-4 years, we started where the burden was worst: overwhelmed teams struggling to find institutional knowledge trapped in silos across four languages. We built immediate relief for those teams first, then let demonstrated value drive organic adoption across the organization. Each phase built on proven success, not projected ROI. This meant the organization could stop at any point, keep everything already built, and face no sunk cost.
              </p>
              <p>
                The technical architecture reinforced this approach. While infrastructure investment was required, the system did not require large proprietary platforms or cloud infrastructure to start, though both remained options for scaling. Each phase brought increasing sophistication and strategic capabilities, from basic search to intelligent agents to autonomous collaboration. The deployment remains non-proprietary throughout, built to integrate easily with proprietary systems when scaling demands it.
              </p>
            </div>
          </Card>

          {/* Six-Phase Implementation */}
          <h3 className="text-xl font-bold mb-4 text-white">Six-Phase Implementation</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {/* Phase 0: Infrastructure Foundation */}
            <Card className="p-4 bg-white border-white shadow-lg hover:border-blue-300 transition-colors">
              <div className="text-xs font-semibold text-gray-500 mb-1">PHASE 0</div>
              <h4 className="text-lg font-bold mb-1 text-gray-900">Infrastructure Foundation</h4>
              <p className="text-base text-gray-600 italic mb-2">Data pipeline and staging infrastructure</p>
              <p className="text-base text-gray-700">
                Foundational registries that track models, datasets, and experiments enabling systematic learning across all phases. Zero infrastructure cost with file-based storage.
              </p>
            </Card>

            {/* Phase 1: Unified Embedding Space */}
            <Card className="p-4 bg-white border-white shadow-lg hover:border-blue-300 transition-colors">
              <div className="text-xs font-semibold text-gray-500 mb-1">PHASE 1</div>
              <h4 className="text-lg font-bold mb-1 text-gray-900">Unified Embedding Space</h4>
              <p className="text-base text-gray-600 italic mb-2">Shared semantic infrastructure across all divisions</p>
              <p className="text-base text-gray-700">
                Search all organizational data with AI embeddings so employees find relevant documents across any division, country, or language (English, French, Spanish, Arabic) more easily.
              </p>
            </Card>

            {/* Phase 2: Task-Specific SLMs */}
            <Card className="p-4 bg-white border-white shadow-lg hover:border-blue-300 transition-colors">
              <div className="text-xs font-semibold text-gray-500 mb-1">PHASE 2</div>
              <h4 className="text-lg font-bold mb-1 text-gray-900">Task-Specific SLMs</h4>
              <p className="text-base text-gray-600 italic mb-2">Fine-tuned small language models for division tasks</p>
              <p className="text-base text-gray-700">
                AI learns the organization&apos;s team-specific tasks giving employees intelligent assistance for the work they prioritize. 15 specialized models trained on the organization&apos;s workflows.
              </p>
            </Card>

            {/* Phase 3: MoE Division Agents */}
            <Card className="p-4 bg-white border-white shadow-lg hover:border-blue-300 transition-colors">
              <div className="text-xs font-semibold text-gray-500 mb-1">PHASE 3</div>
              <h4 className="text-lg font-bold mb-1 text-gray-900">MoE Division Agents</h4>
              <p className="text-base text-gray-600 italic mb-2">Mixture-of-Experts models from merged SLMs</p>
              <p className="text-base text-gray-700">
                Each division gets expert AI combining their specialized assistants into one agent that handles many tasks to the organization&apos;s standards.
              </p>
            </Card>

            {/* Phase 4: Agentic Discovery */}
            <Card className="p-4 bg-white border-white shadow-lg hover:border-blue-300 transition-colors">
              <div className="text-xs font-semibold text-gray-500 mb-1">PHASE 4</div>
              <h4 className="text-lg font-bold mb-1 text-gray-900">Agentic Discovery</h4>
              <p className="text-base text-gray-600 italic mb-2">A2A protocol for autonomous collaboration</p>
              <p className="text-base text-gray-700">
                Agents learn how to use information across the organization&apos;s divisions giving access to task capabilities to enhance other divisions&apos; work.
              </p>
            </Card>

            {/* Phase 5: Orchestrated System */}
            <Card className="p-4 bg-white border-white shadow-lg hover:border-blue-300 transition-colors">
              <div className="text-xs font-semibold text-gray-500 mb-1">PHASE 5</div>
              <h4 className="text-lg font-bold mb-1 text-gray-900">Orchestrated System</h4>
              <p className="text-base text-gray-600 italic mb-2">SLM orchestrator trained from discovery data</p>
              <p className="text-base text-gray-700">
                Employees across the organization engage through a single AI window that can leverage data and capabilities across all the enterprise tailored to the organization&apos;s knowledge and culture.
              </p>
            </Card>
          </div>

          {/* Section CTA */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              href="/solution"
              className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-blue-50 text-gray-900 font-semibold rounded-lg shadow-lg transition-colors"
            >
              See the detailed implementation
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
          </section>
        </div>
      </div>

      {/* 5. Results Section */}
      <div className="bg-green-900 py-12 relative">
        <div className="absolute inset-y-0 left-0 w-1/6 bg-gradient-to-r from-black/40 to-transparent pointer-events-none"></div>
        <div className="absolute inset-y-0 right-0 w-1/6 bg-gradient-to-l from-black/40 to-transparent pointer-events-none"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <section id="results">
            <h1 className="text-4xl md:text-5xl font-bold mb-6 text-white text-center">
              The Results
            </h1>

            {/* Investment Analysis */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold mb-3 text-white">Investment Analysis</h3>
              <p className="text-lg text-white mb-4">
                The complete system can be built for $163,100 in direct investment: $11,100 infrastructure (GPU compute, storage, vector database, inference, monitoring) plus $152,000 training programs (user training, change management, multi-language materials for 8,000 staff). This compares to $2M&ndash;$7M for typical enterprise AI platform deployments.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="p-4 bg-white border-white shadow-lg text-center">
                  <div className="text-2xl font-bold text-gray-900 mb-1">$11,100</div>
                  <div className="text-sm font-semibold text-gray-700">Infrastructure</div>
                </Card>
                <Card className="p-4 bg-white border-white shadow-lg text-center">
                  <div className="text-2xl font-bold text-gray-900 mb-1">$152,000</div>
                  <div className="text-sm font-semibold text-gray-700">Training Programs</div>
                </Card>
                <div className="p-4 bg-white rounded-lg shadow-lg text-center border-2" style={{ borderColor: '#1ABC9C' }}>
                  <div className="text-2xl font-bold mb-1" style={{ color: '#1ABC9C' }}>$163,100</div>
                  <div className="text-sm font-semibold text-gray-700">Total Direct Investment</div>
                </div>
              </div>
            </div>

            {/* Strategic Value Delivered */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold mb-3 text-white">Strategic Value Delivered</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="p-4 bg-white border-white shadow-lg">
                  <h4 className="text-lg font-bold mb-2 text-gray-900">Optionality at Every Phase</h4>
                  <p className="text-base text-gray-700">Each phase delivers standalone value. Stop at Phase 1 ($62,400), Phase 2 ($106,000), or Phase 3 ($137,200) with working AI capabilities. No all-or-nothing commitment.</p>
                </Card>
                <Card className="p-4 bg-white border-white shadow-lg">
                  <h4 className="text-lg font-bold mb-2 text-gray-900">Bounded Risk Per Phase</h4>
                  <p className="text-base text-gray-700">Maximum exposure at any decision point is the cost of the current phase. Largest single phase requires $62,400. Compare to $2M+ vendor commitments before seeing results.</p>
                </Card>
                <Card className="p-4 bg-white border-white shadow-lg">
                  <h4 className="text-lg font-bold mb-2 text-gray-900">Competitive Moat Through Proprietary Models</h4>
                  <p className="text-base text-gray-700">Models trained on organizational data create capabilities competitors cannot purchase. Transforms proprietary knowledge into proprietary AI, not commoditized &ldquo;best practices.&rdquo;</p>
                </Card>
                <Card className="p-4 bg-white border-white shadow-lg">
                  <h4 className="text-lg font-bold mb-2 text-gray-900">Deployment Flexibility</h4>
                  <p className="text-base text-gray-700">Architecture deploys to any environment: local infrastructure for data sovereignty, AWS/Azure cloud for scalability, or hybrid. No vendor lock-in, no forced migration paths.</p>
                </Card>
              </div>
            </div>

            {/* What This Proves */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold mb-3 text-white">What This Proves</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="p-4 bg-white border-white shadow-lg">
                  <h4 className="text-lg font-bold mb-2 text-gray-900 text-center">Enterprise AI doesn&apos;t require enterprise budgets</h4>
                  <p className="text-base text-gray-700">A complete, production-ready system can be built for $163,100. The economics of fine-tuned small models make internal build viable for mid-market organizations.</p>
                </Card>
                <Card className="p-4 bg-white border-white shadow-lg">
                  <h4 className="text-lg font-bold mb-2 text-gray-900 text-center">Phased approaches reduce risk without sacrificing capability</h4>
                  <p className="text-base text-gray-700">Progressive investment with decision points eliminates all-or-nothing risk. Organizations gain optionality without giving up the end-state vision.</p>
                </Card>
                <Card className="p-4 bg-white border-white shadow-lg">
                  <h4 className="text-lg font-bold mb-2 text-gray-900 text-center">Proprietary data becomes proprietary advantage</h4>
                  <p className="text-base text-gray-700">Training on organizational knowledge creates AI capabilities competitors cannot replicate. Internally-built systems preserve and amplify institutional knowledge.</p>
                </Card>
              </div>
            </div>

            {/* Methodology footnote */}
            <p className="text-lg text-green-100 border-t border-green-700 pt-4 mb-6">
              <strong>Note:</strong> This is a portfolio demonstration project. The technical implementation is actual and deployment-ready. Business context provides realistic constraints. Direct investment figures are based on actual infrastructure costs and industry-standard training program estimates.
            </p>

            {/* Section CTA */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/results"
                className="inline-flex items-center justify-center px-6 py-3 bg-white hover:bg-green-50 text-gray-900 font-semibold rounded-lg shadow-lg transition-colors"
              >
                See the full results
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
