import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";

export const metadata: Metadata = {
  title: "Transformation Roadmap - Implementation Execution Path",
  description:
    "18-month, 6-phase transformation roadmap with $163.1K direct investment across three horizons: defend core, build emerging, create transformative",
};

const phases = [
  {
    id: 0,
    name: "Registry Foundation",
    timeline: "Month 0",
    months: [0, 0],
    horizon: "H1",
    purpose:
      "Establish tracking infrastructure for systematic AI development",
    deliverables: "Experiment, Data, Model registries operational",
    targetUsers: "Technical staff (2 FTE)",
    investment: "$0 (infrastructure)",
    successCriteria:
      "All three registries operational, governance framework established",
  },
  {
    id: 1,
    name: "Knowledge Access",
    timeline: "Months 1-3",
    months: [1, 3],
    horizon: "H1",
    purpose:
      "Make organizational knowledge accessible through natural language to defend competitive position",
    deliverables:
      "Unified embedding space, semantic search (4 languages), universal access",
    targetUsers: "All 8,000 staff",
    investment: "$62.4K ($5.4K infra + $57K training)",
    successCriteria:
      "90%+ query success, 80%+ self-initiated adoption, measurable time savings",
  },
  {
    id: 2,
    name: "Task Automation",
    timeline: "Months 4-9",
    months: [4, 9],
    horizon: "H1",
    purpose:
      "Automate repetitive work in existing workflows using Kaizen discovery model",
    deliverables: "Task-specific SLMs, 50% automation of repetitive work",
    targetUsers: "200-500 division/HQ staff",
    investment: "$43.6K ($3.6K infra + $40K training)",
    successCriteria:
      "50%+ work automated, 30-40% Phase 1 users advance, positive Kaizen culture",
  },
  {
    id: 3,
    name: "Division Intelligence",
    timeline: "Months 7-12",
    months: [7, 12],
    horizon: "H2",
    purpose:
      "Create new analytical capabilities through MoE architecture on unique institutional knowledge",
    deliverables:
      "Router model, division-specific expert models, MoE intelligence",
    targetUsers: "30-100 advanced users (15-20% of Phase 2)",
    investment: "$31.2K ($1.2K infra + $30K training)",
    successCriteria:
      "Division intelligence operational, 15-20% Phase 2 users adopt, competitive differentiation achieved",
  },
  {
    id: 4,
    name: "Agentic Discovery",
    timeline: "Months 10-15",
    months: [10, 15],
    horizon: "H3",
    purpose:
      "Enable cross-division experimentation to discover patterns and generate training data",
    deliverables:
      "Sandboxed experimentation, pattern discovery, training data corpus",
    targetUsers: "15-30 expert users (5-10% of Phase 3)",
    investment: "$15.5K ($500 infra + $15K training)",
    successCriteria:
      "Training data corpus generated, emergent patterns discovered, expert community engaged",
  },
  {
    id: 5,
    name: "Orchestrated System",
    timeline: "Months 13-18",
    months: [13, 18],
    horizon: "H3",
    purpose:
      "Train orchestrator on Phase 4 data to enable organizational-scale intelligence",
    deliverables:
      "Orchestrator trained, multi-agent system, organizational intelligence",
    targetUsers: "Phase 4 users + 20-30 technical leaders",
    investment: "$10.4K ($400 infra + $10K training)",
    successCriteria:
      "Orchestrator operational, multi-agent workflows functioning, innovation capacity built",
  },
];

const horizonColors: Record<string, { bg: string; border: string; text: string; barBg: string }> = {
  H1: { bg: "bg-blue-50", border: "border-blue-500", text: "text-blue-700", barBg: "bg-blue-500" },
  H2: { bg: "bg-emerald-50", border: "border-emerald-500", text: "text-emerald-700", barBg: "bg-emerald-500" },
  H3: { bg: "bg-purple-50", border: "border-purple-500", text: "text-purple-700", barBg: "bg-purple-500" },
};

