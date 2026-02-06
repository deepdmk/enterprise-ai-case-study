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
          <h2 className="text-3xl md:text-4xl font-bold text-navy mb-4 flex items-center">
            <span className="bg-navy text-white px-3 py-1 rounded mr-3 text-base">
              1
            </span>
            Strategic Analysis
          </h2>

          {/* Key Finding Callout */}
          <div className="bg-amber/20 border-l-4 border-amber rounded-r-lg p-6 mb-8">
            <h3 className="text-lg font-semibold mb-2 text-amber-dark">Key Finding</h3>
            <p className="text-lg text-gray-700">
              19 CTQs across stakeholder, competitive, and organizational dimensions that any solution must satisfy simultaneously — constraints that eliminated 2 of 3 strategic alternatives before detailed evaluation.
            </p>
          </div>

          <p className="text-lg text-gray-700 leading-relaxed mb-8">
            We conducted three independent analyses to map the landscape and build a complete
            picture of the context, stakeholders, and organizational dynamics. First, we consulted
            stakeholders to understand their needs. Then, we analyzed the competitive landscape (Five Forces)
            to identify market imperatives. Finally, we assessed the organization (7S + SWOT) to expose
            cultural, capability, and structural realities.
          </p>

          {/* Analysis Preview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white border border-gray-200 border-t-4 border-t-navy rounded-lg p-5">
              <div className="text-2xl font-bold text-navy mb-1">8</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Stakeholder CTQs</div>
              <p className="text-base text-gray-600">Board, C-Suite, Culture & People, Customer requirements</p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-teal rounded-lg p-5">
              <div className="text-2xl font-bold text-teal mb-1">7</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Organizational CTQs</div>
              <p className="text-base text-gray-600">Budget, culture, adoption, language, and structural constraints</p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-magenta rounded-lg p-5">
              <div className="text-2xl font-bold text-magenta mb-1">4</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Competitive CTQs</div>
              <p className="text-base text-gray-600">Proprietary capabilities, efficiency, defensibility, staffing</p>
            </div>
          </div>

          <StrategicAnalysisTabs />
        </Container>
      </section>

      {/* ==================== SECTION 2: STRATEGY DEVELOPMENT ==================== */}
      <section className="py-16 bg-white border-t-4 border-navy">
        <Container>
          <h2 className="text-3xl md:text-4xl font-bold text-navy mb-4 flex items-center">
            <span className="bg-teal-dark text-white px-3 py-1 rounded mr-3 text-base">
              2
            </span>
            Strategy Development
          </h2>

          {/* Key Finding Callout */}
          <div className="bg-teal/10 border-l-4 border-teal rounded-r-lg p-6 mb-8">
            <h3 className="text-lg font-semibold mb-2 text-teal-dark">Key Finding</h3>
            <p className="text-lg text-gray-700">
              Phased Internal Build scored +38 on Pugh Matrix analysis while alternatives failed with -29 and -23. Only one approach could satisfy stakeholder, competitive, and organizational requirements simultaneously.
            </p>
          </div>

          <p className="text-lg text-gray-700 leading-relaxed mb-8">
            We evaluated strategic alternatives against all 19 CTQs using Pugh Matrix analysis. The result:
            Phased Internal Build, an approach that builds proprietary AI internally with existing staff
            through progressive deployment and self-initiated adoption.
          </p>

          {/* Options Preview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-red-50 border border-red-200 border-t-4 border-t-red-400 rounded-lg p-5">
              <div className="text-2xl font-bold text-red-600 mb-1">-29</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Vendor Platform</div>
              <p className="text-base text-gray-600">Commoditizes advantage, exceeds budget 20-50x</p>
            </div>
            <div className="bg-red-50 border border-red-200 border-t-4 border-t-red-400 rounded-lg p-5">
              <div className="text-2xl font-bold text-red-600 mb-1">-23</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Custom Big Bang</div>
              <p className="text-base text-gray-600">Requires $1.5-3.75M, inaccessible AI talent</p>
            </div>
            <div className="bg-teal/10 border-2 border-teal rounded-lg p-5">
              <div className="text-2xl font-bold text-teal mb-1">+38</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Phased Internal Build</div>
              <p className="text-base text-gray-600">Satisfies all 19 CTQs with bounded risk</p>
            </div>
          </div>

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
            className="inline-flex items-center justify-center px-8 py-4 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors"
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
