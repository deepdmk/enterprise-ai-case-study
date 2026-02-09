import type { Metadata } from "next";
import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout";
import { PageNav } from "@/components/layout/PageNav";
import Link from "next/link";
import { TheStakesTabs, TheDilemmaTabs } from "./ChallengeTabs";
import { ChallengeFlowGraphic } from "@/components/challenge/ChallengeFlowGraphic";
import { HelpCircle, AlertTriangle, Users, XCircle } from "lucide-react";

export const metadata: Metadata = {
  title: "The Challenge",
  description:
    "Three compounding crises that created contradictory requirements for a $1.3B international organization's AI transformation.",
};

export default function ChallengePage() {
  return (
    <>
      <PageHeader
        title="The Challenge"
        subtitle="Three compounding crises that created contradictory requirements for AI transformation"
      />
      <PageNav current="/challenge" />

      {/* ==================== MODULE 1: CHALLENGE FLOW GRAPHIC ==================== */}
      <section className="py-12 bg-slate-100 border-t-4 border-teal">
        <Container>
          <ChallengeFlowGraphic />
        </Container>
      </section>

      {/* ==================== MODULE 2: THE QUESTION (ENHANCED HOOK) ==================== */}
      <section className="py-12 bg-slate-800">
        <Container>
          <div className="text-center">
            {/* Visual Icon */}
            <div className="mb-6">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-700 border-2 border-slate-600">
                <HelpCircle className="w-8 h-8 text-slate-300" />
              </div>
            </div>

            <h2 className="text-5xl font-bold text-white mb-4">The Question</h2>

            {/* Context line */}
            <p className="text-lg text-slate-400 mb-6">
              For a $1.3B international organization facing 50% revenue decline...
            </p>

            {/* Quote with decorative marks */}
            <div className="relative max-w-4xl mx-auto">
              <span className="absolute -left-4 -top-4 text-6xl text-slate-600 font-serif">&ldquo;</span>
              <p className="text-2xl md:text-3xl text-gray-300 leading-relaxed italic px-8">
                How can an organization deploy enterprise AI to leverage its institutional knowledge advantage, deliver immediate ROI, and rebuild trust with change-fatigued international teams, without top-down mandates, multi-million dollar investments, or degrading its competitive advantage?
              </p>
              <span className="absolute -right-4 -bottom-4 text-6xl text-slate-600 font-serif">&rdquo;</span>
            </div>
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

          {/* MODULE 3A: Key Finding Callout */}
          <div className="bg-amber/20 border-l-4 border-amber rounded-r-lg p-6 mb-8">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-6 h-6 text-amber flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-lg font-semibold mb-2 text-gray-800">Key Finding</h3>
                <p className="text-lg text-gray-700">
                  Three compounding crises created contradictory stakeholder requirements that seemed impossible to satisfy simultaneously.
                </p>
              </div>
            </div>
          </div>

          <p className="text-xl md:text-2xl text-gray-700 leading-relaxed mb-10">
            The organization faced a sudden sector upheaval and dramatic market shift that created
            three compounding crises: competitive survival pressure from market consolidation, a
            financial crisis with projected <span className="font-bold text-navy">50% revenue decline</span>, and deep organizational skepticism
            from a failed transformation and staff reductions. The Board demanded quarterly AI
            progress while the C-Suite required zero-risk investments. Project teams resisted any
            headquarters mandate while customers rejected AI being imposed on them. These requirements
            appeared mutually exclusive.
          </p>

          {/* MODULE 3B: Preview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
            <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-navy/10 rounded-full p-2">
                  <AlertTriangle className="w-5 h-5 text-navy" />
                </div>
                <div className="text-3xl font-bold text-navy">3</div>
              </div>
              <div className="font-semibold text-gray-900 mb-1">Crises</div>
              <div className="text-sm text-gray-600">Compounding: Competitive, Financial, Cultural</div>
            </div>
            <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-teal/10 rounded-full p-2">
                  <Users className="w-5 h-5 text-teal" />
                </div>
                <div className="text-3xl font-bold text-teal">4</div>
              </div>
              <div className="font-semibold text-gray-900 mb-1">Stakeholders</div>
              <div className="text-sm text-gray-600">In Conflict: Board, C-Suite, Teams, Customers</div>
            </div>
            <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-magenta/10 rounded-full p-2">
                  <XCircle className="w-5 h-5 text-magenta" />
                </div>
                <div className="text-3xl font-bold text-magenta">1</div>
              </div>
              <div className="font-semibold text-gray-900 mb-1">Dilemma</div>
              <div className="text-sm text-gray-600">Seemingly impossible: Contradictory constraints</div>
            </div>
          </div>

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

          {/* MODULE 4A: Key Finding Callout */}
          <div className="bg-magenta/10 border-l-4 border-magenta rounded-r-lg p-6 mb-8">
            <div className="flex items-start gap-3">
              <XCircle className="w-6 h-6 text-magenta flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-lg font-semibold mb-2 text-gray-800">Key Finding</h3>
                <p className="text-lg text-gray-700">
                  The organization&apos;s competitive advantage &mdash; institutional knowledge &mdash; must be protected and amplified, not commoditized or made accessible to competitors.
                </p>
              </div>
            </div>
          </div>

          {/* MODULE 4B: Metric Highlights in Text */}
          <p className="text-xl md:text-2xl text-gray-700 leading-relaxed mb-10">
            Sectoral upheaval magnified existing organizational weaknesses into existential threats.
            A decentralized, change-fatigued culture meant any mandated adoption would be resisted. A <span className="font-bold text-navy">50%
            revenue decline</span> meant the organization could not afford multi-million dollar investments or wait <span className="font-bold text-navy">3-4 years</span> for ROI.
            And any approach that commoditized the organization&apos;s key competitive advantage &mdash; institutional knowledge &mdash; would be self-defeating.
          </p>

          {/* MODULE 4C: Preview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
            <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-navy/10 rounded-full p-2">
                  <Users className="w-5 h-5 text-navy" />
                </div>
                <div className="text-lg font-bold text-navy">CULTURE</div>
              </div>
              <div className="text-sm text-gray-700">
                Decentralized, change-fatigued workforce resists any top-down mandates
              </div>
            </div>
            <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-amber/10 rounded-full p-2">
                  <AlertTriangle className="w-5 h-5 text-amber" />
                </div>
                <div className="text-lg font-bold text-amber">FINANCIAL</div>
              </div>
              <div className="text-sm text-gray-700">
                50% revenue decline &mdash; cannot afford large investments or long timelines
              </div>
            </div>
            <div className="bg-white rounded-lg p-6 border border-gray-200 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-magenta/10 rounded-full p-2">
                  <XCircle className="w-5 h-5 text-magenta" />
                </div>
                <div className="text-lg font-bold text-magenta">COMPETITIVE</div>
              </div>
              <div className="text-sm text-gray-700">
                Knowledge trapped in silos &mdash; must be unlocked without commoditizing it
              </div>
            </div>
          </div>

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
