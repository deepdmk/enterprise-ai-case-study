import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { PughMatrixVisual } from "./PughMatrixVisual";

export const metadata: Metadata = {
  title: "Pugh Matrix Decision Framework - Solution Selection Through CTQ-Driven Analysis",
  description:
    "Pugh Matrix evaluation of three alternative solutions against Critical-To-Quality requirements extracted from stakeholder voice, competitive analysis, and organizational assessment.",
};

export default function PughMatrixPage() {
  return (
    <>
      <PageHeader
        title="Pugh Matrix Decision Framework"
        subtitle="Solution Selection Through CTQ-Driven Analysis"
      />

      {/* Breadcrumb */}
      <section className="bg-white border-b border-gray-200">
        <Container size="reading">
          <nav
            className="py-4 text-sm text-gray-600"
            aria-label="Breadcrumb"
          >
            <Link
              href="/strategy"
              className="hover:text-teal focus:outline-none focus:ring-2 focus:ring-teal"
            >
              Strategy
            </Link>
            <span className="mx-2">&rarr;</span>
            <span className="text-gray-900">Pugh Matrix</span>
          </nav>
        </Container>
      </section>

      {/* Introduction */}
      <section className="bg-gray-50 py-12">
        <Container size="reading">
          <h2 className="text-2xl font-bold text-navy mb-4">
            Section 3: Strategic Design - From Requirements to Solution
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed">
            After competitive analysis (Porter&apos;s Five Forces) and
            organizational assessment (McKinsey 7S with SWOT), the challenge was
            to design a strategy that satisfies BOTH competitive requirements AND
            organizational constraints simultaneously.
          </p>
          <p className="text-gray-700 leading-relaxed mt-4">
            This section shows how we extracted Critical-To-Quality (CTQ)
            requirements and used them to evaluate alternative solutions through
            a Pugh Matrix analysis.
          </p>
        </Container>
      </section>

      {/* Interactive Pugh Matrix Component */}
      <section className="py-16">
        <Container size="content">
          <PughMatrixVisual />
        </Container>
      </section>

      {/* CTQ Requirements Framework */}
      <section className="py-16 bg-gray-50">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            CTQ Requirements Framework
          </h2>

          {/* Primary CTQs: Stakeholder Requirements */}
          <div className="mb-12">
            <h3 className="text-xl md:text-2xl font-bold text-navy mb-4">
              Primary CTQs: Direct Stakeholder Requirements (S1-S8)
            </h3>
            <p className="text-gray-700 leading-relaxed mb-6">
              Stakeholders explicitly articulated their requirements through the
              Challenge page. These are non-negotiable constraints that any
              solution MUST satisfy:
            </p>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-sm">
                <thead>
                  <tr className="bg-navy text-white">
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      CTQ ID
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      Critical-To-Quality Requirement
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      Source (Challenge Page)
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      Stakeholder Group
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S1
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Quarterly results + 5-year strategic optionality
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Organizational Dilemma
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Board (quarterly) + C-Suite (5-year); cannot sacrifice
                      either
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S2
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Decisive investment + exit ability at any phase
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Organizational Dilemma
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      CFO (budget commitment) + Board (risk management)
                    </td>
                  </tr>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S3
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Enterprise-wide intelligence + decentralized culture
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Organizational Dilemma
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      C-Suite (unified capabilities) + Country Directors
                      (autonomy)
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S4
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Incremental delivery (value at every phase)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Key Requirements
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      All stakeholders: change-fatigued, need proof before
                      continued investment
                    </td>
                  </tr>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S5
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Bounded risk (stop any phase, keep value)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Key Requirements
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      CFO + Board: failed transformation precedent, protect
                      investment
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S6
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Bottom-up adoption (teams discover value)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Key Requirements
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Country Directors + Staff: top-down mandates fail in this
                      culture
                    </td>
                  </tr>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S7
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Customer choice (improved capability, no forced change)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Key Requirements
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Client-facing staff: preserve relationships, avoid workflow
                      disruption
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      S8
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      No vendor dependency (platform agnostic)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Key Requirements
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      CTO + C-Suite: avoid lock-in, preserve competitive
                      flexibility
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="mt-6 bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
              <p className="text-gray-700">
                <strong>Critical Note:</strong> These are what stakeholders said
                they need. Analyses validate WHY these requirements are critical
                and HOW to achieve them, but they don&apos;t replace stakeholder
                voice.
              </p>
            </div>
          </div>

          {/* Supporting CTQs: Analysis-Derived Requirements */}
          <div className="mb-8">
            <h3 className="text-xl md:text-2xl font-bold text-navy mb-4">
              Supporting CTQs: Analysis-Derived Requirements
            </h3>
            <p className="text-gray-700 leading-relaxed mb-6">
              Competitive and organizational analyses explain WHY stakeholder
              requirements are critical and identify ADDITIONAL requirements
              needed for success:
            </p>
          </div>

          {/* Competitive CTQs */}
          <div className="mb-12">
            <h4 className="text-lg md:text-xl font-bold text-navy mb-4">
              Competitive CTQs (from Porter&apos;s Five Forces) - C1-C4
            </h4>
            <p className="text-gray-700 leading-relaxed mb-6">
              These requirements validate why stakeholder demands for internal
              build (S8), quick value (S4), and strategic optionality (S1) are
              competitively necessary:
            </p>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-sm">
                <thead>
                  <tr className="bg-navy text-white">
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      CTQ ID
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      Critical-To-Quality Requirement
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      Source Analysis
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      How It Supports Stakeholder CTQs
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      C1
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Proprietary capabilities (non-commoditizable)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Porter&apos;s: Threat of Substitutes
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S8 (no vendor dependency): vendor platforms
                      commoditize the one defensible advantage
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      C2
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Dramatic efficiency gains (outperform lean competitors)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Porter&apos;s: Competitive Rivalry
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S1 (strategic optionality): must extract more
                      value from knowledge scale advantage
                    </td>
                  </tr>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      C3
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Defensible differentiation (non-substitutable)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Porter&apos;s: Threat of New Entrants
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S8: need advantages competitors cannot purchase
                      or replicate
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      C4
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Build with existing staff (not external AI talent)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Porter&apos;s: Supplier Power
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S5 (bounded risk): cannot risk $1.5-3.75M on
                      inaccessible AI talent market
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="mt-6 bg-teal/5 border-l-4 border-teal p-4 rounded">
              <p className="text-gray-700">
                <strong>Analysis Insight:</strong> Porter&apos;s Five Forces
                validates stakeholder requirement S8 (no vendor dependency) as
                competitively necessary, not just a preference. Vendor platforms
                would commoditize the only defensible competitive advantage.
              </p>
            </div>
          </div>

          {/* Organizational CTQs */}
          <div className="mb-12">
            <h4 className="text-lg md:text-xl font-bold text-navy mb-4">
              Organizational CTQs (from McKinsey 7S + SWOT) - O1-O7
            </h4>
            <p className="text-gray-700 leading-relaxed mb-6">
              These requirements validate why stakeholder demands for
              decentralized adoption (S6), cultural fit (S3), and bounded
              investment (S2, S5) are organizationally necessary:
            </p>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-sm">
                <thead>
                  <tr className="bg-navy text-white">
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      CTQ ID
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      Critical-To-Quality Requirement
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      Source Analysis
                    </th>
                    <th className="border border-navy/70 p-3 text-left font-semibold">
                      How It Supports Stakeholder CTQs
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      O1
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Total investment &lt;$1M
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      7S: Strategy (SWOT Weakness)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S2, S5 (decisive investment + bounded risk):
                      severe budget constraints are absolute
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      O2
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Decentralized self-initiated adoption (no mandates)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      7S: Structure, Style, Shared Values
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S3, S6 (enterprise intelligence + decentralized
                      culture, bottom-up adoption): mandates organizationally
                      impossible
                    </td>
                  </tr>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      O3
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Quick value with zero training prerequisites
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      7S: Staff, Systems
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S4 (incremental delivery): change-fatigued
                      workforce cannot absorb training burden before seeing value
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      O4
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Four-language support from day one
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      7S: Staff
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Additional requirement: 90% non-native English speakers;
                      English-only excludes majority and violates S6 (bottom-up
                      adoption)
                    </td>
                  </tr>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      O5
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Leverage peer networks and mission framing
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      7S: Style, Shared Values
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S6 (bottom-up adoption): peer validation more
                      powerful than headquarters directives in this culture
                    </td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      O6
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Passive knowledge capture (no expert disruption)
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      7S: Skills, Staff
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S7 (customer choice): experts won&apos;t
                      document; disruption creates resistance and client risk
                    </td>
                  </tr>
                  <tr className="bg-white">
                    <td className="border border-gray-200 p-3 font-semibold text-navy">
                      O7
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Respect strongly aligned cultural elements
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      7S: All elements
                    </td>
                    <td className="border border-gray-200 p-3 text-gray-700">
                      Validates S3 (enterprise + decentralized): cannot change
                      Style-Staff-Structure-Values alignment on transformation
                      timeline
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="mt-6 bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
              <p className="text-gray-700">
                <strong>Analysis Insight:</strong> McKinsey 7S validates that
                stakeholder requirements S3 (enterprise intelligence +
                decentralized culture) and S6 (bottom-up adoption) aren&apos;t
                preferences - they&apos;re organizational constraints. Mandates
                are impossible in this structure and culture.
              </p>
            </div>
          </div>

          {/* CTQ Hierarchy */}
          <div className="mb-8">
            <h3 className="text-xl md:text-2xl font-bold text-navy mb-4">
              CTQ Hierarchy: Primary vs. Supporting
            </h3>

            <div className="space-y-4">
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <p className="text-gray-700">
                  <strong>Primary CTQs (S1-S8):</strong> Direct stakeholder
                  requirements. Solutions that don&apos;t satisfy these fail
                  stakeholder acceptance regardless of analytical merit.
                </p>
              </div>

              <div className="bg-gray-50 border-l-4 border-gray-400 p-4 rounded">
                <p className="text-gray-700 mb-2">
                  <strong>Supporting CTQs (C1-C4, O1-O7):</strong>{" "}
                  Analysis-derived requirements that:
                </p>
                <ol className="list-decimal list-inside text-gray-700 space-y-1 ml-4">
                  <li>
                    Explain WHY primary CTQs are necessary (not just preferences)
                  </li>
                  <li>
                    Identify ADDITIONAL requirements for
                    competitive/organizational success
                  </li>
                  <li>Provide measurable validation criteria</li>
                </ol>
              </div>

              <div className="bg-amber/5 border-l-4 border-amber p-4 rounded">
                <p className="text-gray-700">
                  <strong>Critical Insight:</strong> Analyses validate
                  stakeholder requirements and add depth, but stakeholder voice
                  is primary. If stakeholders want something not reflected in
                  analysis, we validate it through analysis or acknowledge it as
                  a constraint to work within.
                </p>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* Alternative Solutions Evaluated */}
      <section className="py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Alternative Solutions Evaluated
          </h2>

          <div className="space-y-6">
            <Card className="border-l-4 border-l-red-500">
              <h3 className="text-xl font-bold text-navy mb-3">
                Alternative 1: Vendor Platform Approach
              </h3>
              <p className="text-gray-700 mb-4">
                Purchase enterprise AI platform from major vendor (e.g.,
                Salesforce Einstein, Microsoft Copilot, ServiceNow AI)
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-base text-gray-700">
                <div>
                  <strong>Investment:</strong> $2-5M upfront + ongoing licensing
                </div>
                <div>
                  <strong>Timeline:</strong> 3-4 years to ROI
                </div>
                <div>
                  <strong>Deployment:</strong> Centralized rollout, standardized
                  training, English-only initially
                </div>
                <div>
                  <strong>Knowledge:</strong> Standardized &quot;best
                  practices&quot; not organizational-specific
                </div>
              </div>
            </Card>

            <Card className="border-l-4 border-l-orange-500">
              <h3 className="text-xl font-bold text-navy mb-3">
                Alternative 2: Custom Big Bang Build
              </h3>
              <p className="text-gray-700 mb-4">
                Build custom AI solution with external consultants, deploy
                enterprise-wide simultaneously
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-base text-gray-700">
                <div>
                  <strong>Investment:</strong> $1.5-3M for development +
                  $1.5-3.75M for AI specialist recruitment
                </div>
                <div>
                  <strong>Timeline:</strong> 18-24 months development, 6-12
                  months deployment
                </div>
                <div>
                  <strong>Deployment:</strong> Coordinated enterprise-wide
                  rollout with mandatory adoption
                </div>
                <div>
                  <strong>Knowledge:</strong> Custom-built on organizational data
                </div>
              </div>
            </Card>

            <Card className="border-l-4 border-l-green-500">
              <h3 className="text-xl font-bold text-navy mb-3">
                Alternative 3: Phased Internal Build (Our Approach)
              </h3>
              <p className="text-gray-700 mb-4">
                Build proprietary AI internally with existing staff, deploy in
                progressive phases with self-initiated adoption
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-base text-gray-700">
                <div>
                  <strong>Investment:</strong> $163.1K Direct Investment ($11,100 infrastructure) progressive across 4
                  phases (&lt;$6K per phase)
                </div>
                <div>
                  <strong>Timeline:</strong> Quarterly value delivery from Phase
                  1 onward
                </div>
                <div>
                  <strong>Deployment:</strong> Decentralized self-initiated adoption,
                  country-by-country pace
                </div>
                <div>
                  <strong>Knowledge:</strong> Proprietary AI built on unique
                  115-country institutional knowledge
                </div>
              </div>
            </Card>
          </div>
        </Container>
      </section>

      {/* Why Phased Internal Build Was Selected */}
      <section className="py-16 bg-gray-50">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Why Phased Internal Build Was Selected
          </h2>

          <h3 className="text-xl font-bold text-navy mb-4">
            The Only Viable Solution
          </h3>
          <p className="text-gray-700 leading-relaxed mb-8">
            The Pugh Matrix evaluation revealed that Phased Internal Build was
            not just the best option - it was the{" "}
            <strong>only viable option</strong> that could satisfy stakeholder
            requirements while meeting competitive and organizational
            constraints.
          </p>

          {/* Vendor Fatal Flaws */}
          <div className="mb-8">
            <h4 className="text-lg font-bold text-red-700 mb-3">
              Vendor Platform Approach - Fatal Flaws:
            </h4>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <span className="text-red-500 mr-2 mt-1">&#x2022;</span>
                <span>
                  <strong>Stakeholder rejection:</strong> Violates S1 (quarterly
                  results), S2 (exit ability), S3 (decentralized culture), S5
                  (bounded risk), S6 (bottom-up adoption), S8 (no vendor
                  dependency)
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-red-500 mr-2 mt-1">&#x2022;</span>
                <span>
                  <strong>Competitive failure:</strong> Commoditizes the one
                  defensible advantage (institutional knowledge)
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-red-500 mr-2 mt-1">&#x2022;</span>
                <span>
                  <strong>Organizational impossibility:</strong> Requires $2-5M
                  (exceeds budget 20-50x), mandates (culturally impossible),
                  training prerequisites (violates change fatigue), English-only
                  (excludes 90% of workforce)
                </span>
              </li>
            </ul>
          </div>

          {/* Custom Fatal Flaws */}
          <div className="mb-8">
            <h4 className="text-lg font-bold text-orange-700 mb-3">
              Custom Big Bang Approach - Fatal Flaws:
            </h4>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <span className="text-orange-500 mr-2 mt-1">&#x2022;</span>
                <span>
                  <strong>Stakeholder rejection:</strong> Violates S1 (quarterly
                  results), S2 (exit ability), S3 (decentralized culture), S4
                  (incremental delivery), S5 (bounded risk), S6 (bottom-up
                  adoption)
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-orange-500 mr-2 mt-1">&#x2022;</span>
                <span>
                  <strong>Competitive failure:</strong> Requires AI specialist
                  recruitment (talent market inaccessible; sector cannot compete
                  with private sector compensation)
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-orange-500 mr-2 mt-1">&#x2022;</span>
                <span>
                  <strong>Organizational impossibility:</strong> Requires $3-7M
                  investment, centralized coordination (structure prevents),
                  mandates (culture rejects), simultaneous rollout (operationally
                  infeasible across 115 countries)
                </span>
              </li>
            </ul>
          </div>

          {/* Phased Internal Build - Why It Works */}
          <div className="mb-8">
            <h4 className="text-lg font-bold text-green-700 mb-4">
              Phased Internal Build - Why It Works:
            </h4>

            <div className="space-y-6">
              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <h5 className="font-bold text-navy mb-3">
                  Satisfies ALL primary stakeholder CTQs (S1-S8):
                </h5>
                <ul className="space-y-1 text-gray-700">
                  <li>
                    &#x2713; Quarterly value + 5-year optionality (S1)
                  </li>
                  <li>
                    &#x2713; Decisive investment + exit ability at every phase
                    (S2)
                  </li>
                  <li>
                    &#x2713; Enterprise intelligence + decentralized self-initiated
                    adoption (S3)
                  </li>
                  <li>
                    &#x2713; Incremental delivery with value every phase (S4)
                  </li>
                  <li>
                    &#x2713; Bounded risk with exit optionality (S5)
                  </li>
                  <li>
                    &#x2713; Bottom-up self-initiated adoption through peer
                    demonstration (S6)
                  </li>
                  <li>
                    &#x2713; Customer choice with no forced workflow changes (S7)
                  </li>
                  <li>
                    &#x2713; No vendor dependency, platform agnostic (S8)
                  </li>
                </ul>
              </div>

              <div className="bg-teal/5 border-l-4 border-teal p-4 rounded">
                <h5 className="font-bold text-navy mb-3">
                  Validated by competitive analysis (C1-C4):
                </h5>
                <ul className="space-y-1 text-gray-700">
                  <li>
                    &#x2713; Proprietary on unique 115-country knowledge
                  </li>
                  <li>
                    &#x2713; Dramatic efficiency through AI-speed knowledge
                    access
                  </li>
                  <li>
                    &#x2713; Defensible differentiation competitors cannot
                    replicate
                  </li>
                  <li>
                    &#x2713; Built with existing staff progressively upskilled
                  </li>
                </ul>
              </div>

              <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
                <h5 className="font-bold text-navy mb-3">
                  Validated by organizational analysis (O1-O7):
                </h5>
                <ul className="space-y-1 text-gray-700">
                  <li>
                    &#x2713; $163.1K Direct Investment ($11,100 infrastructure) with
                    bounded risk
                  </li>
                  <li>
                    &#x2713; Self-initiated country-by-country adoption respecting
                    consensus culture
                  </li>
                  <li>
                    &#x2713; Immediate value with embedded learning, no training
                    prerequisites
                  </li>
                  <li>&#x2713; Four languages from day one</li>
                  <li>
                    &#x2713; Peer demonstration and mission framing as adoption
                    mechanism
                  </li>
                  <li>
                    &#x2713; Passive knowledge capture from relational networks
                    without expert disruption
                  </li>
                  <li>
                    &#x2713; Works with strongly aligned cultural elements rather
                    than requiring organizational change
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* Key Strategic Insights */}
      <section className="py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Key Strategic Insights
          </h2>

          {/* CTQ-Driven Design Process */}
          <div className="mb-10">
            <h3 className="text-xl font-bold text-navy mb-4">
              CTQ-Driven Design Process
            </h3>
            <p className="text-gray-700 leading-relaxed mb-4">
              The Critical-To-Quality approach ensured rigorous requirements
              extraction and validation:
            </p>
            <ol className="list-decimal list-inside space-y-2 text-gray-700 ml-4">
              <li>
                <strong>Stakeholders First:</strong> Start with what stakeholders
                explicitly said they need (S1-S8)
              </li>
              <li>
                <strong>Analytical Validation:</strong> Use Porter&apos;s and 7S
                to validate WHY stakeholder needs are real and identify
                ADDITIONAL requirements (C1-C4, O1-O7)
              </li>
              <li>
                <strong>Pugh Matrix Evaluation:</strong> Score alternatives
                against all CTQs to find viable solutions
              </li>
              <li>
                <strong>Selection:</strong> Choose solution that satisfies
                stakeholder voice AND passes analytical validation
              </li>
            </ol>
          </div>

          {/* Why Alternatives Failed */}
          <div className="mb-10">
            <h3 className="text-xl font-bold text-navy mb-4">
              Why Alternatives Failed
            </h3>
            <p className="text-gray-700 leading-relaxed mb-3">
              <strong>
                Both Vendor Platform and Custom Big Bang failed because:
              </strong>
            </p>
            <ul className="space-y-2 text-gray-700 ml-4">
              <li className="flex items-start">
                <span className="text-navy mr-2 mt-1">&#x2022;</span>
                <span>
                  Designed for different organizational models (centralized
                  control, mandate authority) than what 7S revealed
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-navy mr-2 mt-1">&#x2022;</span>
                <span>
                  Assumed different competitive contexts (standardization,
                  external expertise) than what Porter&apos;s showed
                </span>
              </li>
              <li className="flex items-start">
                <span className="text-navy mr-2 mt-1">&#x2022;</span>
                <span>
                  Force organizations to choose which stakeholder groups to
                  disappoint rather than satisfying all simultaneously
                </span>
              </li>
            </ul>
          </div>

          {/* The Power of Stakeholder-First CTQ Methodology */}
          <div className="mb-10">
            <h3 className="text-xl font-bold text-navy mb-4">
              The Power of Stakeholder-First CTQ Methodology
            </h3>

            <div className="space-y-4">
              <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                <h5 className="font-bold text-navy mb-2">
                  Without listening to stakeholder voice first:
                </h5>
                <ul className="space-y-1 text-gray-700">
                  <li className="flex items-start">
                    <span className="text-red-500 mr-2 mt-1">&#x2022;</span>
                    <span>
                      Might have pursued vendor platform (standard practice,
                      compelling sales pitch)
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-red-500 mr-2 mt-1">&#x2022;</span>
                    <span>
                      Would have violated what stakeholders explicitly said they
                      need
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-red-500 mr-2 mt-1">&#x2022;</span>
                    <span>
                      $2-5M investment lost, trust further damaged,
                      transformation failed
                    </span>
                  </li>
                </ul>
              </div>

              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <h5 className="font-bold text-navy mb-2">
                  With stakeholder-first CTQ methodology:
                </h5>
                <ul className="space-y-1 text-gray-700">
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">&#x2022;</span>
                    <span>
                      Stakeholder requirements treated as primary constraints
                      (S1-S8)
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">&#x2022;</span>
                    <span>
                      Analyses validate why those requirements are real (C1-C4,
                      O1-O7)
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">&#x2022;</span>
                    <span>
                      Pugh Matrix reveals Phased Internal Build as only viable
                      solution
                    </span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2 mt-1">&#x2022;</span>
                    <span>
                      $163.1K Direct Investment, all stakeholder needs satisfied,
                      transformation successful
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* Navigation */}
      <section className="py-12 bg-gray-50">
        <Container size="reading">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-8 border-t border-gray-200">
            <Link
              href="/strategy"
              className="inline-flex items-center text-teal hover:text-teal/80 font-semibold"
            >
              &larr; Return to Strategy Overview
            </Link>
            <Link
              href="/transformation/three-horizons"
              className="inline-flex items-center text-teal hover:text-teal/80 font-semibold"
            >
              Continue to Implementation Framework: Three Horizons &rarr;
            </Link>
          </div>
        </Container>
      </section>
    </>
  );
}
