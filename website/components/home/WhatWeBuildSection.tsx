import { Container } from "@/components/layout/Container";
import { CheckCircle } from "lucide-react";

const outcomes = [
  {
    title: "Competitive moat from proprietary data",
    description:
      "AI trained exclusively on operations, customer relationships, and organizational knowledge creates advantage competitors cannot buy or replicate. Intelligence compounds over time as the system learns from unique workflows and data.",
  },
  {
    title: "Built from teams outward, not top-down",
    description:
      "Implementation starts at the team level where people see immediate value in their daily work, then builds enterprise capability through organic adoption. No forced reorganization or mandated change management, teams choose to expand usage because it solves real problems.",
  },
  {
    title: "Strategic optionality with ROI at every phase",
    description:
      "Each phase delivers standalone ROI with returns immediately visible, not deferred to project completion. Organizations can stop at any point and retain everything built, or continue scaling toward full orchestration with bounded risk of less than $5K per phase.",
  },
  {
    title: "Differentiation with economic advantage",
    description:
      "Build strategic capabilities that set organizations apart from competition while spending 1-5% of traditional enterprise AI deployment costs. Proprietary models trained on company data provide capabilities competitors cannot access through generic AI solutions.",
  },
];

export function WhatWeBuildSection() {
  return (
    <section className="bg-white py-16 md:py-20">
      <Container size="content">
        <h2 className="text-4xl font-bold text-navy text-center mb-6">
          What We Built
        </h2>
        <p className="text-xl text-gray-700 text-center max-w-3xl mx-auto mb-12">
          A complete enterprise AI system that starts with what teams actually value and builds
          outward from there. Built on proprietary data and designed around customers, it creates
          competitive advantage through bottom-up adoption where teams choose to use it because it
          solves their problems. Strategic optionality at every phase means organizations can stop
          with value retained or scale to full enterprise orchestration.
        </p>

        <div className="grid md:grid-cols-2 gap-8">
          {outcomes.map((outcome) => (
            <div
              key={outcome.title}
              className="bg-gray-50 rounded-lg p-6 border border-gray-100"
            >
              <div className="flex items-start gap-3">
                <CheckCircle className="w-6 h-6 text-teal flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-lg font-bold text-navy mb-2">
                    {outcome.title}
                  </h3>
                  <p className="text-gray-700 leading-relaxed">
                    {outcome.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
