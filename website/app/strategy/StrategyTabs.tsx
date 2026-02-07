"use client";

import Link from "next/link";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui";

/* ───────────────────── Section 1: Strategic Analysis ───────────────────── */

function StakeholderAnalysis() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Stakeholder CTQ Analysis
      </h3>

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="bg-navy/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Approach:</span>
          <span className="ml-2 font-semibold text-navy">One-on-one interviews and focus groups</span>
        </div>
      </div>

      <p className="text-base text-gray-700 mb-6">
        Before evaluating strategic approaches, we analyzed stakeholder needs to derive Critical to Quality requirements that any solution must satisfy. Interviews and focus groups with Board members, C-Suite executives, staff representatives, and customer-facing teams revealed eight distinct requirements spanning financial expectations, risk tolerance, adoption preferences, and service quality standards.
      </p>

      {/* Stakeholder CTQ Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S1</span>
            <span className="font-semibold text-navy">Board: Visible Progress</span>
          </div>
          <p className="text-base text-gray-600">Quarterly visible progress demonstrating momentum</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S2</span>
            <span className="font-semibold text-navy">Board: Fast ROI</span>
          </div>
          <p className="text-base text-gray-600">Rapid return on investment, not deferred payback</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S3</span>
            <span className="font-semibold text-navy">C-Suite: Exit Optionality</span>
          </div>
          <p className="text-base text-gray-600">Ability to stop at any point without sunk cost</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S4</span>
            <span className="font-semibold text-navy">C-Suite: Bounded Risk</span>
          </div>
          <p className="text-base text-gray-600">Limited exposure at any decision point</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S5</span>
            <span className="font-semibold text-navy">Staff: Immediate Value</span>
          </div>
          <p className="text-base text-gray-600">Quick wins that solve real problems from day one</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S6</span>
            <span className="font-semibold text-navy">Staff: No Mandates</span>
          </div>
          <p className="text-base text-gray-600">Self-initiated adoption, not top-down requirements</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S7</span>
            <span className="font-semibold text-navy">Customer: Quality</span>
          </div>
          <p className="text-base text-gray-600">Improved service quality and compliance</p>
        </div>
        <div className="bg-navy/5 border-l-4 border-navy rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-navy text-white text-xs font-bold px-2 py-1 rounded">S8</span>
            <span className="font-semibold text-navy">Customer: No Disruption</span>
          </div>
          <p className="text-base text-gray-600">No imposed changes to existing relationships</p>
        </div>
      </div>

      <p className="text-base text-gray-700 mb-4">
        Four CTQ categories emerged: Cultural, Financial, Competitive, and
        Operational constraints that traditional AI approaches could not satisfy
        simultaneously.
      </p>

      <Link
        href="/strategy/stakeholder-ctq"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors"
      >
        View Full Analysis &rarr;
      </Link>
    </div>
  );
}

function OrganizationalAnalysis() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Understanding Organizational Reality
      </h3>

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="bg-teal/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Approach:</span>
          <span className="ml-2 font-semibold text-teal-dark">McKinsey 7S + SWOT</span>
        </div>
      </div>

      <p className="text-base text-gray-700 mb-6">
        Using McKinsey 7S framework combined with SWOT analysis, we mapped the organizational reality that any AI transformation must navigate. The analysis revealed a decentralized culture structured for relationship-building where top-down mandates are organizationally impossible. Seven constraints emerged spanning budget, adoption model, change fatigue, language requirements, and cultural alignment.
      </p>

      {/* Constraints Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">O1</span>
            <span className="font-semibold text-navy">Budget Constraint</span>
          </div>
          <p className="text-base text-gray-600">Total investment &lt;$1M</p>
        </div>
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">O2</span>
            <span className="font-semibold text-navy">Adoption Model</span>
          </div>
          <p className="text-base text-gray-600">Decentralized self-initiated adoption required</p>
        </div>
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">O3</span>
            <span className="font-semibold text-navy">Change Fatigue</span>
          </div>
          <p className="text-base text-gray-600">Quick value with zero training prerequisites</p>
        </div>
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">O4</span>
            <span className="font-semibold text-navy">Language Support</span>
          </div>
          <p className="text-base text-gray-600">Four languages from day one (90% non-English)</p>
        </div>
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">O5</span>
            <span className="font-semibold text-navy">Relational Culture</span>
          </div>
          <p className="text-base text-gray-600">Leverage peer networks and mission framing</p>
        </div>
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">O6</span>
            <span className="font-semibold text-navy">Knowledge Capture</span>
          </div>
          <p className="text-base text-gray-600">Passive capture only — experts won&apos;t document</p>
        </div>
        <div className="bg-teal/5 border-l-4 border-teal rounded-r-lg p-4 md:col-span-2">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-teal text-white text-xs font-bold px-2 py-1 rounded">O7</span>
            <span className="font-semibold text-navy">Cultural Alignment</span>
          </div>
          <p className="text-base text-gray-600">Style-Staff-Structure-Values cannot change on transformation timeline</p>
        </div>
      </div>

      <div className="bg-amber/10 border-l-4 border-amber p-5 rounded-r-lg mb-6">
        <h4 className="font-semibold text-amber-dark mb-2">Strategic Implication</h4>
        <p className="text-base text-gray-700">
          The strongly aligned Style-Staff-Structure-Values elements create an organizational system
          optimized for decentralized relationship-building, not centralized efficiency. Top-down mandates
          violate both structure (decentralized authority) and culture (consensus-driven, relationship-centric).
          The 18-month transformation timeline makes organizational change impossible. Must design solution
          that works with this reality rather than requiring its transformation. Failed past initiatives
          created change fatigue and trust deficit that only value demonstration can overcome.
        </p>
      </div>

      <Link
        href="/strategy/mckinsey-7s"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors"
      >
        View detailed 7S + SWOT analysis &rarr;
      </Link>
    </div>
  );
}

function CompetitiveAnalysis() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Understanding Competitive Imperatives
      </h3>

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="bg-magenta/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Approach:</span>
          <span className="ml-2 font-semibold text-magenta">Porter&apos;s 5 Forces</span>
        </div>
      </div>

      <p className="text-base text-gray-700 mb-6">
        Porter&apos;s Five Forces analysis examined the competitive landscape to identify what AI capabilities the organization must develop to maintain market position. The analysis revealed that institutional knowledge — accumulated over decades of operations — provides a strong, defensible competitive position that commercial AI platforms would commoditize. Four competitive imperatives emerged that any solution must address.
      </p>

      {/* Competitive Requirements Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        <div className="bg-magenta/5 border-l-4 border-magenta rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-magenta text-white text-xs font-bold px-2 py-1 rounded">C1</span>
            <span className="font-semibold text-navy">Proprietary Capabilities</span>
          </div>
          <p className="text-base text-gray-600">Non-commoditizable AI that competitors cannot purchase</p>
        </div>
        <div className="bg-magenta/5 border-l-4 border-magenta rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-magenta text-white text-xs font-bold px-2 py-1 rounded">C2</span>
            <span className="font-semibold text-navy">Efficiency Gains</span>
          </div>
          <p className="text-base text-gray-600">Dramatic improvements to outperform lean competitors</p>
        </div>
        <div className="bg-magenta/5 border-l-4 border-magenta rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-magenta text-white text-xs font-bold px-2 py-1 rounded">C3</span>
            <span className="font-semibold text-navy">Defensible Differentiation</span>
          </div>
          <p className="text-base text-gray-600">Non-substitutable capabilities based on unique knowledge</p>
        </div>
        <div className="bg-magenta/5 border-l-4 border-magenta rounded-r-lg p-4">
          <div className="flex items-center gap-2 mb-1">
            <span className="bg-magenta text-white text-xs font-bold px-2 py-1 rounded">C4</span>
            <span className="font-semibold text-navy">Existing Staff</span>
          </div>
          <p className="text-base text-gray-600">Build with current team, not external AI talent</p>
        </div>
      </div>

      <div className="bg-amber/10 border-l-4 border-amber p-5 rounded-r-lg mb-6">
        <h4 className="font-semibold text-amber-dark mb-2">Strategic Implication</h4>
        <p className="text-base text-gray-700">
          The organization cannot compete on speed or cost against new market entrants. Commercial AI platforms
          commoditize capabilities that competitors can equally access, destroying a key advantage: institutional
          knowledge. Vendor platforms would convert strategic asset into commodity capability. The best defensible
          position requires building proprietary AI internally on unique institutional knowledge that competitors
          cannot purchase or replicate. This is competitive survival.
        </p>
      </div>

      <Link
        href="/porters-five-forces"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors"
      >
        View detailed 5 Forces analysis &rarr;
      </Link>
    </div>
  );
}

/* ───────────────────── Section 2: Strategy Development ───────────────────── */

function OptionsDevelopment() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Evaluating Solution Options
      </h3>

      <p className="text-base text-gray-700 mb-6">
        With 19 CTQs established across stakeholder, organizational, and competitive dimensions, we developed three distinct strategic alternatives representing fundamentally different approaches to enterprise AI. Each option varies in investment scale, implementation timeline, risk profile, and alignment with organizational constraints.
      </p>

      {/* Options Cards */}
      <div className="space-y-4">
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <span className="bg-gray-400 text-white text-xs font-bold px-3 py-1 rounded">Option 1</span>
            <h4 className="font-semibold text-navy text-lg">Vendor Platform</h4>
          </div>
          <p className="text-base text-gray-700">
            Purchase commercial AI platform (e.g., Microsoft Copilot, Salesforce Einstein) and configure for organizational needs.
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">$2-7M investment</span>
            <span className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">3-4 year ROI</span>
            <span className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">Vendor lock-in</span>
          </div>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <span className="bg-gray-400 text-white text-xs font-bold px-3 py-1 rounded">Option 2</span>
            <h4 className="font-semibold text-navy text-lg">Custom Big Bang</h4>
          </div>
          <p className="text-base text-gray-700">
            Build custom AI system from scratch with full-scope deployment across the organization simultaneously.
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">$1.5-3.75M</span>
            <span className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">Requires AI talent</span>
            <span className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">All-or-nothing</span>
          </div>
        </div>

        <div className="bg-teal/5 border-2 border-teal rounded-lg p-5">
          <div className="flex items-center gap-3 mb-2">
            <span className="bg-teal text-white text-xs font-bold px-3 py-1 rounded">Option 3</span>
            <h4 className="font-semibold text-navy text-lg">Phased Internal Build</h4>
          </div>
          <p className="text-base text-gray-700">
            Build proprietary AI internally with existing staff, deploy progressively with self-initiated adoption.
          </p>
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="text-xs bg-teal/20 text-teal-dark px-2 py-1 rounded">$163K investment</span>
            <span className="text-xs bg-teal/20 text-teal-dark px-2 py-1 rounded">Quarterly ROI</span>
            <span className="text-xs bg-teal/20 text-teal-dark px-2 py-1 rounded">Exit optionality</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function OptionScoring() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Option Scoring: Pugh Matrix
      </h3>

      <div className="flex flex-wrap gap-4 mb-6">
        <div className="bg-navy/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Method:</span>
          <span className="ml-2 font-semibold text-navy">Pugh Matrix</span>
        </div>
        <div className="bg-navy/10 px-4 py-2 rounded-lg">
          <span className="text-sm text-gray-600">Criteria:</span>
          <span className="ml-2 font-semibold text-navy">19 CTQs (8 + 7 + 4)</span>
        </div>
      </div>

      {/* Scoring Results Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-5 text-center">
          <div className="text-4xl font-bold text-red-600 mb-2">-29</div>
          <div className="font-semibold text-gray-800 mb-2">Vendor Platform</div>
          <span className="inline-block bg-red-100 text-red-700 text-xs font-semibold px-3 py-1 rounded-full">REJECTED</span>
          <p className="text-sm text-gray-600 mt-3">Violates 6 of 8 stakeholder requirements, exceeds budget 20-50x</p>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-5 text-center">
          <div className="text-4xl font-bold text-red-600 mb-2">-23</div>
          <div className="font-semibold text-gray-800 mb-2">Custom Big Bang</div>
          <span className="inline-block bg-red-100 text-red-700 text-xs font-semibold px-3 py-1 rounded-full">REJECTED</span>
          <p className="text-sm text-gray-600 mt-3">Requires $1.5-3.75M and inaccessible AI talent</p>
        </div>
        <div className="bg-teal/10 border-2 border-teal rounded-lg p-5 text-center">
          <div className="text-4xl font-bold text-teal mb-2">+38</div>
          <div className="font-semibold text-gray-800 mb-2">Phased Internal Build</div>
          <span className="inline-block bg-teal/20 text-teal-dark text-xs font-semibold px-3 py-1 rounded-full">SELECTED</span>
          <p className="text-sm text-gray-600 mt-3">Satisfies all 19 CTQs with bounded risk</p>
        </div>
      </div>

      <div className="bg-teal/10 border-l-4 border-teal p-5 rounded-r-lg mb-6">
        <h4 className="font-semibold text-teal-dark mb-2">Strategic Implication</h4>
        <p className="text-base text-gray-700">
          Phased Internal Build was the only viable option given the constraints. Both alternatives
          failed stakeholder requirements fundamentally: vendor platforms destroy competitive advantage
          through commoditization, custom big bang requires organizational capabilities that don&apos;t
          exist and cannot be created on the transformation timeline.
        </p>
      </div>

      <Link
        href="/strategy/pugh-matrix"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors"
      >
        View detailed Pugh Matrix analysis &rarr;
      </Link>
    </div>
  );
}

function SelectedStrategy() {
  return (
    <div>
      <h3 className="text-2xl font-bold text-navy mb-4">
        Solution Strategy Selected: Phased Internal Build
      </h3>

      <p className="text-base text-gray-700 mb-6">
        <strong>Phased Internal Build</strong> is the strategic approach: build proprietary AI internally
        with existing staff, deploy progressively with self-initiated adoption. The transformation builds
        through progressive capability stages, where each phase delivers immediate ROI and creates standalone
        value. The phased approach enables stopping at any point with a functioning AI capability that has
        positive ROI, rather than requiring all-or-nothing investment.
      </p>

      {/* Investment Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
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
        <div className="bg-teal/10 border-2 border-teal rounded-lg p-5 text-center">
          <div className="text-3xl font-bold text-teal mb-1">92-98%</div>
          <div className="text-sm font-semibold text-gray-700">Cost Reduction</div>
          <p className="text-xs text-gray-500 mt-1">vs $2-7M alternatives</p>
        </div>
      </div>

      {/* Strategic Outcomes */}
      <h4 className="text-lg font-semibold text-navy mb-4">Strategic Outcomes Achieved</h4>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white border border-gray-200 border-t-4 border-t-navy rounded-lg p-4">
          <h5 className="font-semibold text-navy mb-2">Competitive Advantage</h5>
          <p className="text-base text-gray-600">Proprietary AI built on institutional knowledge competitors cannot purchase or replicate</p>
        </div>
        <div className="bg-white border border-gray-200 border-t-4 border-t-teal rounded-lg p-4">
          <h5 className="font-semibold text-navy mb-2">Financial Performance</h5>
          <p className="text-base text-gray-600">$163.1K Direct Investment vs $2-7M alternatives, quarterly value from Month 1</p>
        </div>
        <div className="bg-white border border-gray-200 border-t-4 border-t-amber rounded-lg p-4">
          <h5 className="font-semibold text-navy mb-2">Organizational Success</h5>
          <p className="text-base text-gray-600">Self-initiated adoption in change-fatigued, decentralized organization across 4 languages</p>
        </div>
        <div className="bg-white border border-gray-200 border-t-4 border-t-magenta rounded-lg p-4">
          <h5 className="font-semibold text-navy mb-2">Risk Management</h5>
          <p className="text-base text-gray-600">Progressive investment with decision points vs. all-or-nothing $2-7M bets</p>
        </div>
      </div>
    </div>
  );
}

