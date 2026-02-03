import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";

export const metadata: Metadata = {
  title: "Balanced Scorecard - Performance Management Framework",
  description:
    "Integrated performance management framework translating Phased Internal Build strategy into measurable objectives across four interdependent perspectives: Learning & Growth, Internal Process, User & Customer, and Financial",
};

const perspectives = [
  {
    name: "Learning & Growth Perspective: Building Organizational Capability",
    objective:
      "Build internal AI capability progressively without external recruitment, enabling ongoing innovation beyond initial transformation.",
    color: "border-l-teal",
    bg: "bg-white",
    rows: [
      {
        objective: "Universal knowledge access capability",
        measure: "% staff successfully using query capabilities",
        target: "80%+ self-initiated adoption by Month 3",
        initiatives:
          "Phase 1: Multilingual semantic search deployment, embedded learning design, zero training prerequisites",
      },
      {
        objective: "Intermediate automation capability",
        measure: "% Phase 1 users advancing to task automation",
        target: "30-40% voluntary progression by Month 9",
        initiatives:
          "Phase 2: Kaizen discovery workshops, automation design training, process analysis skills",
      },
      {
        objective: "Advanced analytical capability",
        measure: "% Phase 2 users advancing to intelligence",
        target: "15-20% voluntary progression by Month 12",
        initiatives:
          "Phase 3: Division-specific training, MoE concepts, analytical reasoning development",
      },
      {
        objective: "Expert orchestration capability",
        measure:
          "Expert users engaged in discovery and orchestration",
        target: "15-30 experts (Phase 4), 20-30 leaders (Phase 5)",
        initiatives:
          "Phases 4-5: Experimentation workshops, orchestration training, system design development",
      },
      {
        objective: "Internal self-sufficiency",
        measure: "Independent operation without external dependency",
        target: "Achieved by Month 18",
        initiatives:
          "Progressive upskilling across 6 phases, capability compounding, institutional knowledge retention",
      },
    ],
    whyMatters:
      "Learning & Growth is the foundation. Without organizational capability building, internal processes cannot improve, customer value cannot be created, and financial results cannot be sustained. External AI talent recruitment is organizationally impossible ($1.5-3.75M unaffordable, salary competition impossible).",
  },
  {
    name: "Internal Business Process Perspective: Knowledge Transformation",
    objective:
      "Transform trapped institutional knowledge into amplified proprietary competitive advantage through progressive AI capability building.",
    color: "border-l-blue-500",
    bg: "bg-gray-50",
    rows: [
      {
        objective: "Knowledge accessibility",
        measure: "Query success rate across 4 languages",
        target: "90%+ useful responses",
        initiatives:
          "Phase 0: Registry infrastructure, Phase 1: Embedding models, vector database, semantic search",
      },
      {
        objective: "Task automation coverage",
        measure: "% of repetitive work automated",
        target: "50%+ for Phase 2 users",
        initiatives:
          "Phase 2: Task-specific SLMs, LoRA fine-tuning, Kaizen methodology",
      },
      {
        objective: "Intelligence sophistication",
        measure:
          "% of Phase 3 queries requiring multi-step analytical reasoning",
        target: "60%+ of queries demonstrating advanced analytical use",
        initiatives:
          "Phase 3: MoE router architecture, division-specific expert models",
      },
      {
        objective: "Innovation capacity",
        measure:
          "Experiments conducted, patterns discovered, workflows orchestrated",
        target:
          "50+ experiments, 10+ patterns, 10+ workflows by Month 18",
        initiatives:
          "Phase 2: Kaizen discovery (user-identified automation), Phase 3: Advanced analytical use cases, Phases 4-5: Sandboxed experimentation, orchestration",
      },
      {
        objective: "System reliability",
        measure: "Service availability and performance",
        target: "99%+ uptime",
        initiatives:
          "Infrastructure management, monitoring, continuous improvement",
      },
    ],
    whyMatters:
      "Porter\u2019s Five Forces analysis revealed proprietary institutional knowledge is the key defensible competitive advantage. This perspective tracks transformation of trapped knowledge into systematic competitive capability that competitors cannot purchase or replicate.",
  },
  {
    name: "User & Customer Perspective: Internal and External Value Creation",
    objective:
      "Enhance internal user capability and satisfaction while improving external service delivery and preserving client relationships.",
    color: "border-l-emerald-500",
    bg: "bg-white",
    rows: [
      {
        objective: "User satisfaction and confidence",
        measure:
          "Staff satisfaction with AI capabilities, trust in outputs",
        target: "80%+ satisfied users, 90%+ trust AI outputs",
        initiatives:
          "Embedded learning design, reliable performance, continuous improvement based on feedback",
      },
      {
        objective: "User productivity impact",
        measure: "Average time to answer complex knowledge queries",
        target: "10x faster (seconds vs hours/days)",
        initiatives:
          "Phase 1: Universal knowledge access, immediate query capability",
      },
      {
        objective: "Client relationship preservation",
        measure:
          "Client satisfaction score, workflow disruption complaints",
        target:
          "Satisfaction maintained/improved, zero disruption complaints",
        initiatives:
          "Zero workflow disruption design, staff capability enhancement (invisible to clients)",
      },
      {
        objective: "Service quality enhancement",
        measure:
          "Client feedback score on staff responsiveness and capability",
        target: "Baseline +10% improvement by Month 18",
        initiatives:
          "Phases 1-5: Progressive staff capability, more knowledgeable assistance, sophisticated support",
      },
      {
        objective: "Multilingual consistency",
        measure: "Language coverage and parity for users and clients",
        target: "4 languages, 90%+ success rate across all",
        initiatives:
          "Phase 1: English, French, Spanish, Portuguese query capability",
      },
    ],
    whyMatters:
      'Internal users (staff) are the immediate customers of AI capabilities, and their satisfaction drives adoption and effective use. External clients experience the outcomes of empowered staff. Stakeholder requirement S5 ("No disruption to client workflows") is absolute constraint\u2014AI transformation must be invisible to clients while being valuable to staff.',
  },
  {
    name: "Financial Perspective: Cost-Effective Transformation",
    objective:
      "Achieve cost-effective transformation within budget constraints through progressive investment with bounded risk and strategic optionality.",
    color: "border-l-purple-500",
    bg: "bg-gray-50",
    rows: [
      {
        objective: "Investment efficiency",
        measure: "Direct Investment vs alternatives",
        target:
          "$163.1K vs $2-7M alternatives (92-98% reduction)",
        initiatives:
          "Phased internal build: $11.1K infrastructure + $152K training across 6 phases",
      },
      {
        objective: "Time to value",
        measure: "Months until first productivity gains",
        target: "Month 1 (vs 18-48 months for alternatives)",
        initiatives:
          "Phase 1 immediate deployment, quarterly value delivery",
      },
      {
        objective: "Budget compliance",
        measure: "Cumulative spend by phase vs budget",
        target:
          "Within constraints: $62.4K (P1), $106K (P2), $137.2K (P3), $152.7K (P4), $163.1K (P5)",
        initiatives:
          "Progressive investment: $0\u2192$62.4K\u2192$43.6K\u2192$31.2K\u2192$15.5K\u2192$10.4K per phase",
      },
      {
        objective: "Risk management",
        measure: "Maximum investment at risk at any decision point",
        target:
          "<$106K at H1 boundary, <$137.2K at H2 boundary, <$163.1K at H3 boundary",
        initiatives:
          "Exit optionality at each horizon boundary (H1: Month 9, H2: Month 12, H3: Month 18)",
      },
      {
        objective: "Value realization",
        measure: "Phases delivering measurable productivity value",
        target:
          "Value realized by Month 1 (Phase 1), compounding quarterly",
        initiatives:
          "Continuous value delivery funds future phases, quarterly assessment",
      },
    ],
    whyMatters:
      "In crisis conditions (20% revenue decline, 15% cost reduction mandate), financial sustainability is existential. Budget constraints that eliminate vendor platforms ($2-5M) become competitive advantage through progressive investment that generates resources to fund future phases.",
    financialContext: true,
  },
];

