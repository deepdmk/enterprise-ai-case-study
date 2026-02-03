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
          everything else—workflows, customers, structure—will be discovered through use,
          not designed in advance.
        </p>

        {/* Part 1: The End State Vision */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-navy mb-6">The End State Vision</h3>

          <div className="space-y-6 text-gray-700">
            <p>
              The vision is an <strong>orchestrated agentic system</strong> that unifies
              divisions through intelligent automation, leverages proprietary knowledge,
              and transforms how the organization processes information.
            </p>

            <p>
              <strong>What we know AI will do:</strong> Fundamentally change how knowledge
              is accessed, how intelligence is applied to decisions, and how tasks are
              automated through agentic systems.
            </p>

            <p>
              <strong>What we leave open:</strong> Everything else. Will workflows change?
              Probably—but we&apos;ll discover which ones and how. Will customer interactions
              transform? Maybe—if experiments prove it valuable. Will organizational
              structure adapt? Possibly—when opportunities reveal themselves.
            </p>

            <p>
              <strong>This is the AI Habitat philosophy in practice:</strong> AI&apos;s
              transformation of intelligence and automation is certain. Build those
              capabilities as the foundation. Let everything else—process innovation,
              customer model changes, structural adaptations—emerge opportunistically as
              teams experiment and discover what becomes possible.
            </p>

            <p>
              Traditional AI bets on specific transformations upfront: &quot;This will change
              how sales works&quot; or &quot;Customers will interact this way.&quot; Those assumptions
              become dependencies. This approach inverts that: <strong>guarantee the AI
              transformation, preserve optionality for everything else.</strong>
            </p>

            <div className="bg-teal/5 border-l-4 border-teal p-6 rounded mt-6">
              <h4 className="font-bold text-navy mb-3">The Sustainable Vision</h4>
              <ul className="space-y-2">
                <li>• Orchestrated intelligence that transforms knowledge work and automation (certain)</li>
                <li>• Integration with existing workflows, with discovered improvements emerging through use (opportunistic)</li>
                <li>• Serves current customers while building potential for new service models (flexible)</li>
                <li>• Fits current structure while enabling adaptation when valuable (adaptive)</li>
                <li>• Competitive moat from proprietary data that compounds regardless of which opportunities materialize</li>
              </ul>
            </div>

            <p className="font-semibold text-navy">
              <strong>What you&apos;re building toward:</strong> An orchestrated agentic system
              that will definitely transform organizational intelligence. How it transforms
              everything else will be discovered as teams experiment with what the new
              capabilities make possible.
            </p>
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
