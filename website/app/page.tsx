import { Container } from "@/components/layout/Container";
import { HeroEnhanced } from "@/components/home/mockups/HeroEnhanced";
import { ElevatorPitchScannable } from "@/components/home/mockups/ElevatorPitchScannable";
import { FourPathsWithGuidance } from "@/components/home/mockups/FourPathsWithGuidance";
import { CaseStudyTabsUpdated } from "@/components/home/mockups/CaseStudyTabsUpdated";
import { SocialProofStrip } from "@/components/home/mockups/SocialProofStrip";
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
      {/* Section 1: Enhanced Hero */}
      <HeroEnhanced />

      {/* Section 2: Scannable Elevator Pitch */}
      <ElevatorPitchScannable />

      {/* Section 3: Pick Your Path with Guidance */}
      <FourPathsWithGuidance />

      {/* Section 4: Tabbed Interface (Journey + Demonstrates) */}
      <section className="py-3 bg-gray-50">
        <Container>
          <CaseStudyTabsUpdated />
        </Container>
      </section>

      {/* Section 5: Built With Strip */}
      <SocialProofStrip />

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
                who operates across the complete value chain, from strategy
                through implementation.
              </p>
              <div className="flex flex-wrap justify-center gap-6 mb-6">
                <a
                  href="https://www.linkedin.com/in/dpdimick"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-white/80 hover:text-teal-on-navy transition-colors"
                >
                  <Linkedin className="w-5 h-5" />
                  <span className="text-base font-medium">LinkedIn</span>
                </a>
                <a
                  href="https://github.com/deepdmk/enterprise-ai-case-study"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-white/80 hover:text-teal-on-navy transition-colors"
                >
                  <Github className="w-5 h-5" />
                  <span className="text-base font-medium">GitHub</span>
                </a>
                <a
                  href="mailto:d.dimick@eastsoutheast.international"
                  className="inline-flex items-center gap-2 text-white/80 hover:text-teal-on-navy transition-colors"
                >
                  <Mail className="w-5 h-5" />
                  <span className="text-base font-medium">Email</span>
                </a>
              </div>
              <Link
                href="/about"
                className="inline-flex items-center text-teal-on-navy hover:text-teal-on-navy/80 font-semibold transition-colors"
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