const strategyMapBoxes = [
  {
    title: "LEARNING & GROWTH (Foundation)",
    content:
      "Progressive staff upskilling \u2192 Internal capability building \u2192 Self-sufficiency \u2192 Ongoing innovation",
    color: "border-l-teal bg-teal/5",
    arrow: "ENABLES",
  },
  {
    title: "INTERNAL BUSINESS PROCESSES (Transformation)",
    content:
      "Knowledge accessible \u2192 Automated \u2192 Intelligent \u2192 Discovered \u2192 Orchestrated = Proprietary competitive advantage",
    color: "border-l-blue-500 bg-blue-50",
    arrow: "CREATES",
  },
  {
    title: "USER & CUSTOMER VALUE (Delivery)",
    content:
      "Satisfied users + Improved productivity + Enhanced service capability + Preserved client relationships = Mission impact",
    color: "border-l-emerald-500 bg-emerald-50",
    arrow: "GENERATES",
  },
  {
    title: "FINANCIAL RESULTS (Outcomes)",
    content:
      "Cost-effective transformation + Quarterly ROI + Bounded risk + Strategic optionality = Financial sustainability",
    color: "border-l-purple-500 bg-purple-50",
    arrow: "ENABLES",
  },
  {
    title: "CONTINUED LEARNING & GROWTH (Virtuous Cycle)",
    content:
      "Financial sustainability funds continued capability building",
    color: "border-l-teal bg-teal/5",
    arrow: null,
  },
];

