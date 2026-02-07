import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { PageNav } from "@/components/layout/PageNav";
import { PHASES } from "@/lib/constants";
import { ArrowRight, Github } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Implementation Phases",
  description:
    "Six-phase implementation of the funder intelligence system, from shared infrastructure to autonomous multi-agent collaboration",
};

const colorMap = {
  navy: {
    hex: '#1e3a5f',
    bg: 'rgba(30, 58, 95, 0.12)',
    solid: 'bg-navy',
  },
  teal: {
    hex: '#0A6B5C',  // Darker teal for 4.5:1 contrast on light backgrounds
    bg: 'rgba(26, 188, 156, 0.12)',
    solid: 'bg-teal',
  },
  amber: {
    hex: '#92400E',  // Darker amber for 4.5:1 contrast on light backgrounds
    bg: 'rgba(243, 156, 18, 0.12)',
    solid: 'bg-amber',
  },
  magenta: {
    hex: '#7B3F96',  // Darker magenta for 4.5:1 contrast on light backgrounds
    bg: 'rgba(155, 89, 182, 0.12)',
    solid: 'bg-magenta',
  },
};

export default function PhasesPortal() {
  return (
    <>
      <PageHeader
        title="Phase-by-Phase Implementation"
        subtitle="How three siloed divisions became an autonomous multi-agent intelligence system in 6 progressive phases"
      >
        <a
          href="https://github.com/deepdmk/enterprise-ai-case-study"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 text-white/70 hover:text-white transition-colors text-base"
        >
          <Github className="w-5 h-5" />
          deepdmk/enterprise-ai-case-study
        </a>
      </PageHeader>
      <PageNav current="/solution" />

      <section className="py-20">
        <Container>
          {/* Phase Cards */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {PHASES.map((phase) => (
              <Link key={phase.number} href={`/solution/${phase.slug}`} className="group block h-full">
                <div
                  className="rounded-xl p-5 h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 border-b-4"
                  style={{
                    borderColor: colorMap[phase.color].hex,
                    backgroundColor: colorMap[phase.color].bg,
                  }}
                >
                  <div className="flex items-start gap-4 mb-3">
                    <div
                      className="text-white text-2xl font-bold w-14 h-14 rounded-lg flex items-center justify-center flex-shrink-0"
                      style={{ backgroundColor: colorMap[phase.color].hex }}
                    >
                      {phase.number}
                    </div>
                    <div className="flex-1">
                      <h2
                        className="text-lg font-bold mb-1"
                        style={{ color: colorMap[phase.color].hex }}
                      >
                        {phase.title}
                      </h2>
                      <p className="text-sm text-gray-700">{phase.subtitle}</p>
                    </div>
                  </div>
                  <p className="text-gray-700 text-sm mb-4">
                    {phase.description}
                  </p>
                  <div
                    className="flex items-center justify-end text-sm font-medium"
                    style={{ color: colorMap[phase.color].hex }}
                  >
                    Explore Phase
                    <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Scaling Production Card - Centered */}
          <div className="mt-6 flex justify-center">
            <div className="w-full md:max-w-[calc(50%-0.75rem)] lg:max-w-[calc(33.333%-1rem)]">
              <Link href="/solution/scaling-production" className="group block h-full">
                <div className="rounded-xl p-5 h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 bg-gradient-to-br from-navy to-teal text-white">
                  <div className="flex items-start gap-4 mb-3">
                    <div className="bg-white/20 text-white text-2xl font-bold w-14 h-14 rounded-lg flex items-center justify-center flex-shrink-0">
                      ✓
                    </div>
                    <div className="flex-1">
                      <h2 className="text-lg font-bold mb-1">Scaling Production</h2>
                      <p className="text-sm text-white/80">Enterprise deployment with AWS architecture</p>
                    </div>
                  </div>
                  <div className="flex items-center justify-end text-sm font-medium">
                    View Deployment Guide
                    <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </Container>
      </section>

      {/* ==================== CTA: RESULTS ==================== */}
      <section className="py-16 bg-navy">
        <Container>
          <h2 className="text-3xl font-bold text-white mb-6">Next: Results</h2>
          <p className="text-lg text-gray-300 mb-6">
            See the complete investment analysis, strategic value delivered, and what this case study proves about enterprise AI deployment.
          </p>
          <Link
            href="/results"
            className="inline-flex items-center justify-center px-8 py-4 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
          >
            View Results
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
