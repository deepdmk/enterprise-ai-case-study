import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { PageNav } from "@/components/layout/PageNav";
import { Container } from "@/components/layout/Container";
import { TransformationFrameworkTabs } from "./TransformationTabs";

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
          <div className="flex justify-center">
            <Image
              src="/transformation-flow.png"
              alt="Strategy Flow: Strategic Analysis → Strategy Development → Transformation Framework"
              width={1200}
              height={400}
              className="w-full max-w-[1200px] h-auto"
            />
          </div>
        </Container>
      </section>

      {/* ==================== SECTION 1: TRANSFORMATION FRAMEWORK ==================== */}
      <section className="py-16 bg-navy/10 border-t-4 border-teal">
        <Container>
          <h2 className="text-5xl font-bold text-navy mb-4 flex items-center">
            <span className="bg-teal text-white px-3 py-1 rounded mr-3 text-base">
              1
            </span>
            Transformation Framework
          </h2>

          <p className="text-xl md:text-2xl text-gray-700 leading-relaxed mb-10">
            The strategic approach alone couldn&apos;t satisfy all 19 CTQs. Many depended on how the
            transformation was timed and implemented. We applied three frameworks to address this:
            Three Horizons for staging with decision points, Roadmap for integrating technical and
            change management, and Balanced Scorecard for data-driven decisions at each phase boundary.
          </p>

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

    </>
  );
}
