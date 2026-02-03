import { Container } from "@/components/layout/Container";
import { CaseStudyTabs } from "@/components/home/CaseStudyTabs";
import FourPathsGateway from "@/components/home/FourPathsGateway";
import Link from "next/link";
import {
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
              international enterprise through a complete AI transformation
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

          {/* Sections 4-5: Tabbed Interface - bottom of connected unit */}
          <CaseStudyTabs />
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
                  href="https://github.com/deepdmk/enterprise-ai-case-study"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-white/80 hover:text-teal transition-colors"
                >
                  <Github className="w-5 h-5" />
                  <span className="text-base font-medium">GitHub</span>
                </a>
                <a
                  href="mailto:d.dimick@eastsoutheast.international"
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
