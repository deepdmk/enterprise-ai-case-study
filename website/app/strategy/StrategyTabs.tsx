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

      <p className="text-lg text-gray-700 mb-6">
        Before evaluating strategic approaches, we analyzed stakeholder needs to
        derive Critical to Quality requirements that any solution must satisfy.
      </p>

      <div className="overflow-x-auto mb-6">
        <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-sm">
          <thead>
            <tr className="bg-navy text-white">
              <th className="border border-navy/70 p-3 text-left font-semibold">
                Stakeholder
              </th>
              <th className="border border-navy/70 p-3 text-left font-semibold">
                Core Need
              </th>
            </tr>
          </thead>
          <tbody>
            <tr className="bg-white">
              <td className="border border-gray-200 p-3 font-semibold text-navy">
                Board
              </td>
              <td className="border border-gray-200 p-3 text-gray-700">
                Quarterly visible progress + fast ROI
              </td>
            </tr>
            <tr className="bg-gray-50">
              <td className="border border-gray-200 p-3 font-semibold text-navy">
                C-Suite
              </td>
              <td className="border border-gray-200 p-3 text-gray-700">
                Exit optionality + bounded risk
              </td>
            </tr>
            <tr className="bg-white">
              <td className="border border-gray-200 p-3 font-semibold text-navy">
                Culture &amp; People
              </td>
              <td className="border border-gray-200 p-3 text-gray-700">
                Immediate local value + no mandates
              </td>
            </tr>
            <tr className="bg-gray-50">
              <td className="border border-gray-200 p-3 font-semibold text-navy">
                Customers
              </td>
              <td className="border border-gray-200 p-3 text-gray-700">
                Quality improvement + compliance + no imposed changes
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p className="text-lg text-gray-700 mb-4">
        Four CTQ categories emerged: Cultural, Financial, Competitive, and
        Operational constraints that traditional AI approaches could not satisfy
        simultaneously.
      </p>

      <Link
        href="/strategy/stakeholder-ctq"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors text-lg"
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

      <p className="text-gray-700 mb-2">
        <strong>Key Finding:</strong> Decentralized culture structured for
        relationship-building makes top-down mandates organizationally impossible
      </p>

      <p className="text-gray-700 mb-4">
        <strong>Approach:</strong> McKinsey 7S + SWOT organizational assessment
      </p>

      <div className="mb-4">
        <p className="text-lg text-gray-700 font-semibold mb-2">
          Constraints Identified (O1-O7):
        </p>
        <ul className="list-disc pl-6 text-lg text-gray-700 space-y-1">
          <li>
            <strong>O1:</strong> Total investment &lt;$1M (severe budget
            constraints)
          </li>
          <li>
            <strong>O2:</strong> Decentralized self-initiated adoption (mandates
            organizationally impossible)
          </li>
          <li>
            <strong>O3:</strong> Quick value with zero training prerequisites
            (change-fatigued workforce)
          </li>
          <li>
            <strong>O4:</strong> Four-language support from day one (90%
            non-English workforce)
          </li>
          <li>
            <strong>O5:</strong> Leverage peer networks and mission framing
            (relational culture)
          </li>
          <li>
            <strong>O6:</strong> Passive knowledge capture (experts won&apos;t
            document, disruption creates resistance)
          </li>
          <li>
            <strong>O7:</strong> Respect strongly aligned cultural elements
            (Style-Staff-Structure-Values cannot change on transformation
            timeline)
          </li>
        </ul>
      </div>

      <div className="bg-navy/5 border-l-4 border-navy p-5 rounded mb-4">
        <p className="text-lg text-gray-700">
          <strong>Strategic Implication:</strong> The strongly aligned
          Style-Staff-Structure-Values elements create an organizational system
          optimized for decentralized relationship-building, not centralized
          efficiency. Top-down mandates violate both structure (decentralized
          authority) and culture (consensus-driven,
          relationship-centric). The 18-month transformation timeline makes
          organizational change impossible. Must design solution that works
          with this reality rather than requiring its transformation. Failed past
          initiatives created change fatigue and trust deficit that only value
          demonstration can overcome.
        </p>
      </div>

      <Link
        href="/strategy/mckinsey-7s"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors text-lg"
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

      <p className="text-lg text-gray-700 mb-2">
        <strong>Key Finding:</strong> Institutional knowledge provides strong,
        defensible competitive position for established player in commoditizing
        AI market
      </p>

      <p className="text-lg text-gray-700 mb-4">
        <strong>Approach:</strong> 5 Forces competitive analysis
      </p>

      <div className="mb-4">
        <p className="text-lg text-gray-700 font-semibold mb-2">
          Requirements Extracted (C1-C4):
        </p>
        <ul className="list-disc pl-6 text-lg text-gray-700 space-y-1">
          <li>
            <strong>C1:</strong> Proprietary capabilities (non-commoditizable)
          </li>
          <li>
            <strong>C2:</strong> Dramatic efficiency gains (outperform lean
            competitors)
          </li>
          <li>
            <strong>C3:</strong> Defensible differentiation (non-substitutable)
          </li>
          <li>
            <strong>C4:</strong> Build with existing staff (not external AI
            talent)
          </li>
        </ul>
      </div>

      <div className="bg-navy/5 border-l-4 border-navy p-5 rounded mb-4">
        <p className="text-lg text-gray-700">
          <strong>Strategic Implication:</strong> The organization cannot compete
          on speed or cost against new market entrants. Commercial AI platforms
          commoditize capabilities that competitors can equally access,
          destroying a key advantage: institutional knowledge. Vendor platforms would convert strategic asset into
          commodity capability. The best defensible position requires building
          proprietary AI internally on unique institutional knowledge that
          competitors cannot purchase or replicate. This is competitive survival.
        </p>
      </div>

      <Link
        href="/porters-five-forces"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors text-lg"
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

      <p className="text-gray-700 mb-4">
        Three strategic alternatives were developed from the CTQ requirements
        and evaluated against the full set of 19 stakeholder, competitive, and
        organizational constraints.
      </p>

      <div className="mb-4">
        <p className="text-lg text-gray-700 font-semibold mb-2">
          Alternatives Evaluated:
        </p>
        <ul className="list-disc pl-6 text-lg text-gray-700 space-y-2">
          <li>
            <strong>Vendor Platform:</strong> Purchase commercial AI platform
            (e.g., Microsoft Copilot, Salesforce Einstein) and configure for
            organizational needs
          </li>
          <li>
            <strong>Custom Big Bang:</strong> Build custom AI system from scratch
            with full-scope deployment across the organization simultaneously
          </li>
          <li>
            <strong>Phased Internal Build:</strong> Build proprietary AI
            internally with existing staff, deploy progressively with
            self-initiated adoption
          </li>
        </ul>
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

      <p className="text-gray-700 mb-2">
        <strong>Key Finding:</strong> Phased Internal Build scored +38;
        alternatives failed with -29 and -23
      </p>

      <p className="text-gray-700 mb-4">
        <strong>Approach:</strong> Pugh Matrix evaluation against 19 CTQs (8
        stakeholder + 4 competitive + 7 organizational)
      </p>

      <div className="mb-4">
        <p className="text-lg text-gray-700 font-semibold mb-2">Results:</p>
        <ul className="list-disc pl-6 text-lg text-gray-700 space-y-2">
          <li>
            <strong>Vendor Platform:</strong> -29 (REJECTED) - Violates 6 of 8
            stakeholder requirements, commoditizes competitive advantage, exceeds
            budget 20-50x
          </li>
          <li>
            <strong>Custom Big Bang:</strong> -23 (REJECTED) - Violates 6 of 8
            stakeholder requirements, requires $1.5-3.75M for inaccessible AI
            talent, culturally impossible
          </li>
          <li>
            <strong>Phased Internal Build:</strong> +38 (SELECTED) - Only option
            satisfying all stakeholder requirements while passing competitive and
            organizational validation
          </li>
        </ul>
      </div>

      <div className="bg-teal/5 border-l-4 border-teal p-5 rounded mb-4">
        <p className="text-lg text-gray-700">
          <strong>Strategic Implication:</strong> Phased Internal Build was the viable option given the constraints. Both alternatives
          failed stakeholder requirements fundamentally: vendor platforms destroy
          competitive advantage through commoditization, custom big bang requires
          organizational capabilities (centralized coordination, mandate
          authority, AI talent access) that don&apos;t exist and cannot be
          created on transformation timeline.
        </p>
      </div>

      <Link
        href="/strategy/pugh-matrix"
        className="inline-flex items-center px-6 py-3 bg-teal-dark hover:bg-navy text-white font-semibold rounded-lg transition-colors text-lg"
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

      <p className="text-gray-700 mb-6">
        <strong>Phased Internal Build</strong> is the strategic approach: build
        proprietary AI internally with existing staff, deploy progressively with
        self-initiated adoption. The transformation builds through progressive
        capability stages, where each phase delivers immediate ROI and creates
        standalone value. The phased approach enables stopping at any point with
        a functioning AI capability that has positive ROI, rather than requiring
        all-or-nothing investment.
      </p>

      <div className="bg-teal/5 border-l-4 border-teal p-5 rounded mb-6">
        <p className="text-lg text-gray-700 font-semibold mb-2">
          Core Investment:
        </p>
        <ul className="list-disc pl-6 text-lg text-gray-700 space-y-1">
          <li>
            <strong>Direct Investment:</strong> $163.1K ($11.1K infrastructure +
            $152K training programs)
          </li>
          <li>
            <strong>Estimated Labor Allocation:</strong> $1,110K (5 FTE over 18
            months)
          </li>
          <li>
            <strong>Cost Reduction:</strong> 92-98% vs $2-7M traditional
            alternatives
          </li>
        </ul>
      </div>

      <p className="text-lg text-gray-700 font-semibold mb-3">
        Strategic Outcomes Achieved:
      </p>

      <div className="space-y-3">
        <p className="text-lg text-gray-700">
          <strong>Competitive Advantage:</strong> Proprietary AI built on
          institutional knowledge competitors cannot purchase or replicate
        </p>
        <p className="text-lg text-gray-700">
          <strong>Financial Performance:</strong> $163.1K Direct Investment vs
          $2-7M alternatives (92-98% reduction), quarterly value from Month 1
        </p>
        <p className="text-lg text-gray-700">
          <strong>Organizational Success:</strong> Self-initiated adoption in
          change-fatigued, decentralized organization across 4 languages
        </p>
        <p className="text-lg text-gray-700">
          <strong>Risk Management:</strong> Progressive investment with decision
          points at horizon boundaries vs. all-or-nothing $2-7M bets
        </p>
        <p className="text-lg text-gray-700">
          <strong>Strategic Optionality:</strong> Guaranteed AI transformation
          while preserving optionality for workflow and organizational changes
        </p>
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
