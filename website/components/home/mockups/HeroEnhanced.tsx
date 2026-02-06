"use client";

import { Container } from "@/components/layout/Container";
import { ArrowDown, Sparkles } from "lucide-react";

/**
 * MOCKUP A: Enhanced Hero with Visual Hook
 *
 * Changes from original:
 * - Added key metric callout ("18 months")
 * - Added brief value proposition line
 * - Added animated scroll CTA button
 * - Added subtle floating decorative elements
 */
export function HeroEnhanced() {
  const scrollToContent = () => {
    document.getElementById("pick-your-path")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative bg-gradient-to-br from-navy to-teal-dark py-20 overflow-hidden">
      {/* Subtle decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-[10%] w-64 h-64 bg-teal/10 rounded-full blur-3xl" />
        <div className="absolute bottom-10 right-[15%] w-48 h-48 bg-white/5 rounded-full blur-2xl" />
      </div>

      <Container>
        <div className="relative max-w-6xl mx-auto text-center">
          {/* Key metric badge */}
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 mb-6">
            <Sparkles className="w-4 h-4 text-teal-on-navy" />
            <span className="text-sm font-medium text-white/90">
              18 months from strategy to deployment
            </span>
          </div>

          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
            Case Study in Emergent Enterprise AI
          </h1>

          <p className="text-xl md:text-2xl text-white/90 mb-3">
            From Strategy Through Implementation
          </p>

          {/* Value proposition line */}
          <p className="text-lg text-white/70 max-w-2xl mx-auto mb-8">
            See how a $1.3B international enterprise built proprietary AI capabilities
            without vendor lock-in
          </p>

          {/* Scroll CTA */}
          <button
            onClick={scrollToContent}
            className="group inline-flex flex-col items-center gap-2 text-white/60 hover:text-white transition-colors"
          >
            <span className="text-sm font-medium">Explore the case study</span>
            <ArrowDown className="w-5 h-5 animate-bounce" />
          </button>
        </div>
      </Container>
    </section>
  );
}