const phaseProgression = [
  {
    phase: "Phase 0: Registry Foundation",
    timeline: "Month 0",
    milestone: "Infrastructure established",
    indicator: "All three registries operational",
  },
  {
    phase: "Phase 1: Knowledge Access",
    timeline: "Months 1-3",
    milestone: "Universal capability deployed",
    indicator: "80%+ adoption, 90%+ query success",
  },
  {
    phase: "Phase 2: Task Automation",
    timeline: "Months 4-9",
    milestone: "Selective automation achieved",
    indicator:
      "30-40% Phase 1 users advance, 50%+ task coverage",
  },
  {
    phase: "Phase 3: Division Intelligence",
    timeline: "Months 7-12",
    milestone: "Advanced capability operational",
    indicator:
      "15-20% Phase 2 users advance, MoE functioning",
  },
  {
    phase: "Phase 4: Agentic Discovery",
    timeline: "Months 10-15",
    milestone: "Experimentation and discovery",
    indicator: "50+ experiments, 10+ patterns discovered",
  },
  {
    phase: "Phase 5: Orchestrated System",
    timeline: "Months 13-18",
    milestone: "Full transformation complete",
    indicator:
      "10+ workflows operational, self-sufficiency achieved",
  },
];

export default function BalancedScorecardPage() {
  return (
    <>
      <PageHeader title="Balanced Scorecard Performance Management" />

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
            <span className="text-gray-900">Balanced Scorecard</span>
          </nav>
        </Container>
      </section>

      {/* BLUF Section */}
      <section className="bg-gray-50 py-12">
        <Container size="reading">
          <p className="text-lg text-gray-700 leading-relaxed">
            Measuring only financial results and deployment metrics misses
            capability building that creates sustainable advantage. Balanced
            Scorecard provides early warning system across four perspectives
            (Learning &amp; Growth, Internal Process, User &amp; Customer,
            Financial) with quarterly assessment enabling progression decisions
            at each horizon boundary based on leading indicators, not deferred
            ROI. Progressive measurement transforms 18-month transformation
            from &ldquo;hope for success&rdquo; to &ldquo;prove value quarterly
            before advancing.&rdquo;
          </p>
        </Container>
      </section>

      {/* Why Balanced Scorecard */}
      <section className="py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Why Balanced Scorecard for AI Transformation?
          </h2>
          <p className="text-gray-700 leading-relaxed mb-6">
            Traditional AI implementations measure success primarily through
            financial metrics (ROI, cost savings) or deployment metrics (% staff
            trained, system usage). This creates three critical problems:
            financial results only visible after complete deployment (delayed
            measurement), organizational capability building and user/customer
            impact missed (incomplete picture), and no ability to identify
            problems until failure occurs (no leading indicators).
          </p>
          <p className="text-gray-700 leading-relaxed">
            Balanced Scorecard addresses these problems by providing progressive
            measurement at each phase across four interdependent perspectives
            (Learning &amp; Growth, Internal Process, User &amp; Customer,
            Financial), holistic assessment that captures both leading and
            lagging indicators, and cause-and-effect linkages that predict future
            performance based on current capability building.
          </p>
        </Container>
      </section>

      {/* Four Perspectives */}
      {perspectives.map((perspective) => (
        <section
          key={perspective.name}
          className={`py-16 ${perspective.bg}`}
        >
          <Container size="content">
            <h2 className="text-2xl md:text-3xl font-bold text-navy mb-4">
              {perspective.name}
            </h2>

            <p className="text-lg text-gray-700 mb-8">
              <strong className="font-semibold text-navy">
                Strategic Objective:
              </strong>{" "}
              {perspective.objective}
            </p>

            <div className="overflow-x-auto mb-6">
              <table className="w-full border border-gray-200">
                <thead className="bg-navy text-white">
                  <tr>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Objective
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Measure
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Target
                    </th>
                    <th
                      scope="col"
                      className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                    >
                      Initiatives
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {perspective.rows.map((row, i) => (
                    <tr
                      key={row.objective}
                      className={`${i % 2 === 0 ? "bg-white" : "bg-gray-50"} hover:bg-gray-100`}
                    >
                      <td className="px-4 py-3 text-gray-700">
                        <strong className="font-semibold text-navy">
                          {row.objective}
                        </strong>
                      </td>
                      <td className="px-4 py-3 text-gray-700 text-sm">
                        {row.measure}
                      </td>
                      <td className="px-4 py-3 text-gray-700 text-sm">
                        {row.target}
                      </td>
                      <td className="px-4 py-3 text-gray-700 text-sm">
                        {row.initiatives}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {perspective.financialContext && (
              <Card className="border-l-4 border-l-purple-500 bg-purple-50 mb-6">
                <p className="text-gray-700 text-base">
                  <strong className="font-semibold text-navy">
                    Financial Context (not primary focus):
                  </strong>
                </p>
                <ul className="mt-2 space-y-1 text-gray-700 text-base">
                  <li>
                    <strong>Direct Investment:</strong> $163.1K
                    (solution-specific costs for comparing alternatives)
                  </li>
                  <li>
                    <strong>Total Program Cost:</strong> $1,273.1K (includes
                    $1,110K labor allocation required for any solution)
                  </li>
                  <li>
                    <strong>Key principle:</strong> Financial sustainability
                    through progressive investment, not upfront capital
                    deployment
                  </li>
                </ul>
              </Card>
            )}

            <Card
              className={`border-l-4 ${perspective.color} ${
                perspective.color.includes("teal")
                  ? "bg-teal/5"
                  : perspective.color.includes("blue")
                    ? "bg-blue-50"
                    : perspective.color.includes("emerald")
                      ? "bg-emerald-50"
                      : "bg-purple-50"
              }`}
            >
              <p className="text-gray-700">
                <strong className="font-semibold text-navy">
                  Why This Matters:
                </strong>{" "}
                {perspective.whyMatters}
              </p>
            </Card>
          </Container>
        </section>
      ))}

      {/* Strategy Map */}
      <section className="bg-gray-50 py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Strategy Map: Cause-and-Effect Linkages
          </h2>

          <p className="text-gray-700 mb-8">
            The Balanced Scorecard perspectives are causally
            connected&mdash;success in one perspective enables success in the
            next:
          </p>

          <div className="bg-white p-8 rounded-lg shadow-sm">
            <div className="space-y-2">
              {strategyMapBoxes.map((box, index) => (
                <div key={index}>
                  <Card className={`border-l-4 ${box.color} p-6`}>
                    <h3 className="font-bold text-navy mb-2">{box.title}</h3>
                    <p className="text-gray-700 text-base">{box.content}</p>
                  </Card>
                  {box.arrow && (
                    <div className="flex justify-center my-2">
                      <span className="text-base text-gray-500 font-semibold">
                        &darr; {box.arrow}
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </Container>
      </section>

      {/* Progressive Measurement */}
      <section className="py-16 bg-white">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Progressive Measurement Across Phases
          </h2>

          <p className="text-gray-700 mb-8">
            While the Balanced Scorecard is a single integrated view,
            measurement occurs progressively across 6 phases (0-5) over 18
            months:
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
                    Key Milestone
                  </th>
                  <th
                    scope="col"
                    className="px-4 py-3 text-left text-sm font-semibold uppercase tracking-wide"
                  >
                    Success Indicator
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {phaseProgression.map((phase, i) => (
                  <tr
                    key={phase.phase}
                    className={`${i % 2 === 0 ? "bg-white" : "bg-gray-50"} hover:bg-gray-100`}
                  >
                    <td className="px-4 py-3 text-gray-700">
                      <strong className="font-semibold text-navy">
                        {phase.phase}
                      </strong>
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      {phase.timeline}
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      {phase.milestone}
                    </td>
                    <td className="px-4 py-3 text-gray-700">
                      {phase.indicator}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <Card className="border-l-4 border-l-teal bg-teal/5">
            <h3 className="font-bold text-navy mb-3">
              Measurement Approach:
            </h3>
            <ul className="space-y-2 text-gray-700 text-base">
              <li>
                <strong>Quarterly assessments</strong> at phase boundaries
              </li>
              <li>
                <strong>All four perspectives measured</strong> each quarter
              </li>
              <li>
                <strong>Leading indicators</strong> (Learning &amp; Growth,
                Internal Process) predict lagging indicators (Customer,
                Financial)
              </li>
              <li>
                <strong>Progression decision points</strong> at horizon
                boundaries (H1: Month 9, H2: Month 12, H3: Month 18)
              </li>
            </ul>
          </Card>
        </Container>
      </section>

      {/* Integration Section */}
      <section className="bg-gray-50 py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Connection to Other Section 4 Frameworks
          </h2>

          <div className="space-y-8">
            {/* Integration with Three Horizons */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                Integration with Three Horizons Framework
              </h3>
              <p className="text-gray-700 mb-4">
                Balanced Scorecard metrics align with Three Horizons strategic
                timing:
              </p>

              <div className="grid md:grid-cols-3 gap-6">
                <Card className="border-t-4 border-t-blue-500">
                  <h4 className="font-bold text-navy mb-2">
                    Horizon 1 (Defend Core)
                  </h4>
                  <p className="text-base text-gray-600 mb-2">
                    Phases 0-2, Months 0-9
                  </p>
                  <p className="text-base text-gray-700 mb-1">
                    <strong>Focus:</strong> Financial sustainability + Customer
                    preservation
                  </p>
                  <p className="text-base text-gray-700">
                    <strong>Scorecard emphasis:</strong> Time to value, adoption
                    rates, relationship preservation
                  </p>
                </Card>
                <Card className="border-t-4 border-t-emerald-500">
                  <h4 className="font-bold text-navy mb-2">
                    Horizon 2 (Build Emerging)
                  </h4>
                  <p className="text-base text-gray-600 mb-2">
                    Phase 3, Months 7-12
                  </p>
                  <p className="text-base text-gray-700 mb-1">
                    <strong>Focus:</strong> Internal Process transformation +
                    Advanced capability
                  </p>
                  <p className="text-base text-gray-700">
                    <strong>Scorecard emphasis:</strong> Intelligence
                    sophistication, competitive advantage building
                  </p>
                </Card>
                <Card className="border-t-4 border-t-purple-500">
                  <h4 className="font-bold text-navy mb-2">
                    Horizon 3 (Create Transformative)
                  </h4>
                  <p className="text-base text-gray-600 mb-2">
                    Phases 4-5, Months 10-18
                  </p>
                  <p className="text-base text-gray-700 mb-1">
                    <strong>Focus:</strong> Organizational capability +
                    Sustainable advantage
                  </p>
                  <p className="text-base text-gray-700">
                    <strong>Scorecard emphasis:</strong> Innovation capacity,
                    self-sufficiency, ongoing improvement
                  </p>
                </Card>
              </div>
            </div>

            {/* Integration with Transformation Roadmap */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                Integration with Transformation Roadmap
              </h3>
              <p className="text-gray-700 mb-4">
                Transformation Roadmap (integrated execution + ADKAR change
                management) informs Balanced Scorecard:
              </p>
              <ul className="space-y-2 text-gray-700 mb-4">
                <li>
                  <strong>Resource planning</strong> &rarr; Learning &amp; Growth
                  and Financial metrics
                </li>
                <li>
                  <strong>ADKAR integration</strong> &rarr; All four perspectives
                  measure change effectiveness
                </li>
                <li>
                  <strong>Phase execution</strong> &rarr; Progressive milestone
                  tracking
                </li>
                <li>
                  <strong>Investment structure</strong> &rarr; Financial
                  perspective targets
                </li>
              </ul>
              <p className="text-gray-700">
                Balanced Scorecard results inform Roadmap execution decisions
                (resource allocation, phase timing, adoption strategy).
              </p>
              <div className="flex flex-wrap gap-4 mt-6">
                <Link
                  href="/transformation/three-horizons"
                  className="inline-flex items-center text-teal hover:text-teal/80 font-semibold"
                >
                  View Three Horizons Framework &rarr;
                </Link>
                <Link
                  href="/transformation/roadmap"
                  className="inline-flex items-center text-teal hover:text-teal/80 font-semibold"
                >
                  View Transformation Roadmap &rarr;
                </Link>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* Summary */}
      <section className="py-16 bg-white">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8 text-center">
            Summary
          </h2>

          <p className="text-gray-700 leading-relaxed mb-6">
            The Balanced Scorecard translates Phased Internal Build strategy
            into a single integrated performance management framework with
            measurable objectives, metrics, targets, and initiatives across four
            interdependent perspectives.
          </p>

          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-bold text-navy mb-3">
                The Strategic Value
              </h3>
              <p className="text-gray-700 leading-relaxed">
                Balanced Scorecard is not just performance
                measurement&mdash;it is strategy translation (abstract strategy
                becomes concrete objectives), progressive assessment (measure at
                each phase, not just end-state), risk management (early warning
                system through four-perspective monitoring), strategic
                optionality (data-driven progression decisions at horizon
                boundaries), continuous improvement (learning organization
                framework), and stakeholder communication (demonstrates progress
                across all dimensions).
              </p>
            </div>

            <div>
              <h3 className="text-xl font-bold text-navy mb-3">
                The Competitive Advantage
              </h3>
              <p className="text-gray-700 leading-relaxed">
                Organizations measuring only financial results miss the
                capability building that creates sustainable advantage. Balanced
                Scorecard ensures Learning &amp; Growth and Internal Process
                perspectives are measured, tracked, and improved&mdash;these are
                the sources of proprietary competitive advantage that competitors
                cannot purchase or replicate.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-bold text-navy mb-3">
                The Integration
              </h3>
              <p className="text-gray-700 leading-relaxed">
                Balanced Scorecard integrates with Three Horizons Framework
                (strategic timing across 3 horizons) and Transformation Roadmap
                (integrated execution + change management) to create
                comprehensive strategy execution framework. Together, these
                three frameworks ensure Phased Internal Build succeeds not just
                in design, but in execution and sustained performance.
              </p>
            </div>
          </div>

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
