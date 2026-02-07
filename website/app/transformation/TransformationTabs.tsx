"use client";

import Link from "next/link";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui";

function ThreeHorizonsJourney() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Strategic Staging
      </h3>

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="bg-teal/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Approach:</span>
          <span className="ml-2 font-semibold text-teal-dark">Three Horizons Framework</span>
        </div>
      </div>

      <p className="text-base text-gray-700 mb-6">
        Manage the strategic timing paradox between defending current competitive position while simultaneously building emerging capabilities and creating transformative future options. Three Horizons enables simultaneous execution across all three timeframes with clear decision points at horizon boundaries.
      </p>

      {/* Horizon Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">H1</span>
            <span className="font-semibold text-navy">Defend & Extend</span>
          </div>
          <p className="text-sm text-gray-500 mb-2">Months 0-9</p>
          <p className="text-base text-gray-600 mb-2">Phases 0-2: Foundation, Knowledge Access, Task Automation</p>
          <div className="flex gap-2 flex-wrap">
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">$106K direct</span>
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">$412.5K labor</span>
          </div>
        </div>
        <div className="bg-amber/5 border-l-4 border-amber rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-amber text-white text-xs font-bold px-2 py-1 rounded">H2</span>
            <span className="font-semibold text-navy">Build Emerging</span>
          </div>
          <p className="text-sm text-gray-500 mb-2">Months 7-12</p>
          <p className="text-base text-gray-600 mb-2">Phase 3: Division Intelligence (MoE architecture)</p>
          <div className="flex gap-2 flex-wrap">
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">$31.2K direct</span>
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">$337.5K labor</span>
          </div>
        </div>
        <div className="bg-magenta/5 border-l-4 border-magenta rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-magenta text-white text-xs font-bold px-2 py-1 rounded">H3</span>
            <span className="font-semibold text-navy">Transform</span>
          </div>
          <p className="text-sm text-gray-500 mb-2">Months 10-18</p>
          <p className="text-base text-gray-600 mb-2">Phases 4-5: Agentic Discovery, Orchestrated System</p>
          <div className="flex gap-2 flex-wrap">
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">$25.9K direct</span>
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">$360K labor</span>
          </div>
        </div>
      </div>

      <div className="bg-teal/10 border-l-4 border-teal p-5 rounded-r-lg mb-6">
        <h4 className="font-semibold text-teal-dark mb-2">Outcome</h4>
        <p className="text-base text-gray-700">
          The framework revealed the optimal staging sequence: defend core operations first (H1: months 0-9), then leverage that foundation to build proprietary competitive advantages (H2: months 7-12), and finally create transformative capabilities (H3: months 10-18). Overlapping horizons maintain momentum while providing natural decision points to validate performance before increasing investment.
        </p>
      </div>

      <Link
        href="/transformation/three-horizons"
        className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
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

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="bg-amber/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Approach:</span>
          <span className="ml-2 font-semibold text-amber-dark">Integrated Roadmap + ADKAR</span>
        </div>
      </div>

      <p className="text-base text-gray-700 mb-6">
        Translate strategic horizons into concrete phase-by-phase execution that integrates technical implementation with change management from design. This roadmap embeds ADKAR change management directly into phase design, user segmentation, and capability progression.
      </p>

      {/* Investment Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-navy/5 border border-gray-200 rounded-lg p-5 text-center">
          <div className="text-3xl font-bold text-navy mb-1">$163.1K</div>
          <div className="text-sm font-semibold text-gray-700">Direct Investment</div>
          <p className="text-xs text-gray-500 mt-1">$11.1K infrastructure + $152K training</p>
        </div>
        <div className="bg-navy/5 border border-gray-200 rounded-lg p-5 text-center">
          <div className="text-3xl font-bold text-navy mb-1">$1,110K</div>
          <div className="text-sm font-semibold text-gray-700">Labor Allocation</div>
          <p className="text-xs text-gray-500 mt-1">5 FTE over 18 months</p>
        </div>
      </div>

      {/* Adoption Progression */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">P1</span>
            <span className="font-semibold text-navy">Universal Access</span>
          </div>
          <p className="text-base text-gray-600">All 8,000 staff — semantic search</p>
        </div>
        <div className="bg-amber/5 border-l-4 border-amber rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-amber text-white text-xs font-bold px-2 py-1 rounded">P2</span>
            <span className="font-semibold text-navy">Task Specialists</span>
          </div>
          <p className="text-base text-gray-600">200-500 who discovered specific needs</p>
        </div>
        <div className="bg-magenta/5 border-l-4 border-magenta rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-magenta text-white text-xs font-bold px-2 py-1 rounded">P3+</span>
            <span className="font-semibold text-navy">Expert Tiers</span>
          </div>
          <p className="text-base text-gray-600">Progressive capability through organic pull</p>
        </div>
      </div>

      <div className="bg-amber/10 border-l-4 border-amber p-5 rounded-r-lg mb-6">
        <h4 className="font-semibold text-amber-dark mb-2">Outcome</h4>
        <p className="text-base text-gray-700">
          The integrated roadmap solved the change management challenge before it became one. Instead of asking &quot;how do we get people to use this?&quot;, the phased progression creates natural adoption: Phase 1 serves all 8,000 staff universally, Phase 2 targets 200-500 who discovered specific needs, continuing through expert tiers. Each phase delivers standalone value that creates pull for the next phase.
        </p>
      </div>

      <Link
        href="/transformation/roadmap"
        className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
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

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="bg-navy/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Approach:</span>
          <span className="ml-2 font-semibold text-navy">Balanced Scorecard</span>
        </div>
      </div>

      <p className="text-base text-gray-700 mb-6">
        Enable data-driven progression decisions through quarterly performance measurement across four interdependent perspectives: Learning &amp; Growth, Internal Process, User &amp; Customer, and Financial. Provides leading indicators that reveal problems at quarterly boundaries when decisions can still be made.
      </p>

      {/* Four Perspectives Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">1</span>
            <span className="font-semibold text-navy">Learning & Growth</span>
          </div>
          <p className="text-base text-gray-600">Team capability and knowledge development</p>
        </div>
        <div className="bg-amber/5 border-l-4 border-amber rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-amber text-white text-xs font-bold px-2 py-1 rounded">2</span>
            <span className="font-semibold text-navy">Internal Process</span>
          </div>
          <p className="text-base text-gray-600">Operational efficiency and system performance</p>
        </div>
        <div className="bg-magenta/5 border-l-4 border-magenta rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-magenta text-white text-xs font-bold px-2 py-1 rounded">3</span>
            <span className="font-semibold text-navy">User & Customer</span>
          </div>
          <p className="text-base text-gray-600">Adoption rates and satisfaction metrics</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">4</span>
            <span className="font-semibold text-navy">Financial</span>
          </div>
          <p className="text-base text-gray-600">ROI, cost savings, and investment efficiency</p>
        </div>
      </div>

      <div className="bg-navy/5 border-l-4 border-navy p-5 rounded-r-lg mb-6">
        <h4 className="font-semibold text-navy mb-2">Key Insight</h4>
        <p className="text-base text-gray-700">
          Quarterly measurement enables data-driven progression decisions at each horizon boundary based on leading indicators, not deferred ROI. Unlike deferred ROI models that gamble on 18-48 month outcomes, this enables empirical validation every 90 days.
        </p>
      </div>

      <Link
        href="/transformation/balanced-scorecard"
        className="inline-flex items-center px-6 py-3 bg-teal hover:bg-teal-dark text-white font-semibold rounded-lg transition-colors"
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
