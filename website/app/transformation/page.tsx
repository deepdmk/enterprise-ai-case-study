import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { PageNav } from "@/components/layout/PageNav";
import { Container } from "@/components/layout/Container";
import { TransformationFrameworkTabs } from "./TransformationTabs";
import { TransformationFlowGraphic } from "@/components/transformation/TransformationFlowGraphic";

export const metadata: Metadata = {
  title: "Transformation Framework",
  description:
    "How we structured the change journey with optionality at each phase — Three Horizons Framework, Transformation Roadmap, and Balanced Scorecard",
};

export default function TransformationPage() {
  return (
    <>
      <PageHeader
        title="Transformation Framework"
        subtitle="How we structured the change journey with optionality at each phase"
      />
      <PageNav current="/transformation" />

      {/* Strategy Flow Diagram */}
      <section className="py-12 bg-slate-100 border-t-4 border-teal">
        <Container>
          <TransformationFlowGraphic />
        </Container>
      </section>

      {/* ==================== TRANSFORMATION FRAMEWORK ==================== */}
      <section className="py-16 bg-navy/10 border-t-4 border-teal">
        <Container>
          {/* Key Finding Callout */}
          <div className="bg-magenta/10 border-l-4 border-magenta rounded-r-lg p-6 mb-8">
            <h3 className="text-lg font-semibold mb-2 text-magenta">Key Finding</h3>
            <p className="text-lg text-gray-700">
              The strategic approach alone couldn&apos;t satisfy all 19 CTQs. Many depended on how the transformation was timed and implemented — requiring three integrated frameworks to translate strategy into executable phases with built-in optionality.
            </p>
          </div>

          <p className="text-lg text-gray-700 leading-relaxed mb-8">
            We applied three frameworks to structure the change journey. Three Horizons provided the strategic staging — defending core operations first, then building emerging advantages, then creating transformative options — with natural decision points at each boundary. The Transformation Roadmap translated these horizons into concrete phase-by-phase execution, integrating technical implementation with change management from design rather than as an afterthought. And Balanced Scorecard enabled data-driven progression decisions through quarterly measurement across four interdependent perspectives.
          </p>

          {/* Framework Preview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white border border-gray-200 border-t-4 border-t-teal rounded-lg p-5">
              <div className="text-2xl font-bold text-teal mb-1">3 Horizons</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Strategic Staging</div>
              <p className="text-base text-gray-600">Defend, build, transform — with decision points at each boundary</p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-amber rounded-lg p-5">
              <div className="text-2xl font-bold text-amber mb-1">6 Phases</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Integrated Roadmap</div>
              <p className="text-base text-gray-600">Technical + change management aligned in each phase</p>
            </div>
            <div className="bg-white border border-gray-200 border-t-4 border-t-navy rounded-lg p-5">
              <div className="text-2xl font-bold text-navy mb-1">4 Perspectives</div>
              <div className="text-sm font-semibold text-gray-700 mb-2">Balanced Scorecard</div>
              <p className="text-base text-gray-600">Quarterly measurement enables data-driven progression</p>
            </div>
          </div>

          <TransformationFrameworkTabs />
        </Container>
      </section>

      {/* ==================== NEXT: SOLUTION (CTA) ==================== */}
      <section className="py-16 bg-navy">
        <Container>
          <h2 className="text-3xl font-bold text-white mb-6">
            Next: The Solution
          </h2>
          <p className="text-lg text-gray-300 mb-6">
            With the transformation framework defined, the Solution details
            the technical architecture that implements each phase, from
            unified embedding space through orchestrated agentic AI,
            delivering the progressive capability build that the strategy
            requires.
          </p>
          <Link
            href="/solution"
            className="inline-flex items-center justify-center px-8 py-4 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
          >
            View The Solution
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

      {/* ==================== TRANSPARENCY NOTE ==================== */}
      <section className="py-2 bg-gray-100">
        <Container>
          <p className="text-base text-gray-500 text-center">
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
