import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { PageHeader } from "@/components/layout";
import { PageNav } from "@/components/layout/PageNav";
import { Container } from "@/components/layout/Container";
import {
  StrategicAnalysisTabs,
  StrategyDevelopmentTabs,
} from "./StrategyTabs";
import { getAssetPath } from "@/lib/assets";

export const metadata: Metadata = {
  title: "Strategy",
  description:
    "Strategic approach to enterprise AI transformation through three phases: Strategic Analysis, Strategy Development, and Transformation Framework",
};

export default function StrategyPage() {
  return (
    <>
      <PageHeader title="Strategic Analysis & Approach" subtitle="Strategic analysis and strategy development that produced the Phased Internal Build approach" />
      <PageNav current="/strategy" />

      {/* Strategy Flow Diagram */}
      <section className="py-12 bg-slate-100 border-t-4 border-teal">
        <Container>
          <div className="flex justify-center">
            <Image
              src={getAssetPath("/strategy-flow.png")}
              alt="Strategy Flow: Strategic Analysis (Stakeholder Consultations, 7S + SWOT Analysis, 5 Forces) feeds into CTQs (Stakeholder, Organizational, Competitive), which flow through Solution Options Development and Option Scoring to Solution Strategy Selected, leading to Transformation Framework (3 Horizons, Roadmap, Balanced Scorecard)"
              width={1200}
              height={392}
              className="w-full max-w-[1200px] h-auto"
              priority
            />
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 1: STRATEGIC ANALYSIS ==================== */}
      <section className="py-16 bg-navy/10 border-t-4 border-teal">
        <Container>
          <h2 className="text-5xl font-bold text-navy mb-4 flex items-center">
            <span className="bg-navy text-white px-3 py-1 rounded mr-3 text-base">
              1
            </span>
            Strategic Analysis
          </h2>

          <p className="text-xl md:text-2xl text-gray-700 leading-relaxed mb-10">
            We conducted three independent analyses to map the landscape and build a complete
            picture of the context, stakeholders, and organizational dynamics. First, we consulted
            stakeholders to understand their needs. Then, we analyzed the competitive landscape (Five Forces)
            to identify market imperatives. Finally, we assessed the organization (7S + SWOT) to expose
            cultural, capability, and structural realities. Brought together, these produced 19 Critical
            to Quality requirements that established the starting point for viable strategies and
            transformation pathways.
          </p>

          <StrategicAnalysisTabs />
        </Container>
      </section>

      {/* ==================== SECTION 2: STRATEGY DEVELOPMENT ==================== */}
      <section className="py-16 border-t-4 border-navy" style={{ backgroundColor: 'rgba(221, 214, 254, 0.6)' }}>
        <Container>
          <h2 className="text-5xl font-bold text-navy mb-4 flex items-center">
            <span className="bg-teal text-white px-3 py-1 rounded mr-3 text-base">
              2
            </span>
            Strategy Development
          </h2>

          <p className="text-xl md:text-2xl text-gray-700 leading-relaxed mb-10">
            We evaluated strategic alternatives against all 19 CTQs using Pugh Matrix analysis. The result:
            Phased Internal Build, an approach that builds proprietary AI internally with existing staff
            through progressive deployment and self-initiated adoption. This approach satisfies stakeholder,
            competitive, and organizational requirements simultaneously, providing the foundation for
            transformation planning.
          </p>

          <StrategyDevelopmentTabs />
        </Container>
      </section>

      {/* ==================== NEXT: TRANSFORMATION FRAMEWORK (CTA) ==================== */}
      <section className="py-16 bg-navy">
        <Container>
          <h2 className="text-3xl font-bold text-white mb-6">
            Next: Transformation Framework
          </h2>
          <p className="text-lg text-gray-300 mb-6">
            With strategy selected, the Transformation Framework translates
            these strategic decisions into concrete implementation through Three
            Horizons phasing, a detailed roadmap with embedded change
            management, and Balanced Scorecard measurement.
          </p>
          <Link
            href="/transformation"
            className="inline-flex items-center justify-center px-8 py-4 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
          >
            View Transformation Framework
            <svg
              className="w-5 h-5 ml-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </Link>
        </Container>
      </section>

    </>
  );
}
