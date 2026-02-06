import { Container } from "@/components/layout/Container";
import { HeroEnhanced } from "@/components/home/mockups/HeroEnhanced";
import { ElevatorPitchScannable } from "@/components/home/mockups/ElevatorPitchScannable";
import { FourPathsWithGuidance } from "@/components/home/mockups/FourPathsWithGuidance";
import { JourneyGraphicResponsive } from "@/components/home/mockups/JourneyGraphicResponsive";
import { CaseStudyTabsUpdated } from "@/components/home/mockups/CaseStudyTabsUpdated";
import {
  SocialProofStrip,
  StatsBar,
} from "@/components/home/mockups/SocialProofStrip";
import {
  DemonstratesSectionBalanced,
  DemonstratesSectionCompact,
  DemonstratesSectionMinimal,
} from "@/components/home/mockups/DemonstratesSection";

export const metadata = {
  title: "Home Page Mockups",
  description: "Visual mockups for home page improvements",
};

export default function MockupsPage() {
  return (
    <div className="min-h-screen">
      {/* Page Header */}
      <div className="bg-gray-900 text-white py-8">
        <Container>
          <h1 className="text-3xl font-bold mb-2">Home Page Mockups</h1>
          <p className="text-gray-400">
            Preview each proposed improvement. Scroll down to see all mockups.
          </p>
        </Container>
      </div>

      {/* Mockup A: Enhanced Hero */}
      <section className="border-b-4 border-teal">
        <div className="bg-gray-800 text-white py-4">
          <Container>
            <div className="flex items-center gap-3">
              <span className="bg-teal text-white text-sm font-bold px-3 py-1 rounded">
                Mockup A
              </span>
              <h2 className="text-xl font-semibold">
                Enhanced Hero with Visual Hook
              </h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Adds metric badge, value proposition, and scroll CTA. Subtle
              decorative elements add visual interest.
            </p>
          </Container>
        </div>
        <HeroEnhanced />
      </section>

      {/* Mockup B: Scannable Elevator Pitch */}
      <section className="border-b-4 border-teal">
        <div className="bg-gray-800 text-white py-4">
          <Container>
            <div className="flex items-center gap-3">
              <span className="bg-teal text-white text-sm font-bold px-3 py-1 rounded">
                Mockup B
              </span>
              <h2 className="text-xl font-semibold">
                Scannable Elevator Pitch
              </h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Breaks dense paragraph into 4 scannable cards with icons and
              metrics. Lighter background for visual breathing room.
            </p>
          </Container>
        </div>
        <ElevatorPitchScannable />
      </section>

      {/* Mockup C: Four Paths with Guidance */}
      <section className="border-b-4 border-teal">
        <div className="bg-gray-800 text-white py-4">
          <Container>
            <div className="flex items-center gap-3">
              <span className="bg-teal text-white text-sm font-bold px-3 py-1 rounded">
                Mockup C
              </span>
              <h2 className="text-xl font-semibold">
                Four Paths with Reader Guidance
              </h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Adds persona hints, reading time, and highlights Case Summary as
              recommended starting point.
            </p>
          </Container>
        </div>
        <FourPathsWithGuidance />
      </section>

      {/* Mockup D: Responsive Journey */}
      <section className="border-b-4 border-teal">
        <div className="bg-gray-800 text-white py-4">
          <Container>
            <div className="flex items-center gap-3">
              <span className="bg-teal text-white text-sm font-bold px-3 py-1 rounded">
                Mockup D
              </span>
              <h2 className="text-xl font-semibold">
                Responsive Journey Graphic
              </h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Vertical timeline on mobile, horizontal on desktop. No horizontal
              scroll required. Resize browser to see responsive behavior.
            </p>
          </Container>
        </div>
        <div className="bg-gray-200 p-10">
          <JourneyGraphicResponsive />
        </div>
      </section>

      {/* Updated Tabs Component */}
      <section className="border-b-4 border-teal">
        <div className="bg-gray-800 text-white py-4">
          <Container>
            <div className="flex items-center gap-3">
              <span className="bg-navy text-white text-sm font-bold px-3 py-1 rounded">
                Tabs Update
              </span>
              <h2 className="text-xl font-semibold">
                Tabbed Interface with Responsive Journey
              </h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Keeps both tabs. &quot;The Journey&quot; uses the responsive graphic. &quot;What This
              Demonstrates&quot; remains unchanged.
            </p>
          </Container>
        </div>
        <div className="bg-gray-50 py-3">
          <Container>
            <CaseStudyTabsUpdated />
          </Container>
        </div>
      </section>

      {/* Mockup F: Improved "Demonstrates" Section */}
      <section className="border-b-4 border-teal">
        <div className="bg-gray-800 text-white py-4">
          <Container>
            <div className="flex items-center gap-3">
              <span className="bg-amber text-white text-sm font-bold px-3 py-1 rounded">
                Mockup F
              </span>
              <h2 className="text-xl font-semibold">
                Improved &quot;What This Demonstrates&quot; (2x2 Grid)
              </h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Three variants: Balanced (recommended), Compact, and Minimal.
            </p>
          </Container>
        </div>
        <div className="bg-gray-200 p-6 space-y-8">
          <div>
            <div className="bg-teal/20 py-2 px-4 mb-4 rounded border border-teal/40">
              <span className="text-sm font-medium text-teal-on-light">
                Variant 1: Balanced (Recommended) — 2x2 with full descriptions
              </span>
            </div>
            <Container>
              <DemonstratesSectionBalanced />
            </Container>
          </div>
          <div>
            <div className="bg-white/50 py-2 px-4 mb-4 rounded">
              <span className="text-sm font-medium text-gray-700">
                Variant 2: Compact — shorter descriptions
              </span>
            </div>
            <Container>
              <DemonstratesSectionCompact />
            </Container>
          </div>
          <div>
            <div className="bg-white/50 py-2 px-4 mb-4 rounded">
              <span className="text-sm font-medium text-gray-700">
                Variant 3: Minimal — tags instead of prose
              </span>
            </div>
            <Container>
              <DemonstratesSectionMinimal />
            </Container>
          </div>
        </div>
      </section>

      {/* Mockup E: Social Proof Strip */}
      <section className="border-b-4 border-teal">
        <div className="bg-gray-800 text-white py-4">
          <Container>
            <div className="flex items-center gap-3">
              <span className="bg-teal text-white text-sm font-bold px-3 py-1 rounded">
                Mockup E
              </span>
              <h2 className="text-xl font-semibold">
                Social Proof / Technology Strip
              </h2>
            </div>
            <p className="text-gray-400 text-sm mt-1">
              Shows technologies used and deployment options. Two variants
              shown.
            </p>
          </Container>
        </div>
        <div className="space-y-4">
          <div>
            <div className="bg-gray-100 py-2 px-4">
              <span className="text-sm text-gray-600">
                Variant 1: Technology Pills
              </span>
            </div>
            <SocialProofStrip />
          </div>
          <div>
            <div className="bg-gray-100 py-2 px-4">
              <span className="text-sm text-gray-600">
                Variant 2: Stats Bar
              </span>
            </div>
            <StatsBar />
          </div>
        </div>
      </section>

      {/* Combined Preview */}
      <section>
        <div className="bg-gray-900 text-white py-6">
          <Container>
            <h2 className="text-2xl font-bold mb-2">
              Combined Preview: Full Page Flow
            </h2>
            <p className="text-gray-400">
              See how these mockups work together as a complete home page
              redesign.
            </p>
          </Container>
        </div>

        {/* Combined mockups */}
        <HeroEnhanced />
        <StatsBar />
        <ElevatorPitchScannable />
        <FourPathsWithGuidance />
        {/* Tabs with responsive journey + What This Demonstrates */}
        <div className="bg-gray-50 py-3">
          <Container>
            <CaseStudyTabsUpdated />
          </Container>
        </div>
        <SocialProofStrip />
      </section>

      {/* Navigation hint */}
      <div className="bg-gray-100 py-8 text-center">
        <p className="text-gray-600">
          View this page at{" "}
          <code className="bg-gray-200 px-2 py-1 rounded text-sm">
            /mockups
          </code>
        </p>
      </div>
    </div>
  );
}
