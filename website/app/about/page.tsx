import Image from "next/image";
import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { PageHeader } from "@/components/layout/PageHeader";
import { SITE_CONFIG } from "@/lib/constants";
import {
  Mail,
  Github,
  Linkedin,
  Cpu,
  TrendingUp,
  Building2,
  Gauge,
  Sparkles,
  ShieldCheck,
  Briefcase,
  ClipboardList,
} from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About This Project",
  description:
    "A comprehensive demonstration of enterprise AI transformation—from strategy through implementation. Learn what this project demonstrates and about the architect behind it.",
};

export default function AboutPage() {
  return (
    <>
      <PageHeader
        title="About This Project"
        subtitle="A comprehensive demonstration of enterprise AI transformation—from strategy to implementation"
      />

      <section className="py-12">
        <Container>
          {/* What This Project Demonstrates */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-navy mb-6">
              What This Project Demonstrates
            </h2>

            <p className="text-lg text-gray-700 leading-relaxed mb-8">
              This project is a complete case study in enterprise AI transformation, demonstrating capabilities across strategic, technical, and organizational domains.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                {
                  icon: Cpu,
                  title: "AI Engineering & Technical Implementation",
                  description:
                    "Production-ready multi-agent system architecture with fine-tuned small language models (LoRA/QLoRA on Llama 3.1 8B), Mixture-of-Experts (MoE) model design, and embedding space architecture using BGE 335M. The implementation includes RAG systems, vector databases, semantic search, and complete LLMOps lifecycle management—from training pipelines to production deployment.",
                },
                {
                  icon: TrendingUp,
                  title: "Business Strategy & Transformation",
                  description:
                    "Strategic approach to AI deployment emphasizing bottom-up emergence over top-down mandates. The six-phase structure delivers incremental value at each stage, reducing risk and enabling strategic optionality—organizations can stop at any phase with retained business value. Cost modeling shows $163.1K Direct Investment ($11,100 infrastructure + $152K training programs) versus $2M+ for traditional approaches.",
                },
                {
                  icon: Building2,
                  title: "Enterprise Architecture & System Design",
                  description:
                    "Complete enterprise architecture spanning local development through cloud-scale production. Phase 0 establishes foundational registries enabling systematic learning. The architecture supports multiple deployment targets (AWS SageMaker/Bedrock, Azure ML, Databricks, local infrastructure) without vendor lock-in.",
                },
                {
                  icon: Gauge,
                  title: "LLMOps & Production Operations",
                  description:
                    "Comprehensive MLOps implementation including model versioning, experiment tracking, training pipeline orchestration, and production deployment patterns. Phase 0's infrastructure includes 151 passing tests validating registry reliability. Documentation covers local development to enterprise-scale AWS deployment.",
                },
                {
                  icon: Sparkles,
                  title: "Organizational Change & Discovery-Led Transformation",
                  description:
                    "Organizational transformation from three siloed divisions into a coordinated intelligence system. Phase 4's 90-day discovery period captures real usage patterns, which Phase 5 transforms into a trained orchestrator—embodying discovery-led transformation where coordination emerges from observed behavior.",
                },
                {
                  icon: ShieldCheck,
                  title: "Governance, Risk Management & Compliance",
                  description:
                    "AI governance frameworks built into the architecture from Phase 0. The phased approach inherently manages risk by delivering testable value incrementally. Infrastructure design includes audit trails, experiment tracking, and model lineage—critical for regulatory compliance.",
                },
                {
                  icon: Briefcase,
                  title: "Business Development & Market Positioning",
                  description:
                    "Complete technical case study serving as thought leadership and market differentiation. The project articulates a clear value proposition: enterprise AI capabilities at 1-5% of traditional costs while preserving strategic optionality. The framework positions as an alternative to vendor-locked approaches.",
                },
                {
                  icon: ClipboardList,
                  title: "Program Management & Delivery Excellence",
                  description:
                    "Six-phase program structure with clear dependencies, resource requirements, and success criteria. Each phase includes cost estimates, timeline projections, and delivered capabilities. Phase 0's 151 passing tests demonstrate quality assurance rigor.",
                },
              ].map((card, index) => {
                const IconComponent = card.icon;
                return (
                  <div
                    key={index}
                    className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm hover:shadow-md hover:border-teal/50 hover:-translate-y-1 transition-all duration-200 focus-within:ring-2 focus-within:ring-teal/50"
                  >
                    <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                      <IconComponent className="w-6 h-6 text-teal" />
                    </div>
                    <h3 className="text-lg font-bold text-navy mb-3">
                      {card.title}
                    </h3>
                    <p className="text-gray-700 text-base leading-relaxed">
                      {card.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* About the Author */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-navy mb-8">
              About the Author
            </h2>

            <div className="grid md:grid-cols-3 gap-8 items-start">
              {/* Left column: Image (1/3 width) */}
              <div className="md:col-span-1">
                <div className="relative w-full aspect-square rounded-lg overflow-hidden">
                  <Image
                    src="/images/daniel-dimick-headshot.jpg"
                    alt="Daniel Dimick"
                    fill
                    className="object-cover"
                  />
                </div>
              </div>

              {/* Right column: Content (2/3 width) */}
              <div className="md:col-span-2 space-y-4 text-gray-700 leading-relaxed">
                <p>
                  This implementation was built by <strong>Daniel Dimick</strong>, who operates across the complete AI value chain—from C-suite strategy through organizational transformation to hands-on technical implementation.
                </p>

                <p>
                  <strong>Background:</strong> Enterprise transformation consultant and IBM Certified AI Engineer. Directed in-house consulting unit for $1.4B transnational organization spanning 115 countries. Advised C-suite executives and government ministers across 30+ countries on AI strategy, organizational transformation, and governance frameworks.
                </p>

                <p>
                  <strong>Technical expertise:</strong> Production multi-agent systems, fine-tuned SLMs, RAG architectures, LLMOps, and data science. Hands-on implementation with PyTorch, Transformers, LangChain, AWS SageMaker, Databricks, and Azure ML. Lean Six Sigma Black Belt, Certified Business Architect (CBA), and Agile/Scrum (DASSM).
                </p>

                <p>
                  <strong>Approach:</strong> Strategic advisory (designing transformation roadmaps with executives), transformation execution (leading cross-functional teams delivering measurable outcomes), and technical implementation (building and deploying AI systems). This ensures solutions that executives understand, organizations can adopt, and engineers can build.
                </p>

                {/* Social Links */}
                <div className="flex gap-4 pt-4">
                  <a
                    href="https://www.linkedin.com/in/dpdimick"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-navy hover:text-teal transition-colors"
                  >
                    <Linkedin className="w-5 h-5" />
                    <span className="text-base font-medium">LinkedIn</span>
                  </a>
                  <a
                    href="https://github.com/deepdmk/enterprise-ai-case-study"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-navy hover:text-teal transition-colors"
                  >
                    <Github className="w-5 h-5" />
                    <span className="text-base font-medium">GitHub</span>
                  </a>
                  <a
                    href={`mailto:${SITE_CONFIG.email}`}
                    className="inline-flex items-center gap-2 text-navy hover:text-teal transition-colors"
                  >
                    <Mail className="w-5 h-5" />
                    <span className="text-base font-medium">Email</span>
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* CTA Section */}
          <div className="bg-gradient-to-br from-navy to-teal text-white p-12 rounded-lg text-center">
            <h2 className="text-3xl font-bold mb-4">Explore the Implementation</h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Review the complete 6-phase implementation, explore the codebase on GitHub, or reach out to discuss how this approach applies to your organizational context.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/solution"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-navy font-medium rounded-md hover:bg-white/90 transition-colors"
              >
                <span>Review the Phases</span>
              </Link>
              <a
                href="https://github.com/deepdmk/enterprise-ai-case-study"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-teal/20 text-white border border-white/20 font-medium rounded-md hover:bg-teal/30 transition-colors"
              >
                <Github className="w-5 h-5" />
                <span>View on GitHub</span>
              </a>
              <a
                href={`mailto:${SITE_CONFIG.email}`}
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-teal/20 text-white border border-white/20 font-medium rounded-md hover:bg-teal/30 transition-colors"
              >
                <Mail className="w-5 h-5" />
                <span>Get in Touch</span>
              </a>
            </div>
          </div>
        </Container>
      </section>
    </>
  );
}
