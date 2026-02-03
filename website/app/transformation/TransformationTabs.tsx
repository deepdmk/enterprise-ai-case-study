"use client";

import Link from "next/link";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui";

function ThreeHorizonsJourney() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Transformational Approach
      </h3>

      <p className="text-lg text-gray-700 mb-4">
        <strong>Approach:</strong> Three Horizons Framework
      </p>

      <p className="text-lg text-gray-700 mb-4">
        <strong>Purpose:</strong> Manage the strategic timing paradox between
        defending current competitive position while simultaneously building
        emerging capabilities and creating transformative future options. Three
        Horizons enables simultaneous execution across all three timeframes with
        clear decision points at horizon boundaries.
      </p>

      <div className="bg-magenta/5 border-l-4 border-magenta p-5 rounded mb-6">
        <p className="text-lg text-gray-700">
          <strong>Outcome:</strong> The framework revealed the optimal staging
          sequence: defend core operations first (H1: months 0-9), then leverage
          that foundation to build proprietary competitive advantages (H2:
          months 7-12), and finally create transformative capabilities (H3:
          months 10-18). Overlapping horizons maintain momentum while providing
          natural decision points to validate performance before increasing
          investment.
        </p>
      </div>

      <div className="space-y-4 mb-6">
        <div className="bg-white border border-gray-200 p-4 rounded">
          <p className="text-lg text-gray-700">
            <strong>Horizon 1 (Months 0-9): Defend &amp; Extend Core</strong>
          </p>
          <ul className="list-disc pl-6 text-lg text-gray-700 mt-2 space-y-1">
            <li>
              Phases 0-2: Registry Foundation, Knowledge Access, Task Automation
            </li>
            <li>Direct Investment: $106K | Labor Allocation: $412.5K</li>
          </ul>
        </div>

        <div className="bg-white border border-gray-200 p-4 rounded">
          <p className="text-lg text-gray-700">
            <strong>
              Horizon 2 (Months 7-12): Build Emerging Advantages
            </strong>
          </p>
          <ul className="list-disc pl-6 text-lg text-gray-700 mt-2 space-y-1">
            <li>Phase 3: Division Intelligence (MoE architecture)</li>
            <li>Direct Investment: $31.2K | Labor Allocation: $337.5K</li>
          </ul>
        </div>

        <div className="bg-white border border-gray-200 p-4 rounded">
          <p className="text-lg text-gray-700">
            <strong>
              Horizon 3 (Months 10-18): Create Transformative Options
            </strong>
          </p>
          <ul className="list-disc pl-6 text-lg text-gray-700 mt-2 space-y-1">
            <li>Phases 4-5: Agentic Discovery, Orchestrated System</li>
            <li>Direct Investment: $25.9K | Labor Allocation: $360K</li>
          </ul>
        </div>
      </div>

      <Link
        href="/transformation/three-horizons"
        className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors text-lg"
      >
        View Three Horizons Framework &rarr;
      </Link>
    </div>
  );
}

function TransformationRoadmap() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Phase-by-Phase Implementation
      </h3>

      <p className="text-lg text-gray-700 mb-4">
        <strong>Approach:</strong> Transformation Roadmap
      </p>

      <p className="text-lg text-gray-700 mb-4">
        <strong>Purpose:</strong> Translate strategic horizons into concrete
        phase-by-phase execution that integrates technical implementation with
        change management from design. This roadmap embeds ADKAR change
        management directly into phase design, user segmentation, and capability
        progression.
      </p>

      <div className="bg-magenta/5 border-l-4 border-magenta p-5 rounded mb-6">
        <p className="text-lg text-gray-700">
          <strong>Outcome:</strong> The integrated roadmap solved the change
          management challenge before it became one. Instead of asking &quot;how
          do we get people to use this?&quot;, the phased progression creates
          natural adoption: Phase 1 serves all 8,000 staff universally, Phase 2
          targets 200-500 who discovered specific needs, continuing through
          expert tiers. Each phase delivers standalone value that creates pull
          for the next phase.
        </p>
      </div>

      <div className="bg-white border border-gray-200 p-4 rounded mb-4">
        <p className="text-lg text-gray-700 font-semibold mb-2">
          Investment Structure:
        </p>
        <ul className="list-disc pl-6 text-lg text-gray-700 space-y-1">
          <li>
            <strong>Direct Investment:</strong> $163.1K ($11.1K infrastructure +
            $152K training)
          </li>
          <li>
            <strong>Labor Allocation:</strong> $1,110K (5 FTE over 18 months)
          </li>
        </ul>
      </div>

      <Link
        href="/transformation/roadmap"
        className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors text-lg"
      >
        View Transformation Roadmap &rarr;
      </Link>
    </div>
  );
}

function MonitoringProgress() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">Measuring Progress</h3>

      <p className="text-lg text-gray-700 mb-4">
        <strong>Approach:</strong> Balanced Scorecard
      </p>

      <p className="text-lg text-gray-700 mb-4">
        <strong>Purpose:</strong> Enable data-driven progression decisions
        through quarterly performance measurement across four interdependent
        perspectives: Learning &amp; Growth, Internal Process, User &amp;
        Customer, and Financial. Provides leading indicators that reveal
        problems at quarterly boundaries when decisions can still be made.
      </p>

      <div className="bg-magenta/5 border-l-4 border-magenta p-5 rounded mb-6">
        <p className="text-lg text-gray-700">
          <strong>Key Insight:</strong> Quarterly measurement enables data-driven
          progression decisions at each horizon boundary based on leading
          indicators, not deferred ROI. Unlike deferred ROI models that gamble
          on 18-48 month outcomes, this enables empirical validation every 90
          days.
        </p>
      </div>

      <Link
        href="/transformation/balanced-scorecard"
        className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors text-lg"
      >
        View Balanced Scorecard &rarr;
      </Link>
    </div>
  );
}

/* ───────────────────── Exported Tabbed Section ───────────────────── */

export function TransformationFrameworkTabs() {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
      <Tabs defaultValue="horizons">
        <TabsList className="p-1 m-4 rounded-lg flex gap-2" style={{ backgroundColor: 'rgba(26, 188, 156, 0.1)' }}>
          <TabsTrigger
            value="horizons"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal data-[state=active]:text-white data-[state=active]:shadow-sm text-teal hover:bg-teal/10"
          >
            3-Horizons Journey
          </TabsTrigger>
          <TabsTrigger
            value="roadmap"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal data-[state=active]:text-white data-[state=active]:shadow-sm text-teal hover:bg-teal/10"
          >
            Transformation Roadmap
          </TabsTrigger>
          <TabsTrigger
            value="monitoring"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal data-[state=active]:text-white data-[state=active]:shadow-sm text-teal hover:bg-teal/10"
          >
            Monitoring Progress
          </TabsTrigger>
        </TabsList>

        <div className="px-4 pb-4">
          <TabsContent value="horizons">
            <ThreeHorizonsJourney />
          </TabsContent>
          <TabsContent value="roadmap">
            <TransformationRoadmap />
          </TabsContent>
          <TabsContent value="monitoring">
            <MonitoringProgress />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
