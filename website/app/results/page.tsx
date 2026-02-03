import type { Metadata } from "next";
import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout";
import { PageNav } from "@/components/layout/PageNav";
import Link from "next/link";
import { InvestmentTabs, TechnicalTabs } from "./ResultsTabs";

export const metadata: Metadata = {
  title: "Results",
  description:
    "A complete enterprise AI system built for $163.1K direct investment — from unified knowledge access through orchestrated multi-agent intelligence.",
};

export default function ResultsPage() {
  return (
    <>
      <PageHeader
        title="Results"
        subtitle="A complete enterprise AI system built for $163.1K direct investment — from unified knowledge access through orchestrated multi-agent intelligence"
      />
      <PageNav current="/results" />

      {/* ==================== SECTION 1: CAPABILITIES DELIVERED ==================== */}
      <section className="py-16 bg-navy/10 border-t-4 border-teal">
        <Container>
          <h2 className="text-3xl font-bold text-navy mb-4">Capabilities Delivered</h2>
          <p className="text-lg text-gray-700 mb-10 max-w-4xl">
            This case study produced a complete, deployment-ready enterprise AI system progressing from foundational knowledge access through orchestrated multi-agent intelligence. Each phase delivers standalone value — organizations can stop at any point with working AI capabilities.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white border-t-4 border-t-navy rounded-lg shadow-md p-6">
              <span className="text-base font-semibold text-navy/60 uppercase tracking-wide">Phase 0</span>
              <h3 className="text-xl font-bold text-navy mt-1 mb-2">MLOps Infrastructure</h3>
              <p className="text-gray-600 text-base mb-4">Data registry, model registry, experiment tracking — the foundation for systematic AI development</p>
              <div className="text-base font-semibold text-gray-500">$0</div>
            </div>

            <div className="bg-white border-t-4 border-t-teal rounded-lg shadow-md p-6">
              <span className="text-base font-semibold text-teal/60 uppercase tracking-wide">Phase 1</span>
              <h3 className="text-xl font-bold text-navy mt-1 mb-2">Unified Embedding Space</h3>
              <p className="text-gray-600 text-base mb-4">Semantic search across all organizational knowledge, breaking down information silos across divisions</p>
              <div className="text-base font-semibold text-teal">$62,400</div>
            </div>

            <div className="bg-white border-t-4 border-t-amber rounded-lg shadow-md p-6">
              <span className="text-base font-semibold text-amber/60 uppercase tracking-wide">Phase 2</span>
              <h3 className="text-xl font-bold text-navy mt-1 mb-2">14 Task-Specific SLMs</h3>
              <p className="text-gray-600 text-base mb-4">Fine-tuned models for specific workflows — portfolio analysis, RFP response, risk assessment, and more</p>
              <div className="text-base font-semibold text-amber">$43,600</div>
            </div>

            <div className="bg-white border-t-4 border-t-magenta rounded-lg shadow-md p-6">
              <span className="text-base font-semibold text-magenta/60 uppercase tracking-wide">Phase 3</span>
              <h3 className="text-xl font-bold text-navy mt-1 mb-2">3 MoE Division Agents</h3>
              <p className="text-gray-600 text-base mb-4">Mixture-of-Experts agents combining task capabilities into division-level intelligence with multi-step reasoning</p>
              <div className="text-base font-semibold text-magenta">$31,200</div>
            </div>

            <div className="bg-white border-t-4 border-t-teal rounded-lg shadow-md p-6">
              <span className="text-base font-semibold text-teal/60 uppercase tracking-wide">Phase 4</span>
              <h3 className="text-xl font-bold text-navy mt-1 mb-2">Agent-to-Agent Protocol</h3>
              <p className="text-gray-600 text-base mb-4">Experimental framework for agents to collaborate across divisions, generating training data for orchestration</p>
              <div className="text-base font-semibold text-teal">$15,500</div>
            </div>

            <div className="bg-white border-t-4 border-t-navy rounded-lg shadow-md p-6">
              <span className="text-base font-semibold text-navy/60 uppercase tracking-wide">Phase 5</span>
              <h3 className="text-xl font-bold text-navy mt-1 mb-2">Learned Orchestrator</h3>
              <p className="text-gray-600 text-base mb-4">Single entry point routing queries to the right experts — enterprise-wide AI through one interface</p>
              <div className="text-base font-semibold text-navy">$10,400</div>
            </div>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 2: STRATEGIC VALUE DELIVERED ==================== */}
      <section className="py-16 border-t-4 border-navy" style={{ backgroundColor: "rgba(253, 230, 138, 0.25)" }}>
        <Container>
          <h2 className="text-3xl font-bold text-navy mb-4">Strategic Value Delivered</h2>
          <p className="text-lg text-gray-700 mb-10 max-w-4xl">
            Beyond the technical capabilities, this approach delivers strategic advantages that traditional enterprise AI deployments cannot match.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border-t-4 border-t-teal rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-navy mb-3">Optionality at Every Phase</h3>
              <p className="text-gray-600 mb-4">
                Each phase delivers standalone value. Organizations can stop at Phase 1 (knowledge access), Phase 2 (task automation), or Phase 3 (division intelligence) with working AI capabilities. No all-or-nothing commitment required.
              </p>
              <ul className="text-base text-gray-500 space-y-1">
                <li>&bull; After Phase 1 ($62,400): Universal search working</li>
                <li>&bull; After Phase 2 ($106,000): Task automation working</li>
                <li>&bull; After Phase 3 ($137,200): Division agents working</li>
              </ul>
            </div>

            <div className="bg-white border-t-4 border-t-navy rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-navy mb-3">Bounded Risk Per Phase</h3>
              <p className="text-gray-600">
                Maximum exposure at any decision point is the cost of the current phase. The largest single phase (Phase 1) requires $62,400. Compare to vendor approaches requiring $2M+ commitment before seeing results.
              </p>
            </div>

            <div className="bg-white border-t-4 border-t-amber rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-navy mb-3">Competitive Moat Through Proprietary Models</h3>
              <p className="text-gray-600">
                Models trained on organizational data create capabilities competitors cannot purchase. Unlike vendor platforms that commoditize institutional knowledge, this approach transforms proprietary knowledge into proprietary AI capabilities.
              </p>
            </div>

            <div className="bg-white border-t-4 border-t-magenta rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-navy mb-3">Deployment Flexibility</h3>
              <p className="text-gray-600">
                The architecture deploys to any environment: local infrastructure for data sovereignty, AWS/Azure cloud for scalability, or hybrid configurations. No vendor lock-in, no forced migration paths.
              </p>
            </div>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 3: INVESTMENT ANALYSIS ==================== */}
      <section className="py-16 bg-slate-200 border-t-4 border-teal">
        <Container>
          <h2 className="text-3xl font-bold text-navy mb-4">Investment Analysis</h2>
          <p className="text-lg text-gray-700 mb-10 max-w-4xl">
            The complete system was built for $163.1K in direct investment — infrastructure and training programs required regardless of technical approach. This compares to $2M&ndash;$7M for typical enterprise AI platform deployments.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white border-t-4 border-t-navy rounded-lg shadow-md p-6 text-center">
              <div className="text-3xl font-bold text-navy mb-1">$11,100</div>
              <div className="text-base font-semibold text-gray-700 mb-2">Infrastructure</div>
              <p className="text-base text-gray-500">GPU compute, storage, vector database, inference infrastructure, monitoring</p>
            </div>
            <div className="bg-white border-t-4 border-t-navy rounded-lg shadow-md p-6 text-center">
              <div className="text-3xl font-bold text-navy mb-1">$152,000</div>
              <div className="text-base font-semibold text-gray-700 mb-2">Training Programs</div>
              <p className="text-base text-gray-500">User training, change management, multi-language materials for 8,000 staff</p>
            </div>
            <div className="bg-teal/10 border-2 border-teal rounded-lg shadow-md p-6 text-center">
              <div className="text-3xl font-bold text-teal mb-1">$163,100</div>
              <div className="text-base font-semibold text-gray-700 mb-2">Total Direct Investment</div>
              <p className="text-base text-gray-500">Complete 6-phase deployment</p>
            </div>
          </div>

          <InvestmentTabs />

          <p className="text-base text-gray-500 italic mt-4">
            Labor costs (technical staff time) are excluded from this comparison as they vary significantly by organization and are required for any AI deployment approach.
          </p>
        </Container>
      </section>

      {/* ==================== SECTION 4: TECHNICAL IMPLEMENTATION ==================== */}
      <section className="py-16 border-t-4 border-navy" style={{ backgroundColor: "rgba(221, 214, 254, 0.6)" }}>
        <Container>
          <h2 className="text-3xl font-bold text-navy mb-4">Technical Implementation</h2>
          <p className="text-lg text-gray-700 mb-10 max-w-4xl">
            The case study demonstrates practical implementation across the full AI engineering stack — from fine-tuning techniques through production architecture.
          </p>

          <div className="mb-8">
            <TechnicalTabs />
          </div>

          <h3 className="text-xl font-semibold text-navy mb-4">Architecture Characteristics</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white border-t-4 border-t-teal rounded-lg shadow-md p-4">
              <div className="font-semibold text-navy mb-1">Model-agnostic</div>
              <p className="text-base text-gray-600">Swappable components, no dependency on specific model families</p>
            </div>
            <div className="bg-white border-t-4 border-t-navy rounded-lg shadow-md p-4">
              <div className="font-semibold text-navy mb-1">Multimodal-ready</div>
              <p className="text-base text-gray-600">Architecture supports expansion to vision and other modalities</p>
            </div>
            <div className="bg-white border-t-4 border-t-amber rounded-lg shadow-md p-4">
              <div className="font-semibold text-navy mb-1">Platform-portable</div>
              <p className="text-base text-gray-600">Validated deployment paths for AWS Bedrock, SageMaker, Azure AI</p>
            </div>
            <div className="bg-white border-t-4 border-t-magenta rounded-lg shadow-md p-4">
              <div className="font-semibold text-navy mb-1">Observable</div>
              <p className="text-base text-gray-600">Structured logging, experiment tracking, evaluation pipelines throughout</p>
            </div>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 5: WHAT THIS PROVES ==================== */}
      <section className="py-16 bg-teal/10 border-t-4 border-teal">
        <Container>
          <h2 className="text-3xl font-bold text-navy mb-8">What This Case Study Proves</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white border-t-4 border-t-teal rounded-lg shadow-md p-6">
              <h3 className="text-lg font-bold text-navy mb-3">Enterprise AI doesn&apos;t require enterprise budgets</h3>
              <p className="text-gray-600 text-base">
                A complete, production-ready system — from embeddings through orchestrated multi-agent intelligence — can be built for $163.1K in direct investment. The economics of fine-tuned small models and modern tooling make internal build viable for mid-market organizations.
              </p>
            </div>
            <div className="bg-white border-t-4 border-t-navy rounded-lg shadow-md p-6">
              <h3 className="text-lg font-bold text-navy mb-3">Phased approaches reduce risk without sacrificing capability</h3>
              <p className="text-gray-600 text-base">
                Progressive investment with decision points at each phase eliminates the all-or-nothing risk of traditional deployments. Organizations gain optionality without giving up the end-state vision of orchestrated enterprise AI.
              </p>
            </div>
            <div className="bg-white border-t-4 border-t-amber rounded-lg shadow-md p-6">
              <h3 className="text-lg font-bold text-navy mb-3">Proprietary data becomes proprietary advantage</h3>
              <p className="text-gray-600 text-base">
                Training on organizational knowledge creates AI capabilities competitors cannot replicate. Unlike vendor platforms, internally-built systems preserve and amplify institutional knowledge rather than commoditizing it.
              </p>
            </div>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 6: CTAs ==================== */}
      <section className="py-16 bg-navy">
        <Container>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/solution"
              className="inline-flex items-center justify-center px-8 py-4 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
            >
              See How It Was Built
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
            <Link
              href="/strategy"
              className="inline-flex items-center justify-center px-8 py-4 bg-transparent hover:bg-white/10 text-white font-semibold rounded-lg border-2 border-white transition-colors"
            >
              Review the Strategic Approach
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 7: TRANSPARENCY NOTE ==================== */}
      <section className="py-8 bg-gray-100">
        <Container>
          <p className="text-base text-gray-500 text-center max-w-4xl mx-auto">
            This is a portfolio demonstration project showcasing the complete design and implementation of an enterprise AI system. The technical implementation is actual and deployment-ready. Business context (the $1.3B international organization) provides realistic constraints and requirements. Direct investment figures are based on actual infrastructure costs and industry-standard training program estimates.
          </p>
          <p className="text-base text-gray-400 text-center mt-4">
            &copy; 2025 Daniel Dimick. Licensed under{' '}
            <a
              href="https://creativecommons.org/licenses/by-nc/4.0/"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-gray-600"
            >
              CC BY-NC 4.0
            </a>{' '}
            for educational use.
          </p>
        </Container>
      </section>
    </>
  );
}
