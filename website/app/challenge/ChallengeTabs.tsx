"use client";

import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui";

/* ───────────────────── Section 1: The Stakes ───────────────────── */

function CrisisConditions() {
  return (
    <div>
      <h3 className="text-2xl md:text-3xl font-bold mb-6 text-gray-900">
        The Crisis Conditions
      </h3>
      <p className="text-lg text-gray-700 mb-8">
        This AI transformation began under extraordinary pressure. The
        organization faced three compounding crises that made traditional AI
        deployment approaches highly infeasible.
      </p>

      <div className="space-y-10">
        {/* Crisis 1 */}
        <div>
          <h4 className="text-xl md:text-2xl font-semibold mb-4 text-gray-900">
            Crisis 1: Competitive Survival
          </h4>
          <div className="space-y-4 text-lg text-gray-800">
            <p>
              Market consolidation in the sector created existential competitive
              pressure. Competitors began entering each other&apos;s traditional
              markets in what became a fight for survival. The
              organization&apos;s core competitive advantages (institutional knowledge, deep client relationships, and decades of project expertise) were under threat.
            </p>
            <p>
              New market entrants leveraged AI capabilities to compete without
              the institutional baggage of established firms. Meanwhile, the
              organization faced a growing productivity gap versus AI-enabled
              competitors, with talent leaving for better-equipped firms and
              client expectations rising as competitors delivered faster results
              with AI tools.
            </p>
            <p>
              Market consolidation forced significant staff reductions over a
              six-month period. The remaining employees absorbed increased
              workloads while managing fear and uncertainty about job security.
              Any new efficiency initiative was viewed with suspicion as a
              potential precursor to further layoffs.
            </p>
          </div>
        </div>

        {/* Crisis 2 */}
        <div>
          <h4 className="text-xl md:text-2xl font-semibold mb-4 text-gray-900">
            Crisis 2: Financial Crisis and Timing Mismatch
          </h4>
          <div className="space-y-4 text-lg text-gray-800">
            <p>
              Revenue pressure from sector upheaval meant the organization could
              not afford traditional AI investment timelines. The board and
              funders demanded visible AI progress and fast ROI, but traditional
              AI deployments require 3-4 years to show returns: 18-24 months to
              deploy vendor platforms plus another 12-24 months to realize
              business value.
            </p>
            <p>
              The organization needed to close competitive gaps immediately, not
              in 3-4 years when the market might already be consolidated. Budget
              constraints after staff reductions made $2M+ vendor platforms
              unaffordable, and the C-suite was highly risk-averse given the
              financial pressures.
            </p>
          </div>
        </div>

        {/* Crisis 3 */}
        <div>
          <h4 className="text-xl md:text-2xl font-semibold mb-4 text-gray-900">
            Crisis 3: Organizational Skepticism and Change Fatigue
          </h4>
          <div className="space-y-4 text-lg text-gray-800">
            <p>
              A recent top-down systems transformation had damaged
              organizational trust. Many employees saw limited value from the
              initiative, experienced increased work overhead rather than reduced
              burden, and developed deep resentment toward headquarters-mandated
              changes.
            </p>
            <p>
              Teams were exhausted from change initiatives that failed to deliver value. International teams (70% of the workforce operating in English, French, Spanish, and Arabic) were particularly skeptical of headquarters-driven initiatives.
            </p>
            <p>
              After staff reductions, remaining employees had limited capacity to
              learn new tools while handling increased responsibilities. The
              organization&apos;s decentralized, relational culture meant top-down mandates would fail. Solutions required organic adoption through demonstrated value.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function StakeholderComplications() {
  return (
    <div>
      <h3 className="text-2xl md:text-3xl font-bold mb-6 text-gray-900">
        Stakeholder Complications
      </h3>
      <p className="text-lg text-gray-700 mb-8">
        These crisis conditions created contradictory stakeholder pressures that
        traditional AI approaches could not satisfy:
      </p>

      <div className="space-y-6 text-lg text-gray-800">
        <p>
          <strong className="text-gray-900">The Board</strong> demanded visible
          AI progress on quarterly timelines while also requiring fast ROI
          throughout the transformation, not just future promises. They needed to
          demonstrate innovation to stakeholders but also wanted proof the
          organization was closing competitive gaps.
        </p>
        <p>
          <strong className="text-gray-900">The C-Suite</strong> was deeply
          risk-averse after past failures and required the ability to exit any AI
          initiative without sunk costs. They needed tangible returns at each
          stage of investment and wanted capabilities that would compound over
          time rather than all-or-nothing bets.
        </p>
        <p>
          <strong className="text-gray-900">Project Teams</strong> in the
          decentralized structure needed to see immediate value at their division
          and regional levels. They required solutions that worked equally well
          in all four organizational languages and resisted any headquarters
          mandate after the recent failed transformation. With increased
          workloads post-layoffs, they had zero appetite for &quot;another
          corporate initiative.&quot;
        </p>
        <p>
          <strong className="text-gray-900">Customers</strong> valued
          consistency from long-standing relationships and were adverse to AI
          being imposed on them. They wanted improved quality and
          personalization but resisted forced changes to established workflows.
          They required transparency, impact metrics, and compliance with
          diverse regulatory environments, with some demanding ethical AI
          guarantees and others having data sovereignty concerns.
        </p>
      </div>
    </div>
  );
}

/* ───────────────────── Section 2: The Dilemma ───────────────────── */

function CultureAndStaff() {
  return (
    <div>
      <h3 className="text-2xl md:text-3xl font-bold mb-6 text-gray-900">
        Culture &amp; Staff
      </h3>
      <div className="space-y-4 text-lg text-gray-800">
        <p>
          The organization operated through a decentralized structure with a
          deeply relational culture, where trust and relationships mattered more
          than systems. The 70% international workforce operated in four languages (English, French, Spanish, Arabic),
          bringing diverse contexts and workflows that had historically been the
          organization&apos;s strength.
        </p>
        <p>
          A recent top-down systems transformation had damaged organizational
          trust. The initiative added work overhead instead of reducing burden,
          creating antipathy toward headquarters-mandated changes. International
          teams, in particular, felt the transformation &quot;was built for HQ
          monitoring and not on the ground needs and staff.&quot; The failed
          transformation created deep change fatigue across the organization.
        </p>
        <p>
          The staff reductions compounded this cultural damage. Over a six-month
          period, the organization was forced to cut significant portions of its
          workforce, leaving remaining employees overwhelmed and doing the work
          of former colleagues with zero additional support. Any new initiative
          was now viewed as either a precursor to more layoffs
          (&quot;efficiency initiative&quot; = &quot;job cuts&quot;) or another
          system that would &quot;make our jobs harder.&quot;
        </p>
        <p>
          In this context, any solution requiring mandated adoption would fail.
          You cannot mandate trust. You cannot force adoption in a
          decentralized, relational culture. And you cannot ask overwhelmed,
          change-fatigued staff to &quot;trust us, this will help&quot; after
          recent failures.
        </p>
      </div>
    </div>
  );
}

function FinancialAndTiming() {
  return (
    <div>
      <h3 className="text-2xl md:text-3xl font-bold mb-6 text-gray-900">
        Financial &amp; Timing
      </h3>
      <div className="space-y-4 text-lg text-gray-800">
        <p>
          The financial crisis was immediate and severe. Over the six-month
          upheaval period, the organization experienced a 25% revenue reduction.
          Projections showed a further 10% decline over the following six months,
          with forecasts indicating a 50% total revenue reduction within two
          years of the initial upheaval.
        </p>
        <p>
          Previously, the organization had operated with discretionary budgets
          allocated to decentralized regional and country offices. This
          flexibility allowed local offices to address process gaps and
          operational inefficiencies as they arose. The revenue collapse
          eliminated these buffers. Combined with reduced staff, the financial
          flexibility that had previously masked inefficiencies disappeared. The
          need for centralized, low-risk, strategically coordinated investments
          became critical.
        </p>
        <p>
          The C-suite could not approve $2M-$5M upfront bets on vendor
          platforms. Investors and funders, already nervous after staff
          reductions and revenue decline, demanded proof of prudent spending
          rather than multi-year gambles. Any investment needed to spread risk
          incrementally, with the ability to stop at any point without losing
          prior value.
        </p>
        <p>
          The timing mismatch compounded the financial constraints. Traditional
          AI platforms require 3-4 year ROI timelines: 18-24 months to deploy
          vendor platforms plus another 12-24 months to realize business value.
          But the organization was fighting for survival with a projected 50%
          revenue reduction over two years. By the time a vendor platform
          delivered ROI (year 3-4), the market might have consolidated and the
          organization could be irrelevant. Meanwhile, both established
          competitors and new entrants were attempting to leverage AI
          capabilities to gain competitive advantage in the shrinking market.
        </p>
        <p>
          The Board demanded quarterly demonstrable results to show stakeholders
          the organization was responding to competitive threats, but traditional
          approaches could not deliver that timeline. The organization needed
          visible progress at each stage to justify continued investment to
          nervous funders, not promises of returns three to four years in the
          future.
        </p>
      </div>
    </div>
  );
}

function CompetitiveSurvival() {
  return (
    <div>
      <h3 className="text-2xl md:text-3xl font-bold mb-6 text-gray-900">
        Competitive Survival
      </h3>
      <div className="space-y-4 text-lg text-gray-800">
        <p>
          The competitive landscape had fundamentally shifted. Market
          consolidation forced established competitors to enter each
          other&apos;s traditional markets in a fight for survival.
          Simultaneously, new entrants emerged with leaner cost structures and
          from-scratch technology stacks, attempting to leverage AI capabilities
          to compete without the institutional baggage that constrained
          established players.
        </p>
        <p>
          The organization&apos;s core competitive advantages were institutional knowledge, deep client relationships built over decades, and hard-won contextual expertise across diverse
          regulatory environments. These advantages could not be replicated
          quickly. The organization could not compete on price, where new
          entrants with lower cost structures held the advantage. It could not
          compete on speed or agility, where smaller firms without legacy
          systems moved faster.
        </p>
        <p>
          The organization had to compete on institutional knowledge,
          relationships, and contextual expertise. But that knowledge was
          trapped in silos across decentralized country offices,
          inaccessible at the speed and scale needed to respond to competitive
          pressures. Without a way to make this knowledge accessible and
          actionable across the organization&apos;s multilingual footprint, these competitive advantages remained locked away while competitors attempted to gain
          ground.
        </p>
        <p>
          This creates a critical constraint for AI deployment. Any AI approach
          that commoditized institutional knowledge into generic processes
          purchasable by competitors would eliminate the organization&apos;s
          differentiation. Vendor platforms, in particular, posed this risk.
          They would transform decades of hard-won expertise into standardized
          &quot;best practices&quot; that any competitor could buy. Smaller,
          more agile entrants could purchase the same platform and instantly
          acquire &quot;good enough&quot; capabilities without decades of
          learning, while the organization would have paid millions to eliminate
          its own competitive moat.
        </p>
        <p>
          The organization needed AI that amplified its unique knowledge
          advantage, making institutional knowledge accessible and scalable
          while remaining proprietary. Any approach that commodified this
          knowledge or made it purchasable by competitors would accelerate
          competitive losses rather than address them.
        </p>
      </div>
    </div>
  );
}

/* ───────────────────── Exported Tabbed Sections ───────────────────── */

export function TheStakesTabs() {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
      <Tabs defaultValue="crises">
        <TabsList className="p-1 m-4 rounded-lg flex gap-2" style={{ backgroundColor: 'rgba(30, 58, 95, 0.1)' }}>
          <TabsTrigger
            value="crises"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy hover:bg-navy/10"
          >
            Crisis Conditions
          </TabsTrigger>
          <TabsTrigger
            value="stakeholders"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy hover:bg-navy/10"
          >
            Stakeholder Complications
          </TabsTrigger>
        </TabsList>

        <div className="px-4 pb-4">
          <TabsContent value="crises">
            <CrisisConditions />
          </TabsContent>
          <TabsContent value="stakeholders">
            <StakeholderComplications />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}

export function TheDilemmaTabs() {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
      <Tabs defaultValue="culture">
        <TabsList className="p-1 m-4 rounded-lg flex gap-2" style={{ backgroundColor: 'rgba(26, 188, 156, 0.1)' }}>
          <TabsTrigger
            value="culture"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal data-[state=active]:text-white data-[state=active]:shadow-sm text-teal hover:bg-teal/10"
          >
            Culture &amp; Staff
          </TabsTrigger>
          <TabsTrigger
            value="financial"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal data-[state=active]:text-white data-[state=active]:shadow-sm text-teal hover:bg-teal/10"
          >
            Financial &amp; Timing
          </TabsTrigger>
          <TabsTrigger
            value="competitive"
            className="flex-1 py-3 px-4 text-lg font-medium rounded-md transition-all data-[state=active]:bg-teal data-[state=active]:text-white data-[state=active]:shadow-sm text-teal hover:bg-teal/10"
          >
            Competitive Survival
          </TabsTrigger>
        </TabsList>

        <div className="px-4 pb-4">
          <TabsContent value="culture">
            <CultureAndStaff />
          </TabsContent>
          <TabsContent value="financial">
            <FinancialAndTiming />
          </TabsContent>
          <TabsContent value="competitive">
            <CompetitiveSurvival />
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
