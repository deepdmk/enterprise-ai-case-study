import type { Metadata } from "next";
import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout";
import { PageNav } from "@/components/layout/PageNav";
import Link from "next/link";
import { TheStakesTabs, TheDilemmaTabs } from "./ChallengeTabs";

export const metadata: Metadata = {
  title: "The Challenge",
  description:
    "Three compounding crises that made traditional AI deployment approaches infeasible for a $1.3B international organization.",
};

export default function ChallengePage() {
  return (
    <>
      <PageHeader
        title="The Challenge"
        subtitle="Three compounding crises that made traditional AI deployment approaches infeasible"
      />
      <PageNav current="/challenge" />

      {/* ==================== THE QUESTION (HOOK) ==================== */}
      <section className="py-12 bg-slate-800">
        <Container>
          <div className="text-center">
            <h2 className="text-5xl font-bold text-white mb-4">The Question</h2>
            <p className="text-2xl md:text-3xl text-gray-300 leading-relaxed italic">
              How can an organization deploy enterprise AI to leverage its institutional knowledge advantage, deliver immediate ROI, and rebuild trust with change-fatigued international teams, without top-down mandates, multi-million dollar investments, or degrading its competitive advantage?
            </p>
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 1: THE STAKES ==================== */}
      <section className="py-16 bg-navy/10 border-t-4 border-teal">
        <Container>
          <h2 className="text-5xl font-bold text-navy mb-4 flex items-center">
            <span className="bg-navy text-white px-3 py-1 rounded mr-3 text-base">
              1
            </span>
            The Stakes
          </h2>

          <p className="text-xl md:text-2xl text-gray-700 leading-relaxed mb-10">
            The organization faced a sudden sector upheaval and dramatic market shift that created
            three compounding crises: competitive survival pressure from market consolidation, a
            financial crisis with projected 50% revenue decline, and deep organizational skepticism
            from a failed transformation and staff reductions. The Board demanded quarterly AI
            progress while the C-Suite required zero-risk investments. Project teams resisted any
            headquarters mandate while customers rejected AI being imposed on them. Traditional AI
            approaches could not satisfy these contradictory demands.
          </p>

          <TheStakesTabs />
        </Container>
      </section>

      {/* ==================== SECTION 2: THE DILEMMA ==================== */}
      <section className="py-16 border-t-4 border-navy" style={{ backgroundColor: 'rgba(26, 188, 156, 0.15)' }}>
        <Container>
          <h2 className="text-5xl font-bold text-navy mb-4 flex items-center">
            <span className="bg-teal text-white px-3 py-1 rounded mr-3 text-base">
              2
            </span>
            The Dilemma
          </h2>

          <p className="text-xl md:text-2xl text-gray-700 leading-relaxed mb-10">
            Sectoral upheaval magnified existing organizational weaknesses into existential threats.
            A decentralized, change-fatigued culture made mandated adoption ineffective. A 50%
            revenue decline with 3-4 year traditional ROI timelines made vendor platforms unaffordable.
            And a key competitive advantage, institutional knowledge, would be commoditized by
            the very platforms designed to help.
          </p>

          <TheDilemmaTabs />
        </Container>
      </section>

      {/* ==================== CTA: NEXT STEPS ==================== */}
      <section className="py-16 bg-navy">
        <Container>
          <h2 className="text-3xl font-bold text-white mb-6">Next: Strategic Analysis &amp; Approach</h2>
          <p className="text-lg text-gray-300 mb-6">
            With these constraints understood, we conducted rigorous strategic analysis to identify the approach that could satisfy all stakeholder requirements simultaneously.
          </p>
          <Link
            href="/strategy"
            className="inline-flex items-center justify-center px-8 py-4 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
          >
            See how we solved it
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