const horizonLabels: Record<string, string> = {
  H1: "Defend Core",
  H2: "Build Emerging",
  H3: "Create Transformative",
};

export default function RoadmapPage() {
  const totalMonths = 19; // 0-18

  return (
    <>
      <PageHeader
        title="Transformation Roadmap"
        subtitle="Implementation Execution Path"
      />

      {/* Breadcrumb */}
      <section className="bg-white border-b border-gray-200">
        <Container size="reading">
          <nav
            className="py-4 text-sm text-gray-600"
            aria-label="Breadcrumb"
          >
            <Link
              href="/transformation"
              className="hover:text-teal focus:outline-none focus:ring-2 focus:ring-teal"
            >
              Transformation
            </Link>
            <span className="mx-2">&rarr;</span>
            <span className="text-gray-900">Transformation Roadmap</span>
          </nav>
        </Container>
      </section>

      {/* BLUF Section */}
      <section className="bg-gray-50 py-12">
        <Container size="reading">
          <p className="text-lg text-gray-700 leading-relaxed mb-6">
            The Transformation Roadmap outlines the practical execution path
            for the 18-month, 6-phase transformation (Phases 0-5).{" "}
            <strong className="font-semibold text-navy">
              Direct Investment: $163.1K
            </strong>{" "}
            ($11.1K infrastructure + $152K training programs).{" "}
            <strong className="font-semibold text-navy">
              Total Program Cost: $1,273.1K
            </strong>{" "}
            (includes $1,110K labor allocation required for any solution).
          </p>
          <p className="text-gray-700 leading-relaxed">
            Change management embedded in design: mission framing (not
            efficiency), self-initiated adoption (no mandates), embedded learning
            (no training burden), progressive complexity (8,000 diverse
            staff), continuous value delivery (reinforcement). Organizational
            structure: 8,000 staff with ~200-500 division workers progressing
            through phases using Kaizen discovery model. Internal build with
            small models maintains data sovereignty and cost control.
          </p>
        </Container>
      </section>

      {/* Key Metrics Cards */}
      <section className="py-12">
        <Container size="content">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { label: "Timeline", value: "18 months" },
              { label: "Phases", value: "6" },
              { label: "Horizons", value: "3" },
              { label: "Peak Staff", value: "5 FTE" },
              { label: "Direct Investment", value: "$163.1K" },
              { label: "Total Program", value: "$1,273.1K" },
            ].map((metric) => (
              <Card key={metric.label} className="text-center">
                <p className="text-2xl md:text-3xl font-bold text-navy">
                  {metric.value}
                </p>
                <p className="text-base text-gray-600 mt-1">{metric.label}</p>
              </Card>
            ))}
          </div>
        </Container>
      </section>

      {/* Core Principles */}
      <section className="bg-gray-50 py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Core Principles
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                title: "Mission Framing",
                description:
                  "AI amplifies mission impact, not efficiency",
              },
              {
                title: "Self-Initiated Adoption",
                description:
                  "Zero mandates, peer demonstration drives desire",
              },
              {
                title: "Embedded Learning",
                description: "Learn by doing, no training burden",
              },
              {
                title: "Progressive Complexity",
                description:
                  "Universal Phase 1, selective advancement",
              },
              {
                title: "Internal Build",
                description:
                  "Small models, data sovereignty, cost control",
              },
              {
                title: "Exit Optionality",
                description:
                  "Value delivered at every horizon boundary",
              },
            ].map((principle) => (
              <Card key={principle.title} className="border-t-4 border-t-teal">
                <h3 className="text-lg font-bold text-navy mb-2">
                  {principle.title}
                </h3>
                <p className="text-gray-700 text-base">
                  {principle.description}
                </p>
              </Card>
            ))}
          </div>
        </Container>
      </section>

      {/* Phase Execution Timeline */}
      <section className="py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Phase Execution Timeline
          </h2>

          {/* Timeline Visualization */}
          <div className="mb-12 overflow-x-auto">
            <div className="min-w-[700px]">
              {/* Month axis */}
              <div className="flex mb-2 pl-48">
                {Array.from({ length: totalMonths }, (_, i) => (
                  <div
                    key={i}
                    className="flex-1 text-xs text-gray-500 text-center"
                  >
                    {i}
                  </div>
                ))}
              </div>

              {/* Horizon groups */}
              {(["H1", "H2", "H3"] as const).map((horizon) => {
                const hPhases = phases.filter((p) => p.horizon === horizon);
                const colors = horizonColors[horizon];
                return (
                  <div key={horizon} className="mb-4">
                    <div className="flex items-center mb-1">
                      <div className="w-48 pr-4">
                        <span
                          className={`inline-block px-2 py-1 rounded text-xs font-bold ${colors.bg} ${colors.text}`}
                        >
                          {horizon}: {horizonLabels[horizon]}
                        </span>
                      </div>
                      <div className="flex-1 h-px bg-gray-200" />
                    </div>
                    {hPhases.map((phase) => (
                      <div key={phase.id} className="flex items-center mb-1">
                        <div className="w-48 pr-4 text-right">
                          <span className="text-base text-gray-700">
                            Phase {phase.id}: {phase.name}
                          </span>
                        </div>
                        <div className="flex-1 flex relative h-7">
                          {Array.from({ length: totalMonths }, (_, i) => (
                            <div key={i} className="flex-1 border-l border-gray-100" />
                          ))}
                          <div
                            className={`absolute top-0 h-full ${colors.barBg} rounded opacity-80`}
                            style={{
                              left: `${(phase.months[0] / totalMonths) * 100}%`,
                              width: `${((phase.months[1] - phase.months[0] + 1) / totalMonths) * 100}%`,
                            }}
                            title={`${phase.name}: ${phase.timeline}`}
                          >
                            <span className="text-xs text-white font-medium px-2 leading-7 whitespace-nowrap">
                              {phase.timeline}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                );
              })}

              {/* Decision points */}
              <div className="flex items-center mt-4">
                <div className="w-48 pr-4 text-right">
                  <span className="text-base font-semibold text-navy">
                    Decision Points
                  </span>
                </div>
                <div className="flex-1 flex relative h-7">
                  {Array.from({ length: totalMonths }, (_, i) => (
                    <div key={i} className="flex-1 border-l border-gray-100" />
                  ))}
                  {[
                    { month: 9, label: "H1 Decision" },
                    { month: 12, label: "H2 Decision" },
                    { month: 18, label: "H3 Decision" },
                  ].map((decisionPoint) => (
                    <div
                      key={decisionPoint.month}
                      className="absolute top-0 h-full flex items-center"
                      style={{
                        left: `${(decisionPoint.month / totalMonths) * 100}%`,
                      }}
                    >
                      <div className="w-0.5 h-full bg-red-400" />
                      <span className="text-xs text-red-600 font-medium ml-1 whitespace-nowrap">
                        {decisionPoint.label}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Phase Detail Table */}
          <div className="overflow-x-auto">
            <table className="w-full border border-gray-200">
              <thead className="bg-navy text-white">
                <tr>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Phase</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Timeline</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Purpose</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Target Users</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Direct Investment</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Success Criteria</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {phases.map((phase, i) => (
                  <tr
                    key={phase.id}
                    className={`${i % 2 === 0 ? "bg-white" : "bg-gray-50"} hover:bg-gray-100`}
                  >
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        Phase {phase.id}: {phase.name}
                      </strong>
                      <span className={`ml-2 inline-block px-1.5 py-0.5 rounded text-xs font-medium ${horizonColors[phase.horizon].bg} ${horizonColors[phase.horizon].text}`}>
                        {phase.horizon}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-700">{phase.timeline}</td>
                    <td className="px-4 py-3 text-gray-700">{phase.purpose}</td>
                    <td className="px-4 py-3 text-gray-700">{phase.targetUsers}</td>
                    <td className="px-4 py-3 text-gray-700">{phase.investment}</td>
                    <td className="px-4 py-3 text-gray-700">{phase.successCriteria}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-base text-gray-600 mt-4">
            Phases overlap intentionally per Three Horizons model (H1: 0-2, H2: 3, H3: 4-5). See Cost Matrix for detailed labor allocation across overlapping phases.
          </p>
        </Container>
      </section>

      {/* ADKAR Change Management */}
      <section className="bg-gray-50 py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Change Management: ADKAR Integration
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full border border-gray-200">
              <thead className="bg-navy text-white">
                <tr>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">ADKAR Principle</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Phase 1</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Phase 2</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Phase 3</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Phases 4-5</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {[
                  {
                    principle: "Awareness",
                    p1: '"Access knowledge instantly to help people in real-time" (mission framing)',
                    p2: '"Automate repetitive work to free time for complex human needs"',
                    p3: '"Build specialized intelligence to support sophisticated mission work"',
                    p45: '"Breakthrough capabilities through experimental discovery"',
                  },
                  {
                    principle: "Desire",
                    p1: "Self-initiated adoption, peer demonstration (champions)",
                    p2: "Self-selected advancement (see Phase 1 successes)",
                    p3: "Advanced users self-select based on specialized needs",
                    p45: "Expert users voluntarily explore cutting-edge capabilities",
                  },
                  {
                    principle: "Knowledge",
                    p1: "Zero training burden\u2014natural language interaction, learn by doing",
                    p2: "Light AI literacy (4-8 hours)\u2014identify opportunities, not technical training",
                    p3: "Router handles complexity\u2014users query, system selects expert",
                    p45: "~15-20 hours voluntary training for orchestration expertise",
                  },
                  {
                    principle: "Ability",
                    p1: "Universal accessibility (multilingual, simple interface, no prerequisites)",
                    p2: "Kaizen model\u2014users spot opportunities, technical staff implement",
                    p3: "Progressive from Phase 2 proficiency, self-selection based on capability",
                    p45: "Highly selective\u2014requires Phase 1-3 proficiency + technical sophistication",
                  },
                  {
                    principle: "Reinforcement",
                    p1: "Immediate value (find answers in seconds vs. days)",
                    p2: "Time freed for mission-critical work, continuous experimentation",
                    p3: "Work previously impossible now possible (not just faster)",
                    p45: "Organizational transformation complete, ongoing innovation capacity",
                  },
                ].map((row, i) => (
                  <tr
                    key={row.principle}
                    className={`${i % 2 === 0 ? "bg-white" : "bg-gray-50"} hover:bg-gray-100`}
                  >
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        {row.principle}
                      </strong>
                    </td>
                    <td className="px-4 py-3 text-gray-700 text-sm">{row.p1}</td>
                    <td className="px-4 py-3 text-gray-700 text-sm">{row.p2}</td>
                    <td className="px-4 py-3 text-gray-700 text-sm">{row.p3}</td>
                    <td className="px-4 py-3 text-gray-700 text-sm">{row.p45}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Container>
      </section>

      {/* Investment Summary */}
      <section className="py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Investment Summary
          </h2>

          {/* Investment Structure Table */}
          <div className="overflow-x-auto mb-8">
            <table className="w-full border border-gray-200">
              <thead className="bg-navy text-white">
                <tr>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Category</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">H1 (Phases 0-2)</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">H2 (Phase 3)</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">H3 (Phases 4-5)</th>
                  <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr className="bg-white hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">Direct Investment</strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">$106K</td>
                  <td className="px-4 py-3 text-gray-700">$31.2K</td>
                  <td className="px-4 py-3 text-gray-700">$25.9K</td>
                  <td className="px-4 py-3 font-bold text-navy">$163.1K</td>
                </tr>
                <tr className="bg-gray-50 hover:bg-gray-100">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">Labor Allocation (5 FTE)</strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">$412.5K</td>
                  <td className="px-4 py-3 text-gray-700">$337.5K</td>
                  <td className="px-4 py-3 text-gray-700">$360K</td>
                  <td className="px-4 py-3 font-bold text-navy">$1,110K</td>
                </tr>
                <tr className="bg-white hover:bg-gray-50">
                  <td className="px-4 py-3 text-gray-700">
                    <strong className="font-semibold text-navy">Total Program Cost</strong>
                  </td>
                  <td className="px-4 py-3 text-gray-700">$518.5K</td>
                  <td className="px-4 py-3 text-gray-700">$368.7K</td>
                  <td className="px-4 py-3 text-gray-700">$385.9K</td>
                  <td className="px-4 py-3 font-bold text-navy">$1,273.1K</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Key Distinction */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <Card className="border-t-4 border-t-emerald-500">
              <h3 className="text-lg font-bold text-navy mb-2">
                Direct Investment
              </h3>
              <p className="text-3xl font-bold text-emerald-600 mb-2">$163.1K</p>
              <p className="text-base text-gray-700">
                Solution-specific costs (infrastructure + training programs). Use this for comparing against alternative solutions (commercial platforms, hybrid approaches).
              </p>
            </Card>
            <Card className="border-t-4 border-t-indigo-500">
              <h3 className="text-lg font-bold text-navy mb-2">
                Labor Allocation
              </h3>
              <p className="text-3xl font-bold text-indigo-600 mb-2">$1,110K</p>
              <p className="text-base text-gray-700">
                Technical staff time required for ANY solution approach (internal build, commercial integration, or hybrid). Constant across solution options.
              </p>
            </Card>
            <Card className="border-t-4 border-t-navy">
              <h3 className="text-lg font-bold text-navy mb-2">
                Total Program Cost
              </h3>
              <p className="text-3xl font-bold text-navy mb-2">$1,273.1K</p>
              <p className="text-base text-gray-700">
                Full organizational investment (Direct + Labor).
              </p>
            </Card>
          </div>

          {/* Component Breakdown */}
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { label: "Infrastructure", value: "$11.1K", detail: "GPU compute, storage, vector database, inference, monitoring" },
              { label: "Training Programs", value: "$152K", detail: "User training, materials development, change management" },
              { label: "Labor Allocation", value: "$1,110K", detail: "5 FTE \u00d7 18 months, 74 FTE-months \u00d7 $15K" },
            ].map((item) => (
              <div key={item.label} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <p className="text-base font-semibold text-navy">{item.label}</p>
                <p className="text-xl font-bold text-navy">{item.value}</p>
                <p className="text-base text-gray-600 mt-1">{item.detail}</p>
              </div>
            ))}
          </div>
        </Container>
      </section>

      {/* Decision Points & ROI */}
      <section className="bg-gray-50 py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Decision Points & ROI
          </h2>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            {[
              {
                decisionPoint: "After Phase 2 (H1)",
                directInvestment: "$106K",
                totalCost: "$518.5K",
                outcome: "Defended/extended core operations",
                decision: "Can stop with core efficiency achieved",
                color: "border-blue-500",
                horizonBg: "bg-blue-50",
                horizonText: "text-blue-700",
              },
              {
                decisionPoint: "After Phase 3 (H2)",
                directInvestment: "$137.2K",
                totalCost: "$887.2K",
                outcome: "Core + competitive advantages",
                decision: "Can stop with proprietary capabilities built",
                color: "border-emerald-500",
                horizonBg: "bg-emerald-50",
                horizonText: "text-emerald-700",
              },
              {
                decisionPoint: "After Phase 5 (H3)",
                directInvestment: "$163.1K",
                totalCost: "$1,273.1K",
                outcome: "Full transformation, innovation capacity",
                decision: "Complete transformation with ongoing innovation",
                color: "border-purple-500",
                horizonBg: "bg-purple-50",
                horizonText: "text-purple-700",
              },
            ].map((option) => (
              <Card key={option.decisionPoint} className={`border-t-4 ${option.color}`}>
                <span className={`inline-block px-2 py-1 rounded text-xs font-bold ${option.horizonBg} ${option.horizonText} mb-3`}>
                  {option.decisionPoint}
                </span>
                <div className="space-y-3">
                  <div>
                    <p className="text-base text-gray-500 uppercase tracking-wide">Direct Investment</p>
                    <p className="text-xl font-bold text-navy">{option.directInvestment}</p>
                  </div>
                  <div>
                    <p className="text-base text-gray-500 uppercase tracking-wide">Total Program Cost</p>
                    <p className="text-lg font-semibold text-gray-700">{option.totalCost}</p>
                  </div>
                  <div>
                    <p className="text-base text-gray-500 uppercase tracking-wide">Outcome</p>
                    <p className="text-base text-gray-700 font-medium">{option.outcome}</p>
                  </div>
                  <div className="pt-3 border-t border-gray-200">
                    <p className="text-base text-gray-700">{option.decision}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          <p className="text-base text-gray-600 text-center">
            ROI calculations based on productivity gains, time savings, and competitive advantage value. Full ROI analysis available in supporting documentation.
          </p>
        </Container>
      </section>

      {/* Implementation Principles */}
      <section className="py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Implementation Principles
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                title: "1. Mission Framing",
                adkar: "ADKAR: Awareness",
                doList: [
                  '"Help more people faster"',
                  '"Access knowledge to support beneficiaries in real-time"',
                ],
                dontList: [
                  '"Increase productivity by 10x"',
                  '"Streamline operations"',
                  '"Digital transformation"',
                ],
                why: "Mission-driven staff resist efficiency messaging; mission framing creates authentic awareness aligned with organizational values.",
              },
              {
                title: "2. Self-Initiated Adoption",
                adkar: "ADKAR: Desire",
                doList: [
                  "Zero mandates, no penalties for non-adoption",
                  "Peer demonstration: early adopters become coaches",
                ],
                dontList: [
                  "No performance review linkage",
                  "No mandated usage targets",
                ],
                why: "Mandates create compliance resistance; self-initiated adoption creates authentic desire aligned with bottom-up culture.",
              },
              {
                title: "3. Embedded Learning",
                adkar: "ADKAR: Knowledge",
                doList: [
                  "Phase 1: Natural language, no prerequisites",
                  "Phase 2: 4-8 hours AI literacy",
                  "Learn by doing: contextual help at point of need",
                ],
                dontList: [
                  "No traditional training burden",
                  "No prerequisite courses",
                ],
                why: "Traditional training burden defeats desire; embedded learning integrates knowledge into actual work.",
              },
              {
                title: "4. Progressive Complexity",
                adkar: "ADKAR: Ability",
                doList: [
                  "Universal (Phase 1: all 8,000)",
                  "Selective (Phase 2: 200-500)",
                  "Advanced (Phase 3: 30-100)",
                  "Expert (Phases 4-5: 15-30)",
                ],
                dontList: [
                  "No one-size-fits-all approach",
                  "No forced advancement",
                ],
                why: "Skill diversity extreme across 8,000 staff in 115 countries; progressive complexity ensures universal access with voluntary advancement.",
              },
              {
                title: "5. Continuous Value",
                adkar: "ADKAR: Reinforcement",
                doList: [
                  "Phase 1: Instant answers",
                  "Phase 2: Time freed",
                  "Phase 3: Work previously impossible",
                  "Phases 4-5: Transformative capabilities",
                ],
                dontList: [
                  "No deferred value",
                  "No all-or-nothing phases",
                ],
                why: "Continuous value reinforces change; transformation self-funds through progressive ROI.",
              },
              {
                title: "6. Internal Build",
                adkar: "Small Models",
                doList: [
                  "Data sovereignty: all models trained internally",
                  "Cost control: small models vs. external APIs",
                  "Proprietary advantages: custom training on institutional knowledge",
                ],
                dontList: [
                  "No external API dependencies",
                  "No vendor lock-in",
                ],
                why: "Maintains control, manages costs, creates defensible competitive advantages.",
              },
            ].map((principle) => (
              <Card key={principle.title}>
                <h3 className="text-lg font-bold text-navy mb-1">
                  {principle.title}
                </h3>
                <p className="text-base text-gray-500 uppercase tracking-wide mb-3">
                  {principle.adkar}
                </p>
                <div className="space-y-2 mb-3">
                  {principle.doList.map((item, i) => (
                    <p key={i} className="text-base text-gray-700">
                      <span className="text-emerald-600 font-bold mr-1">&#10003;</span>
                      {item}
                    </p>
                  ))}
                  {principle.dontList.map((item, i) => (
                    <p key={i} className="text-base text-gray-700">
                      <span className="text-red-500 font-bold mr-1">&#10007;</span>
                      {item}
                    </p>
                  ))}
                </div>
                <p className="text-base text-gray-600 border-t border-gray-200 pt-2">
                  <strong>Why:</strong> {principle.why}
                </p>
              </Card>
            ))}
          </div>
        </Container>
      </section>

      {/* Staffing & User Progression */}
      <section className="bg-gray-50 py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Staffing & User Progression
          </h2>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Staffing Table */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                Technical Staff Allocation
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full border border-gray-200">
                  <thead className="bg-navy text-white">
                    <tr>
                      <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Phase</th>
                      <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">FTE</th>
                      <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Target Users</th>
                      <th scope="col" className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide">Selection</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {[
                      { phase: "Phase 0", fte: "2 FTE", users: "Technical staff", selection: "Initial infrastructure setup" },
                      { phase: "Phase 1", fte: "2.5 FTE avg", users: "All 8,000 staff", selection: "Universal (115 countries, 4 languages)" },
                      { phase: "Phase 2", fte: "3.5 FTE", users: "200-500 division staff", selection: "Self-selected information workers (Kaizen)" },
                      { phase: "Phase 3", fte: "5 FTE (peak)", users: "30-100 advanced users", selection: "15-20% of Phase 2 with specialized needs" },
                      { phase: "Phase 4", fte: "5 FTE (peak)", users: "15-30 expert users", selection: "5-10% of Phase 3, technical sophistication" },
                      { phase: "Phase 5", fte: "3-5 FTE", users: "Phase 4 + 20-30 leaders", selection: "Expert users progressing to orchestration" },
                    ].map((row, i) => (
                      <tr key={row.phase} className={`${i % 2 === 0 ? "bg-white" : "bg-gray-50"} hover:bg-gray-100`}>
                        <td className="px-4 py-3 text-gray-700 font-semibold">{row.phase}</td>
                        <td className="px-4 py-3 text-gray-700">{row.fte}</td>
                        <td className="px-4 py-3 text-gray-700">{row.users}</td>
                        <td className="px-4 py-3 text-gray-700 text-sm">{row.selection}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="mt-4 bg-white rounded-lg border border-gray-200 p-4">
                <p className="text-base font-semibold text-navy mb-2">Labor Allocation Pattern</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>Months 0-6: 2-3.5 FTE (building foundation)</li>
                  <li>Months 7-15: 5 FTE at capacity (overlapping phases)</li>
                  <li>Months 16-18: 3 FTE (orchestrator wrap-up)</li>
                  <li className="font-semibold text-navy">Total: 74 FTE-months over 18 months</li>
                </ul>
              </div>
            </div>

            {/* User Progression Funnel */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                User Progression
              </h3>
              <div className="space-y-3">
                {[
                  { label: "Phase 1: Universal", users: "8,000", width: "100%", color: "bg-blue-500" },
                  { label: "Phase 2: Selective", users: "200-500", width: "50%", color: "bg-blue-500" },
                  { label: "Phase 3: Advanced", users: "30-100", width: "25%", color: "bg-emerald-500" },
                  { label: "Phases 4-5: Expert", users: "15-30", width: "12%", color: "bg-purple-500" },
                ].map((level) => (
                  <div key={level.label}>
                    <div className="flex justify-between text-base mb-1">
                      <span className="font-medium text-gray-700">{level.label}</span>
                      <span className="font-bold text-navy">{level.users}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-6 flex items-center">
                      <div
                        className={`${level.color} h-full rounded-full flex items-center justify-end pr-3`}
                        style={{ width: level.width }}
                      >
                        <span className="text-xs text-white font-medium">{level.users}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 bg-white rounded-lg border border-gray-200 p-4">
                <p className="text-base text-gray-700">
                  <strong className="font-semibold text-navy">Selection model:</strong>{" "}
                  Universal &rarr; Selective &rarr; Advanced &rarr; Expert. Each phase
                  self-selects from the previous phase based on demonstrated interest
                  and capability, not mandated advancement.
                </p>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* Success Factors */}
      <section className="py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Success Factors
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                title: "Change Management Embedded in Design",
                description:
                  "Solution designed from ground up to enable ADKAR progression\u2014not separate \u201ccommunications plan\u201d overlaid on unsuitable solution.",
              },
              {
                title: "Working with Organizational Constraints",
                description:
                  "Mission framing (culture), progressive complexity (8,000 diverse staff, 115 countries), $163.1K Direct Investment vs. $2-7M traditional approaches, decentralized deployment.",
              },
              {
                title: "Internal Build Maintains Control",
                description:
                  "Data sovereignty (no external APIs), cost control (small models), proprietary advantages (custom training).",
              },
              {
                title: "Progressive Investment with Bounded Risk",
                description:
                  "Exit optionality at every horizon boundary. Each phase delivers independent value. Early phases generate ROI that exceeds total investment.",
              },
              {
                title: "Minimal Staff Requirement",
                description:
                  "5 FTE peak (vs. 20-50 traditional transformation teams). No external AI talent recruitment required. Existing staff progressively upskilled. Peer support model.",
              },
            ].map((factor) => (
              <Card key={factor.title} className="border-t-4 border-t-teal">
                <h3 className="text-lg font-bold text-navy mb-2">
                  {factor.title}
                </h3>
                <p className="text-base text-gray-700">{factor.description}</p>
              </Card>
            ))}
          </div>
        </Container>
      </section>

      {/* Summary */}
      <section className="bg-gray-50 py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Summary
          </h2>

          <p className="text-gray-700 leading-relaxed mb-6">
            The Transformation Roadmap provides practical execution from Month
            0 to Month 18 across 6 phases, integrating change management
            principles into solution design.
          </p>

          <Card className="border-l-4 border-l-teal bg-teal/5 mb-6">
            <p className="text-lg font-semibold text-navy mb-2">
              Key Insight
            </p>
            <p className="text-gray-700">
              Change management success requires solution designed for ADKAR
              progression, not ADKAR strategy overlaid on unsuitable solution.
              Mission framing, self-initiated adoption, embedded learning,
              progressive complexity, and continuous value delivery are built
              into phase design&mdash;not added later as &ldquo;change management
              plan.&rdquo;
            </p>
          </Card>

          <p className="text-gray-700 leading-relaxed font-semibold">
            <strong className="font-semibold text-navy">Result:</strong>{" "}
            18-month transformation with $163.1K Direct Investment ($1,273.1K
            total program cost) maintaining data sovereignty, building
            proprietary advantages, and creating sustainable competitive
            advantage&mdash;all while working with (not against) organizational
            constraints.
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
