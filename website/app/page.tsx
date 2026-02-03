import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { CaseJourneyGraphic } from "@/components/home/CaseJourneyGraphic";
import FourPathsGateway from "@/components/home/FourPathsGateway";
import Link from "next/link";
import {
  TrendingUp,
  Sparkles,
  Cpu,
  Building2,
  Linkedin,
  Github,
  Mail,
  ArrowRight,
} from "lucide-react";

export const metadata = {
  title: "Emergent Enterprise AI: Strategy through Implementation",
  description:
    "Enterprise AI capabilities built from strategy through implementation. A case study demonstrating what happens when business strategy, organizational transformation, and AI engineering work together.",
};

export default function HomePage() {
  return (
    <div className="relative">
      {/* Section 1: Hero (compact) */}
      <section className="bg-gradient-to-br from-navy to-teal-dark py-16">
        <Container>
          <div className="max-w-6xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-3">
              Case Study in Emergent Enterprise AI
            </h1>
            <p className="text-xl md:text-2xl text-white/90">
              From Strategy Through Implementation
            </p>
          </div>
        </Container>
      </section>

      {/* Sections 2-4: Connected Unit (Elevator Pitch + Pick Your Path + Graphic) */}
      <section className="py-3 bg-gray-50">
        <Container>
          {/* Section 2: Elevator Pitch - top of connected unit */}
          <div className="bg-navy p-10 rounded-t-lg">
            <p className="text-xl md:text-2xl font-bold italic text-white leading-relaxed text-center max-w-5xl mx-auto">
              Enterprise AI doesn&apos;t require massive investments in
              proprietary LLM platforms. This case study follows a $1.3B
              international organization through a complete AI transformation
              — showing how mid-to-large enterprises can build their own AI
              capabilities, tailored to their context, discoverable through
              use, and strategically differentiating. It demonstrates
              what&apos;s realistically achievable when strategy,
              transformation expertise, and technical implementation come
              together.
            </p>
          </div>

          {/* Section 3: Pick Your Path - middle of connected unit */}
          <FourPathsGateway />

          {/* Section 4: Graphic Section - bottom of connected unit */}
          <div className="bg-gray-200 p-10 rounded-b-lg">
            <h3 className="text-xl font-bold text-navy text-center mb-6">
              Enterprise 18-month Journey from Strategy &rarr; Transformation &rarr; Deployment
            </h3>
            <CaseJourneyGraphic />
          </div>
        </Container>
      </section>

      {/* Section 5: What This Demonstrates */}
      <section className="py-3 bg-white">
        <Container>
          <div className="bg-gradient-to-br from-teal/25 to-teal/15 py-10 pr-10 pl-12 rounded-lg border-l-4 border-teal">
            <h2 className="text-3xl font-bold text-navy mb-6">
              What This Case Study Demonstrates
            </h2>

            <p className="text-lg text-gray-700 leading-relaxed mb-10 max-w-4xl">
              This case study demonstrates capabilities across multiple domains —
              business strategy, organizational transformation, and technical
              implementation — as well as the synergistic value created when these
              disciplines work together. Strategic analysis informs transformation
              design, which shapes technical architecture. Equally, understanding
              downstream technical possibilities allows upstream phases to be
              honed for optionality — designing strategy that accommodates
              what&apos;s architecturally feasible, and shaping transformation to
              leverage what the technology enables. This bidirectional integration
              creates solutions no single discipline achieves alone.
            </p>

            <h3 className="text-xl font-semibold text-navy mb-6">
              What You&apos;ll Find
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <TrendingUp className="w-6 h-6 text-teal" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  Business Strategy &amp; Transformation
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Strategic analysis using established frameworks (Porter&apos;s
                  Five Forces, McKinsey 7S, SWOT, Pugh Matrix), consolidating
                  into Critical to Quality specifications and strategic approach
                  for transformation
                </p>
              </Card>

              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <Sparkles className="w-6 h-6 text-teal" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  Organizational Change &amp; Discovery
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Discovery-led transformation through Kaizen principles:
                  empowering staff at customer value creation points to target AI
                  uses where they add most value, building ownership and agency
                  through targeted experimentation, with phased optionality
                  enabling adaptation and pivots along the journey
                </p>
              </Card>

              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <Cpu className="w-6 h-6 text-teal" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  AI Engineering &amp; Technical Implementation
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Complete technical stack: fine-tuned SLMs using LoRA/QLoRA, MoE
                  division agents, custom embedding space for semantic search,
                  multi-agent orchestration with A2A protocol, full LLMOps
                  lifecycle from model training through production, leveraging
                  AGNO framework for seamless integration with AWS, Azure, and
                  other platforms
                </p>
              </Card>

              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <Building2 className="w-6 h-6 text-teal" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  Enterprise Architecture &amp; System Design
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Architecture designed for deployment optionality: feasible
                  self-deployment on local infrastructure, scalable deployment on
                  cloud platforms (AWS Bedrock, SageMaker, Azure), or integration
                  as sub-agent/tool with other enterprise solutions via AGNO — no
                  vendor lock-in, strategic flexibility preserved
                </p>
              </Card>
            </div>
          </div>
        </Container>
      </section>

      {/* Section 6: About the Architect */}
      <section className="py-3 bg-white">
        <Container>
          <div className="bg-navy py-12 px-8 rounded-lg">
            <div className="max-w-2xl mx-auto text-center">
              <h2 className="text-3xl font-bold text-white mb-4">
                About the Architect
              </h2>
              <p className="text-lg text-white/90 mb-6">
                Built by an enterprise transformation consultant and AI engineer
                who operates across the complete value chain — from strategy
                through implementation.
              </p>
              <div className="flex flex-wrap justify-center gap-6 mb-6">
                <a
                  href="https://www.linkedin.com/in/dpdimick"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-white/80 hover:text-teal transition-colors"
                >
                  <Linkedin className="w-5 h-5" />
                  <span className="text-base font-medium">LinkedIn</span>
                </a>
                <a
                  href="https://github.com/emergent-enterprise-ai"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-white/80 hover:text-teal transition-colors"
                >
                  <Github className="w-5 h-5" />
                  <span className="text-base font-medium">GitHub</span>
                </a>
                <a
                  href="mailto:work.dimick@gmail.com"
                  className="inline-flex items-center gap-2 text-white/80 hover:text-teal transition-colors"
                >
                  <Mail className="w-5 h-5" />
                  <span className="text-base font-medium">Email</span>
                </a>
              </div>
              <Link
                href="/about"
                className="inline-flex items-center text-teal hover:text-teal/80 font-semibold transition-colors"
              >
                View Full Profile
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </div>
          </div>
        </Container>
      </section>
    </div>
  );
}
