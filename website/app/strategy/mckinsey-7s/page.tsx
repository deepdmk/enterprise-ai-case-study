import type { Metadata } from "next";
import Link from "next/link";
import { PageHeader } from "@/components/layout";
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { McKinsey7SVisual } from "./McKinsey7SVisual";

export const metadata: Metadata = {
  title: "McKinsey 7S Framework Analysis - Organizational Assessment",
  description:
    "McKinsey 7S organizational assessment of an International Project Services Enterprise across seven elements: Strategy, Structure, Systems, Style, Staff, Skills, and Shared Values",
};

export default function McKinsey7SPage() {
  return (
    <>
      <PageHeader title="McKinsey 7S Framework Analysis" />

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
            <span className="text-gray-900">McKinsey 7S</span>
          </nav>
        </Container>
      </section>

      {/* Overview */}
      <section className="bg-gray-50 py-12">
        <Container size="reading">
          <h2 className="text-2xl font-bold text-navy mb-4">
            Organizational Assessment
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed mb-4">
            This McKinsey 7S analysis assessed an International Project Services
            Enterprise ($1.3B revenue, 8,000 employees, 115+ countries) to
            understand organizational characteristics, interdependencies, and
            alignment across seven organizational elements.
          </p>
          <p className="text-gray-700 leading-relaxed">
            <strong>Conducted after Porter&apos;s Five Forces competitive analysis, before strategy design.</strong>
          </p>
        </Container>
      </section>

      {/* Organizational Context */}
      <section className="py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            The Organizational Context
          </h2>

          <div className="space-y-4 text-gray-700 leading-relaxed">
            <p>
              <strong className="text-navy">Enterprise Profile:</strong>{" "}
              International Project Services Enterprise operating across 115+
              countries with decentralized structure. $1.3B revenue, 8,000
              employees, four working languages (English, French, Spanish,
              Portuguese).
            </p>
            <p>
              <strong className="text-navy">Recent History:</strong> 25% staff
              reductions during sectoral crisis. Failed ERP and logistics system
              implementations. Revenue decline creating resource constraints.
              Organizational stress and change fatigue.
            </p>
            <p>
              <strong className="text-navy">Assessment Imperative:</strong>{" "}
              Before designing transformation strategy, must understand what
              organizational characteristics enable or constrain execution.
            </p>
          </div>
        </Container>
      </section>

      {/* Element 1: Strategy */}
      <section className="py-16 bg-gray-50">
        <Container size="content">
          <div className="mb-2">
            <span className="inline-block bg-blue-500 text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
              Hard Element
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Element 1: Strategy (with SWOT Analysis)
          </h2>

          <Card className="mb-8">
            <h3 className="text-lg font-bold text-navy mb-3">
              Assessment Questions
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                &bull; What is our competitive position and how do we currently
                compete?
              </li>
              <li>
                &bull; What are our internal strengths and weaknesses?
              </li>
              <li>
                &bull; What external opportunities and threats do we face?
              </li>
              <li>&bull; What strategic assets do we possess?</li>
              <li>
                &bull; What resource constraints limit our strategic options?
              </li>
            </ul>
          </Card>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What We Found
              </h3>

              <h4 className="text-lg font-semibold text-navy mb-2">
                Competitive Position
              </h4>
              <p className="text-gray-700 leading-relaxed mb-6">
                Institutional knowledge accumulated across 115 countries and
                decades represents primary competitive asset. However, this
                knowledge is currently trapped in expert silos, inaccessible at
                organizational scale. Deep domain expertise exists but cannot be
                leveraged effectively.
              </p>

              <h4 className="text-lg font-semibold text-navy mb-4">
                SWOT Analysis
              </h4>

              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <Card className="border-l-4 border-l-green-500 bg-green-50">
                  <h5 className="font-bold text-green-800 mb-3">
                    Strengths (Internal)
                  </h5>
                  <ul className="space-y-2 text-gray-700 text-base">
                    <li>
                      &bull; Institutional knowledge spanning 115 countries and
                      decades of operations
                    </li>
                    <li>
                      &bull; Established client relationships and trust built
                      over time
                    </li>
                    <li>
                      &bull; Multi-cultural organization with localized staff in
                      target countries and regions
                    </li>
                    <li>
                      &bull; Mission-driven workforce creating intrinsic
                      motivation
                    </li>
                    <li>
                      &bull; Decentralized structure enabling local adaptation
                    </li>
                  </ul>
                </Card>

                <Card className="border-l-4 border-l-red-500 bg-red-50">
                  <h5 className="font-bold text-red-800 mb-3">
                    Weaknesses (Internal)
                  </h5>
                  <ul className="space-y-2 text-gray-700 text-base">
                    <li>
                      &bull; Institutional knowledge trapped in silos,
                      organizationally inaccessible
                    </li>
                    <li>
                      &bull; Severe budget constraints (&lt;$1M available for
                      transformation initiatives)
                    </li>
                    <li>
                      &bull; Change-fatigued workforce following layoffs and
                      failed transformations
                    </li>
                    <li>
                      &bull; AI talent not integrated into sector workforce or
                      given organizational attention; recruitment expensive
                    </li>
                    <li>
                      &bull; Technical skills exist but uptake is slower;
                      traditional-skills prioritized in hiring and operations
                    </li>
                  </ul>
                </Card>

                <Card className="border-l-4 border-l-blue-500 bg-blue-50">
                  <h5 className="font-bold text-blue-800 mb-3">
                    Opportunities (External)
                  </h5>
                  <ul className="space-y-2 text-gray-700 text-base">
                    <li>
                      &bull; AI technology enables knowledge amplification at
                      scale
                    </li>
                    <li>
                      &bull; Efficiency improvements possible through better
                      knowledge accessibility
                    </li>
                    <li>
                      &bull; Competitors vulnerable where knowledge scale
                      matters
                    </li>
                    <li>
                      &bull; Stakeholders supportive of innovation that
                      demonstrates clear value
                    </li>
                    <li>
                      &bull; Progressive approaches avoid large upfront capital
                      requirements
                    </li>
                  </ul>
                </Card>

                <Card className="border-l-4 border-l-amber bg-amber/5">
                  <h5 className="font-bold text-amber-800 mb-3">
                    Threats (External)
                  </h5>
                  <ul className="space-y-2 text-gray-700 text-base">
                    <li>
                      &bull; New entrants using AI to overcome institutional
                      knowledge barriers
                    </li>
                    <li>
                      &bull; Vendor platforms could commoditize our competitive
                      capabilities
                    </li>
                    <li>
                      &bull; Competitive intensity increasing with encroachment
                      by other established competitors in resource-constrained
                      environment
                    </li>
                    <li>
                      &bull; Client/funder price sensitivity and efficiency
                      expectations rising
                    </li>
                    <li>
                      &bull; AI talent expensive and not integrated into sector;
                      requires investment in recruitment and development
                    </li>
                  </ul>
                </Card>
              </div>

              <div className="space-y-4 mb-6">
                <p className="text-gray-700 leading-relaxed">
                  <strong className="text-navy">Strategic Assets:</strong> Deep
                  domain expertise, 115-country operational knowledge,
                  multi-cultural and localized operational capabilities,
                  established client relationships across diverse contexts.
                </p>
                <p className="text-gray-700 leading-relaxed">
                  <strong className="text-navy">Resource Constraints:</strong>{" "}
                  Severe budget limitations. AI talent expensive and not
                  integrated into sector workforce. Must build with existing
                  staff capabilities and progressive skill development.
                </p>
              </div>
            </div>

            <Card className="border-l-4 border-l-purple-500 bg-purple-50">
              <h3 className="text-lg font-bold text-navy mb-3">
                Interdependencies with Other Elements
              </h3>
              <ul className="space-y-3 text-gray-700">
                <li>
                  <strong>Strategy &harr; Skills:</strong> Institutional
                  knowledge (strategic asset) trapped because Skills element
                  shows experts won&apos;t document knowledge and expertise
                  exists in relationship networks, not systems.
                </li>
                <li>
                  <strong>Strategy &harr; Staff:</strong> Resource constraints
                  align with Staff reality (cannot attract premium talent, must
                  work with existing workforce capabilities).
                </li>
                <li>
                  <strong>Strategy &harr; Structure:</strong> Decentralized
                  structure means competitive advantage must be buildable and
                  accessible across 115 autonomous country offices, not just at
                  headquarters.
                </li>
              </ul>
            </Card>
          </div>
        </Container>
      </section>

      {/* Element 2: Structure */}
      <section className="py-16">
        <Container size="content">
          <div className="mb-2">
            <span className="inline-block bg-blue-500 text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
              Hard Element
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Element 2: Structure
          </h2>

          <Card className="mb-8">
            <h3 className="text-lg font-bold text-navy mb-3">
              Assessment Questions
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>&bull; How is the organization structured?</li>
              <li>
                &bull; Where does decision-making authority reside?
              </li>
              <li>
                &bull; What is headquarters&apos; role versus country office
                autonomy?
              </li>
              <li>
                &bull; How much coordination capability exists across the
                enterprise?
              </li>
            </ul>
          </Card>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What We Found
              </h3>

              <div className="space-y-6 text-gray-700 leading-relaxed">
                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Structural Model
                  </h4>
                  <p>
                    115 decentralized country offices with substantial
                    operational autonomy. Country directors control local
                    operations, prioritize local needs, have limited
                    accountability to headquarters directives.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Decision-Making
                  </h4>
                  <p>
                    Decentralized with multiple layers. Country directors make
                    operational decisions based on local context, not
                    headquarters priorities. Regional offices sit between
                    headquarters and country offices, providing another layer of
                    decentralization. Much traditional support comes from
                    regions, not headquarters. Local autonomy highly valued.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Headquarters Role
                  </h4>
                  <p>
                    Strategic direction and high-level support, but limited
                    operational authority. Multiple checks on headquarters
                    authority through regional and country office autonomy.
                    Cannot mandate country-level implementation or compliance.
                    Regional offices provide substantial operational support
                    traditionally.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Coordination Capacity
                  </h4>
                  <p>
                    Minimal ability to coordinate enterprise-wide initiatives.
                    Country offices operate semi-independently across different
                    time zones, regulatory environments, cultural contexts.
                    Enterprise-wide synchronized rollouts organizationally
                    infeasible.
                  </p>
                </div>
              </div>
            </div>

            <Card className="border-l-4 border-l-purple-500 bg-purple-50">
              <h3 className="text-lg font-bold text-navy mb-3">
                Interdependencies with Other Elements
              </h3>
              <ul className="space-y-3 text-gray-700">
                <li>
                  <strong>Structure &harr; Style:</strong> Decentralized
                  structure reinforces bottom-up style - headquarters cannot
                  mandate because structure doesn&apos;t provide authority to do
                  so.
                </li>
                <li>
                  <strong>Structure &harr; Systems:</strong> Decentralized
                  structure means systems must be accessible independently by
                  each country office without requiring central coordination or
                  dependencies.
                </li>
                <li>
                  <strong>Structure &harr; Staff:</strong> Multi-layered
                  decentralization (HQ &rarr; Regional &rarr; Country offices)
                  means workforce experiences organizational reality locally,
                  not through headquarters lens. Change must deliver value and
                  benefit at every level - cannot accumulate benefits only at
                  higher levels while imposing costs on lower levels. Change
                  must work office-by-office.
                </li>
                <li>
                  <strong>Strength becoming weakness:</strong> Decentralized
                  structure enables local responsiveness (strength) but prevents
                  coordinated enterprise-wide initiatives (weakness). Cannot
                  leverage organizational scale for transformation if approach
                  requires centralized coordination.
                </li>
              </ul>
            </Card>
          </div>
        </Container>
      </section>

      {/* Element 3: Systems */}
      <section className="py-16 bg-gray-50">
        <Container size="content">
          <div className="mb-2">
            <span className="inline-block bg-blue-500 text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
              Hard Element
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Element 3: Systems
          </h2>

          <Card className="mb-8">
            <h3 className="text-lg font-bold text-navy mb-3">
              Assessment Questions
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                &bull; What formal systems exist (measurement, performance
                management, resource allocation)?
              </li>
              <li>
                &bull; What informal systems exist (meeting formats, conflict
                resolution)?
              </li>
              <li>
                &bull; What is the precedent from previous system
                implementations?
              </li>
              <li>&bull; What technology adoption patterns exist?</li>
              <li>&bull; What language requirements do systems have?</li>
            </ul>
          </Card>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What We Found
              </h3>

              <div className="space-y-6 text-gray-700 leading-relaxed">
                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Technology Precedent
                  </h4>
                  <p>
                    One recent major transformation failure integrating both ERP
                    and logistics systems following pattern: long deployment
                    timelines, mandatory training, workflow disruption,
                    unfulfilled promises, eventual abandonment. Systems were
                    unevenly deployed with different regions and offices at
                    different stages of deployment. Deep organizational memory of
                    &ldquo;headquarters technology initiatives&rdquo; failing.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    System Association
                  </h4>
                  <p>
                    Staff associate new systems with these failures. &ldquo;We&apos;ve
                    seen this before&rdquo; skepticism. Trust damaged by systems
                    that disrupted work without delivering promised value.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Operational Reality
                  </h4>
                  <p>
                    Staff operationally consumed, running lean post-layoffs.
                    Limited capacity to absorb training, workflow disruption, or
                    learning curves. Need systems that enhance existing work
                    immediately, not create additional burden.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Language Requirements
                  </h4>
                  <p>
                    Four organizational languages (English, French, Spanish,
                    Portuguese). 60% of workforce non-English speaking.
                    English-only systems exclude majority of staff, create
                    adoption barriers.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Current Systems
                  </h4>
                  <p>
                    Relational culture, not process culture. Most systems and
                    processes are localized and undocumented. Systems rely
                    heavily on individual knowledge and relationships to work and
                    be maintained. Measurement and resource allocation systems
                    exist but technology systems viewed with skepticism. Informal
                    relational systems often more effective than formal documented
                    systems.
                  </p>
                </div>
              </div>
            </div>

            <Card className="border-l-4 border-l-purple-500 bg-purple-50">
              <h3 className="text-lg font-bold text-navy mb-3">
                Interdependencies with Other Elements
              </h3>
              <ul className="space-y-3 text-gray-700">
                <li>
                  <strong>Systems &harr; Staff:</strong> Failed systems
                  precedent creates staff skepticism and change fatigue. Staff
                  capacity limited - cannot absorb systems requiring extensive
                  training or creating operational burden.
                </li>
                <li>
                  <strong>Systems &harr; Skills:</strong> Current systems
                  don&apos;t capture institutional knowledge. Expertise remains
                  in relationship networks, not documented in accessible systems.
                </li>
                <li>
                  <strong>Systems &harr; Style:</strong> Previous top-down
                  system mandates failed. Informal peer-to-peer systems
                  (relationship networks) often work better than formal
                  headquarters-imposed systems.
                </li>
                <li>
                  <strong>Systems &harr; Shared Values:</strong> Mission-driven
                  culture rejected systems emphasizing
                  efficiency/standardization over mission impact.
                  Corporate-style system implementations felt alien to
                  organizational identity.
                </li>
                <li>
                  <strong>Misalignment creating weakness:</strong> Organization
                  needs better systems to scale knowledge (weakness) but systems
                  precedent creates resistance (making system improvements
                  difficult to implement).
                </li>
              </ul>
            </Card>
          </div>
        </Container>
      </section>

      {/* Element 4: Style */}
      <section className="py-16">
        <Container size="content">
          <div className="mb-2">
            <span className="inline-block bg-orange-500 text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
              Soft Element
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Element 4: Style
          </h2>

          <Card className="mb-8">
            <h3 className="text-lg font-bold text-navy mb-3">
              Assessment Questions
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                &bull; How do leaders and employees behave internally and
                externally?
              </li>
              <li>
                &bull; Where does real influence come from - formal authority or
                peer networks?
              </li>
              <li>&bull; How are decisions actually made?</li>
              <li>
                &bull; What is the cultural response to top-down directives?
              </li>
            </ul>
          </Card>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What We Found
              </h3>

              <div className="space-y-6 text-gray-700 leading-relaxed">
                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Cultural Style
                  </h4>
                  <p>
                    Bottom-up, relational, peer-driven. Decisions emerge through
                    trust networks and peer influence, not through headquarters
                    directives or formal authority. Culture very much
                    consensus-driven rather than mandate-driven.
                    &ldquo;Forgiveness is better than permission&rdquo; cultural
                    norm - staff act and adjust rather than wait for approval.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Personality-Centric Organization
                  </h4>
                  <p>
                    Strong personality centricity with many systems, units, and
                    processes designed around specific people and their ideas
                    rather than around abstract systems, structure, or strategy.
                    Organizational processes reflect &ldquo;how this person does
                    things&rdquo; more than standardized best practices.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Influence Patterns
                  </h4>
                  <p>
                    Real influence flows through peer relationships. Country
                    directors trust other country directors. Staff trust local
                    colleagues. Headquarters communications carry limited weight
                    compared to peer validation.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Response to Mandates
                  </h4>
                  <p>
                    Top-down directives trigger reflexive resistance or
                    compliance theater (appearing to adopt while not actually
                    using). Cannot compel genuine adoption through authority.
                    Staff view mandates with skepticism, especially post-layoffs
                    when trust eroded. Consensus-driven culture means mandates
                    fundamentally misaligned with how decisions actually happen.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Decision Culture
                  </h4>
                  <p>
                    Staff expect to choose adoption based on peer validation and
                    demonstrated value, not because they&apos;re told to comply.
                    &ldquo;Show me it works for people I trust&rdquo; more
                    persuasive than &ldquo;headquarters says you must.&rdquo;
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Leadership Style
                  </h4>
                  <p>
                    Collaborative, relationship-focused. Leaders effective when
                    working through peer networks, not when directing from
                    authority.
                  </p>
                </div>
              </div>
            </div>

            <Card className="border-l-4 border-l-purple-500 bg-purple-50">
              <h3 className="text-lg font-bold text-navy mb-3">
                Interdependencies with Other Elements
              </h3>
              <ul className="space-y-3 text-gray-700">
                <li>
                  <strong>Style &harr; Structure:</strong> Bottom-up style
                  perfectly aligned with decentralized structure. Both reinforce
                  local autonomy and peer-driven decision-making.
                </li>
                <li>
                  <strong>Style &harr; Systems:</strong> Top-down system
                  implementations failed because style is bottom-up. Systems
                  succeed when adopted through self-initiated peer demonstration,
                  fail when mandated.
                </li>
                <li>
                  <strong>Style &harr; Staff:</strong> Relational style aligns
                  with mission-driven staff who value trust and collaboration
                  over mandate compliance.
                </li>
                <li>
                  <strong>Style &harr; Shared Values:</strong> Bottom-up,
                  relational style directly reflects shared values (trust-based
                  collaboration, respect for local contexts, non-corporate
                  identity).
                </li>
                <li>
                  <strong>Strong alignment creating strength:</strong> Style,
                  Structure, and Shared Values strongly aligned around
                  bottom-up, relational, decentralized approach. This alignment
                  creates powerful organizational strength when leveraged, but
                  also makes top-down approaches organizationally impossible.
                </li>
              </ul>
            </Card>
          </div>
        </Container>
      </section>

      {/* Element 5: Staff */}
      <section className="py-16 bg-gray-50">
        <Container size="content">
          <div className="mb-2">
            <span className="inline-block bg-orange-500 text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
              Soft Element
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Element 5: Staff
          </h2>

          <Card className="mb-8">
            <h3 className="text-lg font-bold text-navy mb-3">
              Assessment Questions
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                &bull; What is the workforce state (morale, capacity,
                readiness)?
              </li>
              <li>
                &bull; What demographics and language profile exists?
              </li>
              <li>&bull; What motivates staff?</li>
              <li>&bull; What is staff capacity for change?</li>
              <li>&bull; What skills does the workforce possess?</li>
            </ul>
          </Card>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What We Found
              </h3>

              <div className="space-y-6 text-gray-700 leading-relaxed">
                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Workforce State
                  </h4>
                  <p>
                    Change-fatigued following layoffs, failed systems, revenue
                    decline. Emotionally exhausted, operationally consumed,
                    skeptical of &ldquo;headquarters initiatives.&rdquo; Trust
                    eroded by recent organizational trauma.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Demographics
                  </h4>
                  <p>
                    90% of workforce are non-native English speakers living
                    outside of the US. Globally distributed with staff embedded
                    in local contexts across 115 countries.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Language Profile
                  </h4>
                  <p>
                    Multilingual workforce (40% English, 60%
                    French/Spanish/Portuguese as primary working language).
                    Cross-linguistic collaboration currently limited by language
                    barriers. Four-language capability is organizational strength
                    but also complexity.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Motivation Profile
                  </h4>
                  <p>
                    Mission-driven (joined for social impact, not compensation).
                    Below-market pay offset by mission alignment and previously
                    stable employment. Intrinsically motivated by meaningful
                    work, not responsive to extrinsic incentives or performance
                    pressure. Upheaval eroded stability value proposition.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Change Capacity
                  </h4>
                  <p>
                    Limited remaining capacity for change. Running lean
                    post-layoffs with increased workloads. Cannot absorb
                    additional burden without removing existing work. Require
                    immediate value to justify time investment in anything new.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Skills Profile
                  </h4>
                  <p>
                    Traditional project management skills. Strong relationship
                    management, contextual adaptation, cross-cultural
                    capability. Limited technical sophistication - some staff
                    uncomfortable with new technology. Need simple, accessible
                    approaches that build on existing strengths.
                  </p>
                </div>
              </div>
            </div>

            <Card className="border-l-4 border-l-purple-500 bg-purple-50">
              <h3 className="text-lg font-bold text-navy mb-3">
                Interdependencies with Other Elements
              </h3>
              <ul className="space-y-3 text-gray-700">
                <li>
                  <strong>Staff &harr; Systems:</strong> Change-fatigued staff
                  resist systems requiring training burden or adding work before
                  delivering value. Failed systems precedent reinforces staff
                  skepticism.
                </li>
                <li>
                  <strong>Staff &harr; Style:</strong> Mission-driven staff
                  respond to bottom-up, values-aligned approaches. Resistant to
                  top-down mandates or corporate performance pressure.
                </li>
                <li>
                  <strong>Staff &harr; Skills:</strong> Staff possess strong
                  traditional skills (relationships, adaptation) but limited
                  technical skills. Any approach must build on existing strengths
                  rather than requiring capabilities staff don&apos;t have.
                </li>
                <li>
                  <strong>Staff &harr; Shared Values:</strong> Mission-driven
                  motivation aligns with mission-driven values. Staff engage
                  authentically when initiatives framed around mission impact,
                  resist when framed as corporate efficiency.
                </li>
                <li>
                  <strong>Misalignment creating constraint:</strong> Staff
                  motivation is strength (mission-driven = intrinsic commitment)
                  but change fatigue is weakness (limited capacity for change).
                  Any approach must respect this tension - leverage motivation
                  while respecting capacity limits.
                </li>
              </ul>
            </Card>
          </div>
        </Container>
      </section>

      {/* Element 6: Skills */}
      <section className="py-16">
        <Container size="content">
          <div className="mb-2">
            <span className="inline-block bg-orange-500 text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
              Soft Element
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Element 6: Skills
          </h2>

          <Card className="mb-8">
            <h3 className="text-lg font-bold text-navy mb-3">
              Assessment Questions
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                &bull; What capabilities and competencies exist in the
                organization?
              </li>
              <li>
                &bull; Where does institutional knowledge reside?
              </li>
              <li>&bull; How is knowledge shared or accessed?</li>
              <li>
                &bull; What is expert behavior around knowledge documentation?
              </li>
              <li>&bull; What technical capabilities exist?</li>
            </ul>
          </Card>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What We Found
              </h3>

              <div className="space-y-6 text-gray-700 leading-relaxed">
                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Knowledge Assets
                  </h4>
                  <p>
                    Deep institutional knowledge accumulated over decades across
                    115 countries. Expertise in complex project contexts, diverse
                    regulatory environments, cultural adaptation, relationship
                    management across varied stakeholder types.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Knowledge Problem
                  </h4>
                  <p className="mb-3">
                    Expertise trapped in silos due to lack of processes,
                    databases, and systems. Countries and regions very siloed -
                    not even strong sharing across organizational units when
                    people in same areas are not directly in contact. Learning
                    and knowledge transfer are relational (happens through
                    people networks) not systemic (through documented processes
                    or databases).
                  </p>
                  <p className="mb-3">
                    How and where to access data, expertise, and institutional
                    knowledge depends on relational people networks and
                    knowledge in people&apos;s heads. &ldquo;Who do I ask about
                    X?&rdquo; rather than &ldquo;Where do I look for information
                    on X?&rdquo; This relational knowledge access was
                    drastically affected by the staff losses - when key people
                    left, access to knowledge areas disappeared.
                  </p>
                  <p>
                    Not primarily a language barrier issue (though that exists) -
                    even within same language groups, knowledge siloed by
                    geographic unit, relationship network, and individual expert
                    location.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Expert Reality
                  </h4>
                  <p>
                    Experts operationally busy, protective of valuable
                    knowledge, resistant to documentation burden. See knowledge
                    as personal value and job security. Will not voluntarily
                    document knowledge that took years to acquire - it&apos;s
                    &ldquo;how things work here&rdquo; tacit knowledge, not
                    easily documented. Documentation requests viewed as creating
                    work without benefit to expert.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Knowledge Sharing
                  </h4>
                  <p>
                    Happens through relationships and networks, not formal
                    systems. If you know the right person to ask, you can access
                    expertise. If you don&apos;t, the knowledge is inaccessible.
                    Relationship-based knowledge access works locally but
                    doesn&apos;t scale organizationally.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Skill Development Capacity
                  </h4>
                  <p>
                    Traditional-skills workforce. Cannot rapidly develop
                    sophisticated technical skills. Need progressive building on
                    existing capabilities. Cannot handle sudden technical
                    complexity requirements. Strong at relationship-based work,
                    weaker at technology-based work.
                  </p>
                </div>
              </div>
            </div>

            <Card className="border-l-4 border-l-purple-500 bg-purple-50">
              <h3 className="text-lg font-bold text-navy mb-3">
                Interdependencies with Other Elements
              </h3>
              <ul className="space-y-3 text-gray-700">
                <li>
                  <strong>Skills &harr; Strategy:</strong> Institutional
                  knowledge is strategic asset (SWOT strength) but trapped state
                  makes it unusable competitive advantage. Cannot leverage
                  strategic asset that&apos;s organizationally inaccessible.
                </li>
                <li>
                  <strong>Skills &harr; Systems:</strong> Knowledge lives in
                  relationships, not systems. Current systems don&apos;t capture
                  or enable knowledge access. This misalignment means strategic
                  asset remains trapped.
                </li>
                <li>
                  <strong>Skills &harr; Staff:</strong> Experts won&apos;t
                  document because it creates burden without personal benefit.
                  Staff motivation (mission-driven, not process-driven)
                  doesn&apos;t support documentation for documentation&apos;s
                  sake.
                </li>
                <li>
                  <strong>Skills &harr; Style:</strong> Knowledge sharing
                  happens through relational networks (style) not formal
                  processes. This alignment is strength for those in networks,
                  weakness for those outside networks.
                </li>
                <li>
                  <strong>Critical misalignment:</strong> Greatest strategic
                  asset (institutional knowledge across 115 countries) is
                  organizationally inaccessible because Skills element (trapped
                  knowledge) doesn&apos;t align with Systems element (no capture
                  mechanism) or Staff element (experts won&apos;t document).
                  Strength exists but is unusable.
                </li>
              </ul>
            </Card>
          </div>
        </Container>
      </section>

      {/* Element 7: Shared Values */}
      <section className="py-16 bg-gray-50">
        <Container size="content">
          <div className="mb-2">
            <span className="inline-block bg-purple-600 text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
              Core Element
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Element 7: Shared Values
          </h2>

          <Card className="mb-8">
            <h3 className="text-lg font-bold text-navy mb-3">
              Assessment Questions
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                &bull; What principles guide organizational behavior?
              </li>
              <li>&bull; What is the organizational identity?</li>
              <li>
                &bull; What language resonates or triggers resistance?
              </li>
              <li>&bull; What do staff value most?</li>
            </ul>
          </Card>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                What We Found
              </h3>

              <div className="space-y-6 text-gray-700 leading-relaxed">
                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Core Identity
                  </h4>
                  <p>
                    Mission-driven, non-corporate, relationship-centric. Staff
                    joined for social impact, not business efficiency. Value
                    collaborative trust-based work over metrics and
                    standardization. Strong non-corporate identity - &ldquo;we&apos;re
                    not a business, we serve a social mission.&rdquo;
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Cultural Values
                  </h4>
                  <p>
                    Respect for local contexts and diversity. Trust-based
                    collaboration over control. Human relationships over process
                    efficiency. Mission advancement over corporate metrics.
                    Autonomy and contextualization over standardization.
                    People-first over systems-first.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Language Sensitivity
                  </h4>
                  <p>
                    &ldquo;Corporate efficiency,&rdquo;
                    &ldquo;standardization,&rdquo; &ldquo;digital
                    transformation,&rdquo; &ldquo;best practices&rdquo; language
                    triggers &ldquo;this isn&apos;t who we are&rdquo; resistance.
                    Business-speak feels alien and manipulative. Staff respond to
                    mission-framed language about advancing social impact,
                    serving clients better, amplifying collective expertise for
                    mission advancement.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Value Alignment
                  </h4>
                  <p>
                    Staff engage authentically when initiatives align with
                    mission and values (social impact, relationship enhancement,
                    trust-building). Resist when framed in corporate efficiency
                    terms even if ultimately beneficial. Values alignment matters
                    more than practical benefit for engagement.
                  </p>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-navy mb-2">
                    Identity Protection
                  </h4>
                  <p>
                    Strong organizational identity means changes perceived as
                    threatening identity face intense resistance. &ldquo;This is
                    who we are&rdquo; identity must be respected, not
                    challenged, for change adoption.
                  </p>
                </div>
              </div>
            </div>

            <Card className="border-l-4 border-l-purple-500 bg-purple-50">
              <h3 className="text-lg font-bold text-navy mb-3">
                Interdependencies with Other Elements
              </h3>
              <ul className="space-y-3 text-gray-700">
                <li>
                  <strong>Shared Values &harr; Style:</strong> Mission-driven
                  values directly create bottom-up, relational style. Values
                  explain why style exists - mandate culture contradicts
                  trust-based collaborative values.
                </li>
                <li>
                  <strong>Shared Values &harr; Staff:</strong> Mission-driven
                  values explain staff motivation profile. Staff joined for
                  values alignment, resist initiatives contradicting values even
                  when mandated.
                </li>
                <li>
                  <strong>Shared Values &harr; Structure:</strong> Respect for
                  local contexts and autonomy (values) creates decentralized
                  structure. Values justify why headquarters can&apos;t mandate -
                  violates autonomy values.
                </li>
                <li>
                  <strong>Shared Values &harr; Systems:</strong> Failed systems
                  emphasized standardization/efficiency (contradicting values).
                  This values misalignment contributed to system rejection beyond
                  just operational failures.
                </li>
                <li>
                  <strong>Powerful alignment:</strong> Shared Values strongly
                  aligned with Style, Staff, and Structure. This creates
                  coherent cultural architecture - all soft elements reinforce
                  each other. But this strong alignment also means anything
                  violating values faces resistance from multiple elements
                  simultaneously.
                </li>
              </ul>
            </Card>
          </div>
        </Container>
      </section>

      {/* Interactive 7S Assessment Map */}
      <section className="py-16">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-4 text-center">
            Interactive 7S Assessment Map
          </h2>
          <p className="text-gray-600 text-center mb-8">
            Click each element to explore key findings and interdependencies
          </p>
          <McKinsey7SVisual />
        </Container>
      </section>

      {/* Organizational Alignment Analysis */}
      <section className="py-16 bg-gray-50">
        <Container size="content">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-8">
            Organizational Alignment Analysis
          </h2>

          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                Strong Alignments (Organizational Strengths)
              </h3>

              <Card className="border-l-4 border-l-green-500 bg-green-50 mb-6">
                <h4 className="font-bold text-green-800 mb-3">
                  Bottom-Up Cultural Coherence
                </h4>
                <p className="text-gray-700 mb-3">
                  Style (bottom-up, relational) + Structure (decentralized
                  autonomy) + Staff (mission-driven) + Shared Values
                  (trust-based, autonomy-respecting) = Powerful aligned cultural
                  architecture.
                </p>
                <p className="text-gray-700 mb-3">
                  <strong>Strength:</strong> When change approaches align with
                  this cultural architecture, peer networks accelerate adoption
                  faster than top-down mandates ever could. Culture becomes
                  change accelerant.
                </p>
                <p className="text-gray-700">
                  <strong>Constraint:</strong> Any approach requiring top-down
                  coordination, centralized mandates, or standardization fights
                  against four aligned elements. Nearly impossible to execute.
                </p>
              </Card>

              <Card className="border-l-4 border-l-green-500 bg-green-50">
                <h4 className="font-bold text-green-800 mb-3">
                  Multilingual Capability
                </h4>
                <p className="text-gray-700 mb-3">
                  Staff (60% non-English) + Structure (115 countries) + Skills
                  (cross-cultural adaptation) = Organizational capability to
                  operate across linguistic contexts.
                </p>
                <p className="text-gray-700 mb-3">
                  <strong>Strength:</strong> Can serve diverse markets and
                  contexts others cannot.
                </p>
                <p className="text-gray-700">
                  <strong>Constraint:</strong> Any approach must support four
                  languages from day one or exclude 60% of workforce. Language
                  inclusivity non-negotiable.
                </p>
              </Card>
            </div>

            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                Critical Misalignments (Organizational Weaknesses)
              </h3>

              <Card className="border-l-4 border-l-red-500 bg-red-50 mb-6">
                <h4 className="font-bold text-red-800 mb-3">
                  Trapped Knowledge Misalignment
                </h4>
                <p className="text-gray-700 mb-3">
                  Strategy (knowledge is competitive asset) &ne; Skills
                  (knowledge trapped in silos) &ne; Systems (no knowledge
                  capture) &ne; Staff (experts won&apos;t document)
                </p>
                <p className="text-gray-700 mb-3">
                  <strong>Impact:</strong> Greatest strategic asset
                  organizationally inaccessible. Strength exists but is
                  unusable. This misalignment creates critical competitive
                  vulnerability - cannot leverage primary advantage.
                </p>
                <p className="text-gray-700 font-semibold">
                  This is the core organizational problem: Four elements
                  misaligned around knowledge accessibility. Cannot fix by
                  changing one element - requires approach that addresses all
                  four simultaneously.
                </p>
              </Card>

              <Card className="border-l-4 border-l-red-500 bg-red-50 mb-6">
                <h4 className="font-bold text-red-800 mb-3">
                  Change Fatigue Misalignment
                </h4>
                <p className="text-gray-700 mb-3">
                  Systems (need improvements) &ne; Staff (change-fatigued,
                  limited capacity) &ne; Systems precedent (failed
                  implementations)
                </p>
                <p className="text-gray-700">
                  <strong>Impact:</strong> Organization needs system
                  improvements but staff resist systems. Past failures created
                  precedent making future systems difficult to implement
                  regardless of merit.
                </p>
              </Card>

              <Card className="border-l-4 border-l-red-500 bg-red-50">
                <h4 className="font-bold text-red-800 mb-3">
                  Resource Constraint Misalignment
                </h4>
                <p className="text-gray-700 mb-3">
                  Strategy (need competitive capabilities) &ne; Strategy budget
                  (severely constrained) &ne; Staff (cannot recruit specialized
                  talent)
                </p>
                <p className="text-gray-700">
                  <strong>Impact:</strong> Need sophisticated capabilities but
                  cannot afford traditional approaches (vendor platforms $2-5M)
                  or talent acquisition. Must find approach buildable with
                  existing resources and staff.
                </p>
              </Card>
            </div>

            <div>
              <h3 className="text-xl font-bold text-navy mb-4">
                Interdependency Insights
              </h3>

              <div className="space-y-4 text-gray-700 leading-relaxed">
                <p>
                  <strong className="text-navy">
                    Soft Elements (Style, Staff, Shared Values) Form Coherent
                    Culture:
                  </strong>{" "}
                  These three elements strongly aligned create powerful cultural
                  architecture. This alignment is organizational strength when
                  leveraged (peer-driven change spreads fast) but organizational
                  constraint when violated (cultural resistance from multiple
                  directions).
                </p>
                <p>
                  <strong className="text-navy">
                    Hard Elements (Strategy, Structure, Systems) Have Gaps:
                  </strong>{" "}
                  Strategy asset (knowledge) not supported by Systems (no
                  capture) or Structure (decentralized = harder to coordinate
                  knowledge sharing). Hard element gaps prevent strategic asset
                  utilization.
                </p>
                <p>
                  <strong className="text-navy">Skills Element Bridge:</strong>{" "}
                  Skills element sits between hard and soft. Technical skills
                  (hard) limited, but relationship skills (soft) strong.
                  Knowledge (strategic asset) trapped because soft elements
                  (experts won&apos;t document) not supported by hard elements
                  (no systems).
                </p>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* What This Organization Can Do / Cannot Do */}
      <section className="py-16">
        <Container size="content">
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <div>
              <h2 className="text-2xl font-bold text-navy mb-6">
                What This Organization Can Do
              </h2>
              <Card className="border-l-4 border-l-green-500 bg-green-50">
                <h3 className="font-bold text-green-800 mb-4">
                  Strengths That Are Usable
                </h3>
                <ol className="space-y-3 text-gray-700 list-decimal list-inside">
                  <li>
                    <strong>Peer-driven adoption:</strong> Strong alignment
                    across Style, Structure, Staff, Shared Values means
                    peer-to-peer self-initiated adoption very effective when value
                    demonstrated
                  </li>
                  <li>
                    <strong>Local adaptation:</strong> Decentralized structure +
                    relationship skills + respect for local contexts = excellent
                    capability for context-specific implementation
                  </li>
                  <li>
                    <strong>Mission-driven engagement:</strong> Mission-aligned
                    initiatives generate authentic intrinsic commitment (when
                    properly framed)
                  </li>
                  <li>
                    <strong>Multilingual operation:</strong> Can implement across
                    four languages given organizational capability
                  </li>
                  <li>
                    <strong>Relationship-based work:</strong> Strong at
                    collaborative, trust-based approaches leveraging existing
                    relationship networks
                  </li>
                </ol>
              </Card>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-navy mb-6">
                What This Organization Cannot Do
              </h2>
              <Card className="border-l-4 border-l-red-500 bg-red-50">
                <h3 className="font-bold text-red-800 mb-4">
                  Constraints That Are Non-Negotiable
                </h3>
                <ol className="space-y-3 text-gray-700 list-decimal list-inside">
                  <li>
                    <strong>Top-down mandated change:</strong> Style, Structure,
                    Staff, Shared Values all misaligned with mandate approaches -
                    organizationally infeasible
                  </li>
                  <li>
                    <strong>Centralized enterprise-wide coordination:</strong>{" "}
                    Structure prevents, Style doesn&apos;t support, Staff would
                    resist
                  </li>
                  <li>
                    <strong>Large capital investments:</strong> Budget
                    constraints absolute, cannot change on transformation
                    timeline
                  </li>
                  <li>
                    <strong>Rapid technical capability development:</strong>{" "}
                    Staff skills profile doesn&apos;t support, would require
                    time and resources unavailable
                  </li>
                  <li>
                    <strong>English-only approaches:</strong> Excludes 60% of
                    workforce, structurally impossible
                  </li>
                  <li>
                    <strong>
                      Expert knowledge documentation through mandates:
                    </strong>{" "}
                    Skills, Staff, Style all show this won&apos;t work - experts
                    will resist
                  </li>
                </ol>
              </Card>
            </div>
          </div>

          {/* What Needs to Change */}
          <h2 className="text-2xl font-bold text-navy mb-6">
            What Needs to Change (Or Be Worked Around)
          </h2>

          <Card className="border-l-4 border-l-amber bg-amber/5 mb-8">
            <h3 className="font-bold text-navy mb-3">
              Critical Misalignment That Constrains Strategy
            </h3>
            <p className="text-gray-700 mb-4 leading-relaxed">
              The <strong>trapped knowledge misalignment</strong> (Strategy &ne;
              Skills &ne; Systems &ne; Staff) must be addressed for any
              competitive strategy to succeed. Either:
            </p>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded border border-gray-200">
                <h4 className="font-bold text-navy mb-2">
                  Option A: Change the organization (align elements)
                </h4>
                <ul className="space-y-2 text-gray-700 text-base">
                  <li>
                    &bull; Create systems that capture knowledge automatically
                    (change Systems)
                  </li>
                  <li>
                    &bull; Mandate expert documentation (change Staff behavior)
                  </li>
                </ul>
                <p className="text-red-700 text-base mt-3 font-semibold">
                  Problem: This fights against Style, Staff, Shared Values
                  alignment. Nearly impossible given cultural strength and
                  change fatigue.
                </p>
              </div>

              <div className="bg-white p-4 rounded border border-gray-200">
                <h4 className="font-bold text-navy mb-2">
                  Option B: Design approach that works with misalignment
                </h4>
                <ul className="space-y-2 text-gray-700 text-base">
                  <li>
                    &bull; Make knowledge accessible WITHOUT requiring expert
                    documentation
                  </li>
                  <li>
                    &bull; Capture knowledge passively as experts work naturally
                  </li>
                  <li>
                    &bull; Work with organizational characteristics as they
                    exist
                  </li>
                </ul>
                <p className="text-green-700 text-base mt-3 font-semibold">
                  Advantage: Respects cultural alignment, doesn&apos;t require
                  changing multiple elements
                </p>
              </div>
            </div>
          </Card>
        </Container>
      </section>

      {/* Organizational Profile Summary */}
      <section className="py-16 bg-gray-50">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Organizational Profile Summary
          </h2>

          <p className="text-lg text-gray-700 mb-6 font-semibold">
            This is an organization with:
          </p>

          <ul className="space-y-3 text-gray-700 leading-relaxed mb-8">
            <li>
              &bull; Strong cultural coherence (bottom-up, relational,
              mission-driven) across soft elements creating powerful
              peer-driven capability when aligned approaches used
            </li>
            <li>
              &bull; Critical knowledge assets trapped by misalignment between
              strategic needs and organizational capabilities
            </li>
            <li>
              &bull; Severe resource constraints (budget, talent access)
              requiring creative approaches
            </li>
            <li>
              &bull; Change fatigue limiting capacity for transformation but not
              eliminating possibility if value demonstrated
            </li>
            <li>
              &bull; Decentralized structure enabling local adaptation but
              preventing centralized coordination
            </li>
            <li>
              &bull; Multilingual capability requiring four-language
              inclusivity
            </li>
            <li>
              &bull; Systems precedent creating skepticism that must be overcome
              through different approach patterns
            </li>
          </ul>

          <Card className="border-l-4 border-l-teal bg-teal/5">
            <h3 className="font-bold text-navy mb-3">
              For transformation strategy:
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                &bull; Must leverage aligned cultural elements (peer networks,
                mission framing, self-initiated adoption)
              </li>
              <li>
                &bull; Must address trapped knowledge misalignment without
                requiring organizational element changes
              </li>
              <li>
                &bull; Must work within resource constraints (existing staff,
                &lt;$1M budget)
              </li>
              <li>
                &bull; Must respect change fatigue (value-first, not
                burden-first)
              </li>
              <li>
                &bull; Must support decentralized adoption
                (country-by-country self-initiated)
              </li>
              <li>
                &bull; Must be multilingual (four languages from day one)
              </li>
              <li>
                &bull; Must demonstrate different pattern from failed systems
                (quick value, no training prerequisites)
              </li>
            </ul>
          </Card>
        </Container>
      </section>

      {/* Conclusion */}
      <section className="py-16">
        <Container size="reading">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-6">
            Conclusion
          </h2>

          <div className="space-y-6 text-gray-700 leading-relaxed">
            <p>
              The McKinsey 7S assessment revealed an organization with strong
              cultural coherence creating powerful peer-driven capabilities when
              aligned approaches used, but with critical knowledge asset trapped
              by misalignment between strategic needs and organizational
              characteristics.
            </p>

            <div>
              <h3 className="text-lg font-bold text-navy mb-3">
                Key organizational characteristics:
              </h3>
              <ul className="space-y-2">
                <li>
                  &bull; Strong bottom-up, relational, mission-driven culture
                  (Style, Staff, Shared Values aligned)
                </li>
                <li>
                  &bull; Decentralized structure reinforcing cultural autonomy
                </li>
                <li>
                  &bull; Trapped institutional knowledge
                  (Strategy-Skills-Systems-Staff misaligned)
                </li>
                <li>
                  &bull; Severe resource constraints (budget, talent access)
                </li>
                <li>
                  &bull; Change fatigue limiting capacity but not eliminating
                  possibility
                </li>
                <li>
                  &bull; Multilingual capability requiring four-language
                  inclusivity
                </li>
              </ul>
            </div>

            <p>
              <strong className="text-navy">Critical misalignment:</strong>{" "}
              Greatest strategic asset (institutional knowledge)
              organizationally inaccessible due to misalignment across four
              elements. This creates both the primary strategic challenge and
              the primary organizational constraint.
            </p>

            <p>
              <strong className="text-navy">
                For transformation strategy design:
              </strong>{" "}
              Must leverage cultural strengths (peer networks, mission
              alignment, self-initiated adoption) while addressing trapped knowledge
              misalignment without requiring changes to strongly aligned
              cultural elements. Strategy must work with organizational reality
              as it exists, not require organizational transformation before
              strategic transformation can begin.
            </p>

            <p>
              <strong className="text-navy">The assessment value:</strong>{" "}
              Prevented expensive strategic errors by revealing what
              organization cannot do (top-down mandates, centralized
              coordination, documentation requirements) while identifying what
              organization can do exceptionally well when properly aligned
              (peer-driven self-initiated adoption, local adaptation, mission-driven
              engagement).
            </p>

            <p>
              Strategy design must find approach at intersection of competitive
              requirements and organizational capabilities - the 7S analysis
              defined the organizational half of that equation.
            </p>
          </div>

          {/* Navigation */}
          <div className="flex flex-wrap justify-between items-center pt-8 mt-8 border-t border-gray-200 gap-4">
            <Link
              href="/strategy"
              className="inline-flex items-center text-teal hover:text-teal/80 font-semibold focus:outline-none focus:ring-2 focus:ring-teal"
            >
              &larr; Return to Strategy Overview
            </Link>
            <Link
              href="/strategy/pugh-matrix"
              className="inline-flex items-center text-teal hover:text-teal/80 font-semibold focus:outline-none focus:ring-2 focus:ring-teal"
            >
              Continue to Solution Selection: Pugh Matrix &rarr;
            </Link>
          </div>
        </Container>
      </section>
    </>
  );
}
