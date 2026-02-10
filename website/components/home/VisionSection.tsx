import { Container } from "@/components/layout/Container";

export function VisionSection() {
  return (
    <section className="py-20">
      <Container size="reading">
        <h2 className="text-4xl font-bold text-navy text-center mb-6">
          Vision &amp; Strategy
        </h2>
        <p className="text-xl text-gray-700 text-center max-w-3xl mx-auto mb-12">
          AI will transform organizational intelligence and automation. How it transforms
          everything else (workflows, customers, structure) will be discovered through use,
          not designed in advance.
        </p>

        {/* Part 1: Problem → Solution → Value */}
        <div className="mb-16">
          <div className="space-y-8">
            {/* The Problem */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-3">The Problem</h3>
              <p className="text-gray-700 mb-4">
                Enterprises invest heavily in AI but face vendor lock-in, generic tools that don&apos;t
                learn organizational patterns, and top-down deployments that fail to address where
                work actually happens. Commercial AI platforms remain generic regardless of how much
                proprietary data exists, creating no competitive advantage.
              </p>
              <p className="text-gray-700">
                Traditional AI bets on specific transformations upfront: &quot;This will change how sales
                works&quot; or &quot;Customers will interact this way.&quot; Those assumptions become dependencies
                that constrain future options when reality differs from projections.
              </p>
            </div>

            {/* The Solution */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-3">The Solution</h3>
              <p className="text-gray-700 mb-4">
                Build AI capabilities from the bottom up: team-level experimentation creating
                proprietary intelligence that compounds with use. Start with shared semantic
                infrastructure, then fine-tune task-specific models on organizational data,
                consolidate into division-level agents, and discover cross-division patterns
                through structured experimentation.
              </p>
              <p className="text-gray-700">
                This is the AI Habitat philosophy in practice: AI&apos;s transformation of intelligence
                and automation is certain. Build those capabilities as the foundation. Let everything
                else (process innovation, customer model changes, structural adaptations) emerge
                opportunistically as teams experiment and discover what becomes possible.
              </p>
            </div>

            {/* The Value */}
            <div>
              <h3 className="text-xl font-bold text-navy mb-3">The Value</h3>
              <p className="text-gray-700 mb-4">
                An orchestrated agentic system that transforms organizational intelligence while
                preserving optionality at every stage. Each phase delivers working AI capabilities
                that compound into division-level agents and ultimately enterprise-wide orchestration.
              </p>
              <div className="bg-teal/5 border-l-4 border-teal p-6 rounded">
                <h4 className="font-bold text-navy mb-3">What You&apos;re Building Toward</h4>
                <ul className="space-y-2 text-gray-700">
                  <li>• Orchestrated intelligence that transforms knowledge work and automation</li>
                  <li>• Competitive moat from proprietary data that competitors cannot replicate</li>
                  <li>• Full optionality: stop at any phase with working AI, or continue building</li>
                  <li>• $163K total investment achieving multi-agent AI at a fraction of vendor platform costs</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Part 2: The Strategic Path */}
        <div>
          <h3 className="text-2xl font-bold text-navy mb-4">The Strategic Path</h3>
          <p className="text-lg text-gray-700 mb-8">
            Build the AI transformation, discover the operational transformation
          </p>

          <div className="space-y-6">
            {/* Block 1: Teal */}
            <div className="bg-teal/5 border-l-4 border-teal p-6 rounded">
              <h4 className="font-bold text-navy mb-2">Transform Knowledge Access First</h4>
              <p className="text-gray-700">
                Phase 1 creates semantic intelligence across existing data. This is the
                guaranteed transformation: how people find and use knowledge fundamentally
                improves. No workflow changes required, but teams start discovering what
                better knowledge access makes possible. First innovations emerge here.
              </p>
            </div>

            {/* Block 2: Amber */}
            <div className="bg-amber/5 border-l-4 border-amber p-6 rounded">
              <h4 className="font-bold text-navy mb-2">Transform at Team/Task Level</h4>
              <p className="text-gray-700">
                Phase 2 builds task-specific SLMs at the team and lower unit level. Individual
                teams fine-tune models for their specific workflows—delivering real value right
                where work happens. This creates immediate ROI for those teams while enabling
                bottom-up change management: adoption spreads because teams see their own value,
                not because it&apos;s mandated. From a Lean perspective, value is created at the point
                where value is added for the customer.
              </p>
            </div>

            {/* Block 3: Magenta */}
            <div className="bg-magenta/5 border-l-4 border-magenta p-6 rounded">
              <h4 className="font-bold text-navy mb-2">Transform at Division Level</h4>
              <p className="text-gray-700">
                Phase 3 brings separate task SLMs together into division-level MoE (Mixture of
                Experts) agents. Each division gets a single agent point that orchestrates their
                task-specific models. Emergent capabilities appear here—the whole becomes more
                than the sum of its parts. Divisions discover what becomes possible with unified
                intelligence.
              </p>
            </div>

            {/* Block 4: Magenta */}
            <div className="bg-magenta/10 border-l-4 border-magenta p-6 rounded">
              <h4 className="font-bold text-navy mb-2">Discover Cross-Division Potential</h4>
              <p className="text-gray-700">
                Phase 4 accelerates years of organizational learning into 90 days of
                experimentation. MoE agents communicate across divisions in a sandboxed
                environment, discovering collaboration patterns that would normally emerge slowly
                through informal networks and tribal knowledge. What pathways work? How many
                steps? What handoffs are valuable? This messy experimentation generates the
                training data that makes Phase 5 possible—capturing relational intelligence that
                typically lives only in people&apos;s heads.
              </p>
            </div>

            {/* Block 5: Navy */}
            <div className="bg-navy text-white p-6 rounded">
              <h4 className="font-bold mb-2">Orchestrate the Whole System</h4>
              <p className="text-white/95">
                Phase 5 trains a single orchestrator on the discovered patterns from Phase 4.
                This becomes the unified point that leverages everything—all divisions, all
                tasks, all the emergent intelligence. The orchestrated system that emerges is
                based on what actually worked in experimentation, not what we assumed would work
                upfront.
              </p>
            </div>
          </div>

          {/* Closing Statement */}
          <div className="mt-8 bg-navy text-white p-8 rounded-lg">
            <p className="text-lg mb-4">
              This path guarantees AI&apos;s transformation of intelligence and automation while
              preserving optionality for everything else. Each phase builds capability:
              team-level tasks → division-level agents → discovered collaboration →
              orchestrated system. Operational innovations happen when discovered valuable,
              not because a plan assumed them.
            </p>
            <p className="text-white/90">
              $11,100 training cost. Five progressive phases. An orchestrated agentic system
              that adapts as your enterprise experiments with what AI makes possible.
            </p>
          </div>
        </div>
      </Container>
    </section>
  );
}
