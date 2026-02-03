import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { Container } from "@/components/layout/Container";

export const metadata: Metadata = {
  title: "Stakeholder CTQ Analysis - Deriving Critical to Quality Requirements",
  description:
    "Stakeholder needs analysis and Critical to Quality requirements derivation for enterprise AI transformation strategy.",
};

export default function StakeholderCtqPage() {
  return (
    <>
      <PageHeader
        title="Stakeholder CTQ Analysis"
        subtitle="Deriving Critical to Quality requirements from stakeholders"
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
            <span className="text-gray-900">Stakeholder CTQ</span>
          </nav>
        </Container>
      </section>

      {/* Introduction */}
      <section className="bg-gray-50 py-12">
        <Container size="reading">
          <p className="text-lg text-gray-700 leading-relaxed">
            Strategic analysis began with understanding stakeholder needs.
            Through a mix of one-on-one meetings, focus group discussions, and
            surveys, we gathered perspectives from each stakeholder group. Each
            brought different, often conflicting requirements that any solution
            would need to satisfy simultaneously. From these inputs, we derived
            Critical to Quality specifications that defined success criteria
            before evaluating approaches.
          </p>
        </Container>
      </section>

      {/* Stakeholder Needs */}
      <section className="py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Stakeholder Needs
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-sm">
              <thead>
                <tr className="bg-navy text-white">
                  <th className="border border-navy/70 p-3 text-left font-semibold">
                    Stakeholder
                  </th>
                  <th className="border border-navy/70 p-3 text-left font-semibold">
                    Needs
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr className="bg-white">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    The Board
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    Visible AI progress on quarterly timelines; fast ROI
                    throughout transformation (not future promises); demonstrate
                    innovation to stakeholders; prove organization closing
                    competitive gaps
                  </td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    C-Suite
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    Risk-averse after past failures; ability to exit without sunk
                    costs; tangible returns at each investment stage; capabilities
                    that compound over time; no all-or-nothing bets
                  </td>
                </tr>
                <tr className="bg-white">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    Culture &amp; People
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    Immediate value at division/regional levels; no headquarters
                    mandates; solutions working in all 4 languages; zero appetite
                    for &quot;another corporate initiative&quot;; reduced burden
                    (not added)
                  </td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    Customers
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    Consistency from long-standing relationships; no imposed AI;
                    improved quality and personalization; no forced workflow
                    changes; transparency and impact metrics; compliance across
                    115+ countries; data sovereignty requirements
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </Container>
      </section>

      {/* Critical to Quality Requirements */}
      <section className="py-16 bg-gray-50">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Critical to Quality Requirements
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow-sm">
              <thead>
                <tr className="bg-navy text-white">
                  <th className="border border-navy/70 p-3 text-left font-semibold">
                    Category
                  </th>
                  <th className="border border-navy/70 p-3 text-left font-semibold">
                    Requirements
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr className="bg-white">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    Cultural
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    <ul className="space-y-1">
                      <li>4-language support from day one</li>
                      <li>Bottom-up adoption via demonstrated value</li>
                      <li>Rebuild trust by proving value first</li>
                      <li>Reduce staff burden</li>
                      <li>Organic peer-validated adoption</li>
                      <li>
                        Address job-loss fears by investing in people
                      </li>
                    </ul>
                  </td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    Financial
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    <ul className="space-y-1">
                      <li>Quarterly demonstrable value</li>
                      <li>Exit optionality at each phase</li>
                      <li>Cost less than 1% of vendor platforms</li>
                      <li>Deploy in weeks per phase</li>
                      <li>
                        Bounded risk with ability to stop without losing prior
                        investment
                      </li>
                    </ul>
                  </td>
                </tr>
                <tr className="bg-white">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    Competitive
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    <ul className="space-y-1">
                      <li>
                        Amplify (not commoditize) institutional knowledge
                      </li>
                      <li>
                        Build proprietary non-purchasable capabilities
                      </li>
                      <li>
                        Make 115-country expertise accessible at AI speed
                      </li>
                      <li>
                        Create defensible moat with immediate productivity gains
                      </li>
                    </ul>
                  </td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="border border-gray-200 p-3 font-semibold text-navy align-top">
                    Operational
                  </td>
                  <td className="border border-gray-200 p-3 text-gray-700">
                    <ul className="space-y-1">
                      <li>
                        Work across 115+ countries with varying regulations
                      </li>
                      <li>
                        Compounding capabilities (each phase builds on last)
                      </li>
                      <li>
                        Satisfy diverse stakeholders simultaneously
                      </li>
                      <li>
                        No mandated reorganization or process changes
                      </li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </Container>
      </section>

      {/* Navigation */}
      <section className="py-12 bg-white">
        <Container size="reading">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4 pt-8 border-t border-gray-200">
            <Link
              href="/strategy"
              className="inline-flex items-center text-teal hover:text-teal/80 font-semibold"
            >
              &larr; Return to Strategy Overview
            </Link>
            <Link
              href="/strategy/mckinsey-7s"
              className="inline-flex items-center text-teal hover:text-teal/80 font-semibold"
            >
              Continue to McKinsey 7S Analysis &rarr;
            </Link>
          </div>
        </Container>
      </section>
    </>
  );
}
