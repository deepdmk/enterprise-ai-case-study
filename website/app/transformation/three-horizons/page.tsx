import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";

export const metadata: Metadata = {
  title: "Three Horizons Framework - Strategic Design Foundation",
  description:
    "Strategic architecture for Phased Internal Build: defend core operations, build emerging capabilities, and create transformative options through six purpose-designed phases",
};

export default function ThreeHorizonsPage() {
  return (
    <>
      <PageHeader
        title="Three Horizons Framework"
        subtitle="Strategic Design Foundation"
      />

      {/* Breadcrumb Navigation */}
      <section className="bg-white border-b border-gray-200">
        <Container size="reading">
          <nav className="py-4 text-sm text-gray-600" aria-label="Breadcrumb">
            <Link
              href="/transformation"
              className="hover:text-teal focus:outline-none focus:ring-2 focus:ring-teal"
            >
              Transformation
            </Link>
            <span className="mx-2">&rarr;</span>
            <span className="text-gray-900">Three Horizons Framework</span>
          </nav>
        </Container>
      </section>

      {/* BLUF Section */}
      <section className="bg-gray-50 py-12">
        <Container size="reading">
          <p className="text-lg text-gray-700 leading-relaxed">
            Three Horizons Framework provides the strategic architecture for
            Phased Internal Build by defining what the organization must
            accomplish at each horizon. Competitive analysis (Porter&apos;s)
            revealed we must defend core operations, build proprietary
            advantages, and create strategic options. Organizational constraints
            (7S) required a progressive, voluntary, bounded-risk approach. Three
            Horizons framework structures these requirements into three strategic
            objectives: H1 (Defend/Extend Core), H2 (Build Emerging
            Capabilities), H3 (Create Transformative Options). From these
            horizon objectives, we designed{" "}
            <strong className="font-semibold text-navy">six phases</strong> to
            achieve the required transformation with{" "}
            <strong className="font-semibold text-navy">
              exit optionality at every horizon boundary
            </strong>
            .
          </p>
        </Container>
      </section>

      {/* What Each Horizon Must Accomplish */}
      <section className="py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            What Each Horizon Must Accomplish
          </h2>

          <p className="text-gray-700 leading-relaxed mb-12">
            Three Horizons Framework (McKinsey) provides the strategic
            architecture by defining three clear objectives: defend core
            operations, build emerging competitive advantages, and create
            transformative strategic options. Each horizon&apos;s objectives are
            derived directly from competitive analysis (Porter&apos;s),
            organizational constraints (7S), and stakeholder requirements.
          </p>

          {/* Horizon 1 Card */}
          <Card className="border-t-4 border-t-teal mb-8">
            <h3 className="text-2xl font-bold text-navy mb-4">
              Horizon 1: Defend and Extend the Core
            </h3>
            <p className="text-gray-700 mb-6">
              <strong className="font-semibold text-navy">
                Strategic Imperative:
              </strong>{" "}
              Core business under threat from lean competitors (Porter&apos;s),
              organization in crisis requiring immediate value delivery (7S,
              stakeholders), must defend by improving existing operations
              efficiency.
            </p>

            <div className="overflow-x-auto">
              <table className="w-full border border-gray-200">
                <thead className="bg-navy text-white">
                  <tr>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      What H1 Must Deliver
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Success Criteria
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Defend Core Business:
                      </strong>{" "}
                      Protect competitive position under threat
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Core operations measurably more efficient
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Extend Core Efficiency:
                      </strong>{" "}
                      Improve operations without disruption
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Competitive vulnerability reduced
                    </td>
                  </tr>
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Preserve Client Value:
                      </strong>{" "}
                      No workflow changes, better service
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Staff self-initiating adoption (proof of value)
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Generate Resources:
                      </strong>{" "}
                      ROI funds next horizon
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Positive ROI funding H2 consideration
                    </td>
                  </tr>
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Build Credibility:
                      </strong>{" "}
                      Success creates trust for H2 investment
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Decision point: Can stop with defended/extended core
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Card>

          {/* Horizon 2 Card */}
          <Card className="border-t-4 border-t-amber mb-8">
            <h3 className="text-2xl font-bold text-navy mb-4">
              Horizon 2: Build Emerging Competitive Advantages
            </h3>
            <p className="text-gray-700 mb-6">
              <strong className="font-semibold text-navy">
                Strategic Imperative:
              </strong>{" "}
              Only defensible competitive advantage is proprietary capabilities
              on unique institutional knowledge (Porter&apos;s), must build with
              existing staff as AI talent is inaccessible (7S), stakeholders
              require non-commoditizable capabilities.
            </p>

            <div className="overflow-x-auto">
              <table className="w-full border border-gray-200">
                <thead className="bg-navy text-white">
                  <tr>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      What H2 Must Deliver
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Success Criteria
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Genuinely New Capabilities:
                      </strong>{" "}
                      Not faster existing work, but work we couldn&apos;t do
                      before
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      New capabilities operational (not just efficiency gains)
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Proprietary Advantage:
                      </strong>{" "}
                      Capabilities competitors cannot purchase or replicate
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Staff can do work previously impossible
                    </td>
                  </tr>
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Defensible Differentiation:
                      </strong>{" "}
                      Based on unique institutional knowledge
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Competitive differentiation achieved
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Advanced Staff Capabilities:
                      </strong>{" "}
                      Internal expertise, not external dependency
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Proprietary advantage built on institutional knowledge
                    </td>
                  </tr>
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Competitive Moat:
                      </strong>{" "}
                      Sustainable advantage that strengthens over time
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Decision point: Can stop with defended core + competitive
                      advantages
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Card>

          {/* Horizon 3 Card */}
          <Card className="border-t-4 border-t-magenta mb-8">
            <h3 className="text-2xl font-bold text-navy mb-4">
              Horizon 3: Create Transformative Strategic Options
            </h3>
            <p className="text-gray-700 mb-6">
              <strong className="font-semibold text-navy">
                Strategic Imperative:
              </strong>{" "}
              Rapidly changing AI environment requires strategic flexibility and
              ongoing innovation capacity (Porter&apos;s, 7S), stakeholders
              require strategic optionality beyond one-time transformation.
            </p>

            <div className="overflow-x-auto">
              <table className="w-full border border-gray-200">
                <thead className="bg-navy text-white">
                  <tr>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      What H3 Must Deliver
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Success Criteria
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Transformative Capabilities:
                      </strong>{" "}
                      Fundamentally different ways of operating
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Breakthrough capabilities operational
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Strategic Optionality:
                      </strong>{" "}
                      Options for future innovation and adaptation
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Strategic options created (not just current improvements)
                    </td>
                  </tr>
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Organizational-Scale Intelligence:
                      </strong>{" "}
                      Enterprise-wide AI capabilities
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Innovation capacity built (ongoing capability development)
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Innovation Capacity:
                      </strong>{" "}
                      Internal expertise to continue evolving
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Organizational transformation complete
                    </td>
                  </tr>
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Future-Ready Organization:
                      </strong>{" "}
                      Sustainable competitive advantage
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Sustainable advantage: Capability strengthens over time
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Card>
        </Container>
      </section>

      {/* From Horizons to Phase Design */}
      <section className="bg-gray-50 py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            From Horizons to Phase Design
          </h2>

          {/* Design Principle Callout */}
          <Card className="border-l-4 border-l-teal bg-teal/5 mb-12">
            <p className="text-lg font-semibold text-navy mb-2">
              Design Principle
            </p>
            <p className="text-gray-700">
              <strong className="font-semibold text-navy">
                Start with horizon objectives &rarr; Design phases to achieve
                them
              </strong>
            </p>
            <p className="text-gray-700 mt-2">
              Each horizon&apos;s strategic requirements drove the design of
              specific phases. Phases are not arbitrary divisions&mdash;they are
              purpose-built to accomplish horizon objectives while respecting
              organizational constraints.
            </p>
          </Card>

          {/* Horizon 1: Phases 0, 1, 2 */}
          <div className="mb-12">
            <h3 className="text-2xl font-bold text-navy mb-4">
              Horizon 1: Phases 0, 1, 2 (Defend/Extend Core)
            </h3>
            <p className="text-gray-700 mb-6">
              <strong className="font-semibold text-navy">
                H1 Objective:
              </strong>{" "}
              Defend and extend core operations through existing capabilities
              augmentation
            </p>

            <div className="overflow-x-auto mb-6">
              <table className="w-full border border-gray-200">
                <thead className="bg-navy text-white">
                  <tr>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Phase
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Purpose & Design Rationale
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Why H1?
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Deliverable
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Value
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700 font-semibold">
                      <strong className="font-semibold text-navy">
                        Phase 0: Registry Foundation
                      </strong>{" "}
                      (Month 0)
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Put registries in place to track experiments, data, and
                      models
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Must establish tracking infrastructure before any AI work
                      begins
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Experiment registry, data registry, model registry
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Enables systematic AI development and governance
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700 font-semibold">
                      <strong className="font-semibold text-navy">
                        Phase 1: Knowledge Access
                      </strong>{" "}
                      (Months 1-3)
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Make trapped knowledge accessible to defend competitive
                      position
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Works with{" "}
                      <strong className="font-semibold text-navy">
                        existing
                      </strong>{" "}
                      knowledge, just makes it accessible
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Natural language query, 4 languages, universal access
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Core operations immediately more efficient
                    </td>
                  </tr>
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700 font-semibold">
                      <strong className="font-semibold text-navy">
                        Phase 2: Task Automation
                      </strong>{" "}
                      (Months 4-9)
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Automate repetitive work in{" "}
                      <strong className="font-semibold text-navy">
                        existing
                      </strong>{" "}
                      workflows
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Works with{" "}
                      <strong className="font-semibold text-navy">
                        existing
                      </strong>{" "}
                      tasks and processes, just automates them
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      50% repetitive work automated
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Extended core efficiency, resources generated for H2
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p className="text-gray-700 leading-relaxed mb-4">
              <strong className="font-semibold text-navy">
                Why H1 Required Three Phases:
              </strong>{" "}
              To defend and extend core operations, we needed to establish
              tracking infrastructure (Phase 0), make existing knowledge
              accessible (Phase 1), and automate existing workflows (Phase 2).
              All three phases work with what already exists rather than creating
              new capabilities. Additionally, stakeholder requirements for
              quarterly ROI (S1) and exit optionality (S2) drove the decision to
              break H1 into three phases rather than one&mdash;each phase
              delivers independent value with decision points, enabling
              progressive investment with bounded risk.
            </p>

            <p className="text-gray-700 font-semibold">
              <strong className="font-semibold text-navy">
                H1 Investment:
              </strong>{" "}
              $106,000 ($0 Phase 0 + $62.4K Phase 1 + $43.6K Phase 2) |{" "}
              <strong className="font-semibold text-navy">
                H1 Timeline:
              </strong>{" "}
              Months 0-9 |{" "}
              <strong className="font-semibold text-navy">
                H1 Decision Point:
              </strong>{" "}
              Can stop with defended/extended core operations
            </p>
          </div>

          {/* Horizon 2: Phase 3 */}
          <div className="mb-12">
            <h3 className="text-2xl font-bold text-navy mb-4">
              Horizon 2: Phase 3 (Build Emerging)
            </h3>
            <p className="text-gray-700 mb-6">
              <strong className="font-semibold text-navy">
                H2 Objective:
              </strong>{" "}
              Build genuinely new competitive capabilities
            </p>

            <div className="overflow-x-auto mb-6">
              <table className="w-full border border-gray-200">
                <thead className="bg-navy text-white">
                  <tr>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Phase
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Purpose & Design Rationale
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Why H2?
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Deliverable
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Value
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700 font-semibold">
                      <strong className="font-semibold text-navy">
                        Phase 3: Division Intelligence
                      </strong>{" "}
                      (Months 7-12)
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Create sophisticated analytical capabilities on unique
                      institutional knowledge
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Creates{" "}
                      <strong className="font-semibold text-navy">
                        genuinely new
                      </strong>{" "}
                      capabilities that competitors cannot purchase or replicate
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Advanced analysis, division-specific intelligence,
                      sophisticated queries
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Staff can do work previously impossible (not just faster)
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p className="text-gray-700 leading-relaxed mb-4">
              <strong className="font-semibold text-navy">
                Why H2 Required This Phase:
              </strong>{" "}
              To build genuinely new competitive advantages, we needed
              capabilities that don&apos;t exist today. Phase 3 was designed to
              create division-level intelligence&mdash;sophisticated analytical
              capabilities that enable work previously impossible, not just
              faster existing work.
            </p>

            <p className="text-gray-700 font-semibold">
              <strong className="font-semibold text-navy">
                H2 Investment:
              </strong>{" "}
              $31,200 (Phase 3) |{" "}
              <strong className="font-semibold text-navy">
                H2 Timeline:
              </strong>{" "}
              Months 7-12 (overlap with H1 Months 7-9) |{" "}
              <strong className="font-semibold text-navy">
                H2 Decision Point:
              </strong>{" "}
              Can stop with defended core + competitive advantages
            </p>
          </div>

          {/* Horizon 3: Phase 4 */}
          <div className="mb-12">
            <h3 className="text-2xl font-bold text-navy mb-4">
              Horizon 3: Phases 4 &amp; 5 (Create Transformative Options)
            </h3>
            <p className="text-gray-700 mb-6">
              <strong className="font-semibold text-navy">
                H3 Objective:
              </strong>{" "}
              Create transformative strategic options
            </p>

            <div className="overflow-x-auto mb-6">
              <table className="w-full border border-gray-200">
                <thead className="bg-navy text-white">
                  <tr>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Phase
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Purpose & Design Rationale
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Why H3?
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Deliverable
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Value
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr className="bg-white hover:bg-gray-50">
                    <td className="px-4 py-3 text-gray-700 font-semibold">
                      <strong className="font-semibold text-navy">
                        Phase 4: Agentic Discovery
                      </strong>{" "}
                      (Months 10-15)
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Enable cross-division experimentation in sandboxed
                      environments to discover patterns and generate training
                      data. H3 requires breakthrough capabilities&mdash;Phase 4
                      creates experimental foundation through siloed discovery
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Siloed experimentation generates training corpus for
                      orchestration
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Experimentation patterns, cross-division insights,
                      training data corpus
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Discovery of emergent organizational patterns
                    </td>
                  </tr>
                  <tr className="bg-gray-50 hover:bg-gray-100">
                    <td className="px-4 py-3 text-gray-700 font-semibold">
                      <strong className="font-semibold text-navy">
                        Phase 5: Orchestrated System
                      </strong>{" "}
                      (Months 13-18)
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Train orchestrator on Phase 4 experimental data to enable
                      organizational-scale intelligence. Phase 5 transforms
                      siloed discoveries into unified orchestration
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Transforms
                      </strong>{" "}
                      how the organization operates (not incremental improvement)
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Trained orchestrator, integrated multi-agent system,
                      organizational-scale intelligence
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      Strategic options for future innovation and adaptation
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p className="text-gray-700 leading-relaxed mb-4">
              <strong className="font-semibold text-navy">
                Why H3 Required Two Phases:
              </strong>{" "}
              To create transformative strategic options, we needed breakthrough
              capabilities beyond incremental improvements. Phase 4 generates
              training data through siloed experimentation across
              divisions&mdash;discovering patterns in sandboxed environments.
              Phase 5 uses this training data to build the orchestrator that
              unifies these discoveries into organizational-scale intelligence.
              Phase 4 creates the data that makes Phase 5 possible.
            </p>

            <p className="text-gray-700 font-semibold">
              <strong className="font-semibold text-navy">
                H3 Investment:
              </strong>{" "}
              $25,900 ($15.5K Phase 4 + $10.4K Phase 5) |{" "}
              <strong className="font-semibold text-navy">
                H3 Timeline:
              </strong>{" "}
              Months 10-18 (overlap with H2 Months 10-12, Phase 4/5 overlap
              Months 13-15) |{" "}
              <strong className="font-semibold text-navy">
                H3 Outcome:
              </strong>{" "}
              Full transformation complete, ongoing innovation capacity
            </p>
          </div>
        </Container>
      </section>

      {/* Final Phase Design */}
      <section className="py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-4 text-center">
            Final Phase Design
          </h2>
          <p className="text-gray-700 text-center mb-8">
            <strong className="font-semibold text-navy">
              Six phases designed from three horizon objectives:
            </strong>
          </p>

          <div className="overflow-x-auto mb-8">
            <table className="w-full border border-gray-200">
              <thead className="bg-navy text-white">
                <tr>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Phase
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Timeline
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Horizon
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Purpose
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Deliverable
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Investment
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr className="bg-white hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      Phase 0: Registry Foundation
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Month 0</td>
                  <td className="px-4 py-3 text-gray-700">H1</td>
                  <td className="px-4 py-3 text-gray-700">
                    Establish tracking infrastructure for systematic AI
                    development
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    Experiment, data, model registries
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    $0 infrastructure
                  </td>
                </tr>
                <tr className="bg-gray-50 hover:bg-gray-100">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      Phase 1: Knowledge Access
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Months 1-3</td>
                  <td className="px-4 py-3 text-gray-700">H1</td>
                  <td className="px-4 py-3 text-gray-700">
                    Make existing knowledge accessible to defend competitive
                    position
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    Natural language query, 4 languages, universal access
                  </td>
                  <td className="px-4 py-3 text-gray-700">$62,400</td>
                </tr>
                <tr className="bg-white hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      Phase 2: Task Automation
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Months 4-9</td>
                  <td className="px-4 py-3 text-gray-700">H1</td>
                  <td className="px-4 py-3 text-gray-700">
                    Automate repetitive work in existing workflows to extend
                    core efficiency
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    50% repetitive work automated
                  </td>
                  <td className="px-4 py-3 text-gray-700">$43,600</td>
                </tr>
                <tr className="bg-gray-50 hover:bg-gray-100">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      Phase 3: Division Intelligence
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Months 7-12</td>
                  <td className="px-4 py-3 text-gray-700">H2</td>
                  <td className="px-4 py-3 text-gray-700">
                    Create genuinely new analytical capabilities on
                    institutional knowledge
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    Advanced analysis, division-specific intelligence
                  </td>
                  <td className="px-4 py-3 text-gray-700">$31,200</td>
                </tr>
                <tr className="bg-white hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      Phase 4: Agentic Discovery
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Months 10-15</td>
                  <td className="px-4 py-3 text-gray-700">H3</td>
                  <td className="px-4 py-3 text-gray-700">
                    Enable cross-division experimentation to discover patterns
                    and generate training data
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    Experimentation patterns, training data corpus
                  </td>
                  <td className="px-4 py-3 text-gray-700">$15,500</td>
                </tr>
                <tr className="bg-gray-50 hover:bg-gray-100">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      Phase 5: Orchestrated System
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Months 13-18</td>
                  <td className="px-4 py-3 text-gray-700">H3</td>
                  <td className="px-4 py-3 text-gray-700">
                    Train orchestrator on Phase 4 data for organizational-scale
                    intelligence
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    Trained orchestrator, integrated multi-agent system
                  </td>
                  <td className="px-4 py-3 text-gray-700">$10,400</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p className="text-gray-700 font-semibold text-center">
            <strong className="font-semibold text-navy">
              Total Investment:
            </strong>{" "}
            $163.1K Direct Investment ($11,100 infrastructure) |{" "}
            <strong className="font-semibold text-navy">
              Total Timeline:
            </strong>{" "}
            18 months |{" "}
            <strong className="font-semibold text-navy">Decision Points:</strong>{" "}
            After Phase 2 (H1), Phase 3 (H2), Phase 4 (H3), or Phase 5 (H3)
          </p>
        </Container>
      </section>

      {/* Design Validation */}
      <section className="bg-gray-50 py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-4">
            Design Validation
          </h2>
          <p className="text-gray-700 mb-8">
            <strong className="font-semibold text-navy">
              The phase design accomplishes all horizon objectives:
            </strong>
          </p>

          <div className="overflow-x-auto mb-8">
            <table className="w-full border border-gray-200">
              <thead className="bg-navy text-white">
                <tr>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Horizon Objective
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Phase(s) Designed
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    How Phases Achieve Objective
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr className="bg-white hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      H1: Defend Core
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Phases 0-2</td>
                  <td className="px-4 py-3 text-gray-700">
                    Registry foundation + knowledge access + task automation =
                    defended/extended core
                  </td>
                </tr>
                <tr className="bg-gray-50 hover:bg-gray-100">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      H2: Build Emerging
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Phase 3</td>
                  <td className="px-4 py-3 text-gray-700">
                    Division intelligence = genuinely new competitive
                    capabilities
                  </td>
                </tr>
                <tr className="bg-white hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">
                      H3: Create Transformative
                    </strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">Phases 4-5</td>
                  <td className="px-4 py-3 text-gray-700">
                    Agentic discovery (experimentation/training data) +
                    orchestrated system = transformative strategic options
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <p className="text-gray-700 font-semibold">
            <strong className="font-semibold text-navy">
              Strategic coherence:
            </strong>{" "}
            Every phase exists to accomplish a specific horizon objective. No
            phase is arbitrary. Phase 4 generates the training data that Phase 5
            requires&mdash;they are sequential and interdependent within H3.
          </p>

          {/* Back Link */}
          <div className="text-center pt-8 mt-8 border-t border-gray-200">
            <Link
              href="/transformation"
              className="inline-flex items-center text-teal hover:text-teal/80 font-semibold focus:outline-none focus:ring-2 focus:ring-teal"
              aria-label="Back to Transformation Framework"
            >
              &larr; Back to Transformation Framework
            </Link>
          </div>
        </Container>
      </section>
    </>
  );
}