/* ───────────────────── Exported Tabbed Sections ───────────────────── */

export function StrategicAnalysisTabs() {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
      <Tabs defaultValue="stakeholder">
        <TabsList className="p-1 m-4 rounded-lg flex gap-2" style={{ backgroundColor: 'rgba(30, 58, 95, 0.1)' }}>
          <TabsTrigger
            value="stakeholder"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy hover:bg-navy/10"
          >
            Stakeholder Analysis
          </TabsTrigger>
          <TabsTrigger
            value="organizational"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy hover:bg-navy/10"
          >
            Organizational Analysis
          </TabsTrigger>
          <TabsTrigger
            value="competitive"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy hover:bg-navy/10"
          >
            Competitive Analysis
          </TabsTrigger>
        </TabsList>

        <div className="px-4 pb-4">
          <TabsContent value="stakeholder">
            <StakeholderAnalysis />
          </TabsContent>
          <TabsContent value="organizational">
            <OrganizationalAnalysis />
          </TabsContent>
          <TabsContent value="competitive">
            <CompetitiveAnalysis />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}

export function StrategyDevelopmentTabs() {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
      <Tabs defaultValue="options">
        <TabsList className="p-1 m-4 rounded-lg flex gap-2" style={{ backgroundColor: 'rgba(26, 188, 156, 0.1)' }}>
          <TabsTrigger
            value="options"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal-dark data-[state=active]:text-white data-[state=active]:shadow-sm text-teal-on-light hover:bg-teal/10"
          >
            Options Development
          </TabsTrigger>
          <TabsTrigger
            value="scoring"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal-dark data-[state=active]:text-white data-[state=active]:shadow-sm text-teal-on-light hover:bg-teal/10"
          >
            Option Scoring
          </TabsTrigger>
          <TabsTrigger
            value="selected"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal-dark data-[state=active]:text-white data-[state=active]:shadow-sm text-teal-on-light hover:bg-teal/10"
          >
            Selected Strategy
          </TabsTrigger>
        </TabsList>

        <div className="px-4 pb-4">
          <TabsContent value="options">
            <OptionsDevelopment />
          </TabsContent>
          <TabsContent value="scoring">
            <OptionScoring />
          </TabsContent>
          <TabsContent value="selected">
            <SelectedStrategy />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
