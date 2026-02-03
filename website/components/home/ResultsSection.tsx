import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { Check } from "lucide-react";

export function ResultsSection() {
  return (
    <section className="py-20 bg-gradient-to-b from-white to-navy/5">
      <Container>
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-navy mb-4">Results</h2>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto">
            Stakeholder success, progressive value delivery, and economic proof
          </p>
        </div>

        {/* Part 1: Stakeholder Success */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-navy text-center mb-8">Stakeholder Success</h3>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            {/* Card 1: The Board */}
            <Card className="border-l-4 border-teal">
              <div className="flex items-start gap-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-teal flex items-center justify-center flex-shrink-0">
                  <Check className="w-5 h-5 text-white" />
                </div>
                <h4 className="text-xl font-bold text-navy">The Board</h4>
              </div>
              <div className="mb-4">
                <p className="text-base font-semibold text-gray-600 mb-2">Their Need:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Fear of missing out on AI opportunities</li>
                  <li>• Wanted visible leadership investment in AI</li>
                  <li>• Demanded fast ROI throughout, not just future promises</li>
                </ul>
              </div>
              <div>
                <p className="text-base font-semibold text-teal mb-2">Result:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Built AI capabilities from the core of the organization outward (strategic leadership)</li>
                  <li>• Visible AI progress at each phase</li>
                  <li>• ROI delivered progressively, not deferred to future</li>
                  <li>• Demonstrated innovation, not just technology adoption</li>
                </ul>
              </div>
            </Card>

            {/* Card 2: C-Suite */}
            <Card className="border-l-4 border-amber">
              <div className="flex items-start gap-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-amber flex items-center justify-center flex-shrink-0">
                  <Check className="w-5 h-5 text-white" />
                </div>
                <h4 className="text-xl font-bold text-navy">C-Suite</h4>
              </div>
              <div className="mb-4">
                <p className="text-base font-semibold text-gray-600 mb-2">Their Need:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Risk-averse after past failed initiatives</li>
                  <li>• Required optionality to exit without sunk costs</li>
                  <li>• Needed tangible returns at each stage</li>
                  <li>• Wanted cumulative capabilities that compound</li>
                </ul>
              </div>
              <div>
                <p className="text-base font-semibold text-amber mb-2">Result:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Bounded risk: &lt;$5K investment per phase</li>
                  <li>• Could stop at any phase with value retained</li>
                  <li>• Tangible ROI at Phase 1, 2, 3, 4, 5</li>
                  <li>• Each phase builds on previous capabilities</li>
                </ul>
              </div>
            </Card>

            {/* Card 3: Culture & People */}
            <Card className="border-l-4 border-magenta">
              <div className="flex items-start gap-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-magenta flex items-center justify-center flex-shrink-0">
                  <Check className="w-5 h-5 text-white" />
                </div>
                <h4 className="text-xl font-bold text-navy">Culture &amp; People</h4>
              </div>
              <div className="mb-4">
                <p className="text-base font-semibold text-gray-600 mb-2">Their Need:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Decentralized organization structure</li>
                  <li>• Must see short-term benefits to support change</li>
                  <li>• Change exhaustion from previous initiatives</li>
                  <li>• Need value delivered at their team/division level</li>
                </ul>
              </div>
              <div>
                <p className="text-base font-semibold text-magenta mb-2">Result:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Built AI capabilities from the core outward, not imposed from above</li>
                  <li>• Bottom-up adoption: teams chose to use it based on value they experienced</li>
                  <li>• Immediate value at team level (Phase 2)</li>
                  <li>• No mandated reorganization required</li>
                  <li>• Division-level ownership and control</li>
                </ul>
              </div>
            </Card>

            {/* Card 4: Customer */}
            <Card className="border-l-4 border-navy">
              <div className="flex items-start gap-3 mb-4">
                <div className="w-8 h-8 rounded-full bg-navy flex items-center justify-center flex-shrink-0">
                  <Check className="w-5 h-5 text-white" />
                </div>
                <h4 className="text-xl font-bold text-navy">Customer</h4>
              </div>
              <div className="mb-4">
                <p className="text-base font-semibold text-gray-600 mb-2">Their Need:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Wanted improved quality and personalization</li>
                  <li>• Adverse to AI being pushed on them</li>
                  <li>• Resistant to forced changes</li>
                  <li>• Valued consistency from long relationship</li>
                </ul>
              </div>
              <div>
                <p className="text-base font-semibold text-navy mb-2">Result:</p>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Improved service quality without workflow disruption</li>
                  <li>• No forced AI interactions with customers</li>
                  <li>• Existing relationships maintained</li>
                  <li>• Enhanced personalization through better intelligence</li>
                </ul>
              </div>
            </Card>
          </div>
        </div>

        {/* Part 2: Value Delivered Through Progressive Phases */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-navy text-center mb-8">
            Value Delivered Through Progressive Phases
          </h3>

          <div className="space-y-4">
            {/* Phase 1 */}
            <div className="flex items-start gap-4">
              <div className="bg-teal text-white p-6 rounded-lg flex-1">
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-3">
                  <h4 className="font-bold text-lg">Phase 1: Collective Knowledge (Semantic Space)</h4>
                  <span className="bg-white/20 px-3 py-1 rounded text-base w-fit">Productivity</span>
                </div>
                <p className="text-base mb-2"><strong>What&apos;s built:</strong> Unified vector database with semantic search</p>
                <p className="text-base text-white/90"><strong>User benefit:</strong> Better data retrieval and cross-silo access, ROI from emergent capabilities</p>
              </div>
            </div>

            {/* Phase 2 */}
            <div className="flex items-start gap-4">
              <div className="bg-amber text-white p-6 rounded-lg flex-1">
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-3">
                  <h4 className="font-bold text-lg">Phase 2: Domain Expertise (Task SLMs)</h4>
                  <span className="bg-white/20 px-3 py-1 rounded text-base w-fit">Productivity</span>
                </div>
                <p className="text-base mb-2"><strong>What&apos;s built:</strong> Multiple task-specific agent models tailored for company workflows</p>
                <p className="text-base text-white/90"><strong>User benefit:</strong> Precise, accurate task automation designed for their use case, ROI from efficiency</p>
              </div>
            </div>

            {/* Phase 3 */}
            <div className="flex items-start gap-4">
              <div className="bg-magenta text-white p-6 rounded-lg flex-1">
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-3">
                  <h4 className="font-bold text-lg">Phase 3: Division Expert (MoE Agents)</h4>
                  <span className="bg-white/20 px-3 py-1 rounded text-base w-fit">Differentiation</span>
                </div>
                <p className="text-base mb-2"><strong>What&apos;s built:</strong> Division Expert Agents that handle multiple tasks with high precision</p>
                <p className="text-base text-white/90"><strong>User benefit:</strong> Single point expert for their units&apos; common tasks in multiple steps with high accuracy and precision, ROI from efficiency and new capabilities</p>
              </div>
            </div>

            {/* Phase 4-5 */}
            <div className="flex items-start gap-4">
              <div className="bg-navy text-white p-6 rounded-lg flex-1">
                <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-3">
                  <h4 className="font-bold text-lg">Phase 4-5: System Intelligence (Agentic Orchestration)</h4>
                  <span className="bg-white/20 px-3 py-1 rounded text-base w-fit">Disruption</span>
                </div>
                <p className="text-base mb-2"><strong>What&apos;s built:</strong> Enterprise-wide multi-agent system designed for business model and architecture</p>
                <p className="text-base text-white/90"><strong>User benefit:</strong> Company-wide single window AI system that can navigate across divisions and provide high accuracy outputs designed around their business architecture and model. Company differentiation and disruption with new capabilities</p>
              </div>
            </div>
          </div>
        </div>

        {/* Part 3: Economic & Strategic Outcomes */}
        <div>
          <h3 className="text-2xl font-bold text-navy text-center mb-8">
            Economic &amp; Strategic Outcomes
          </h3>

          <div className="grid lg:grid-cols-2 gap-8 mb-8">
            {/* Left: Training Economics */}
            <Card>
              <h4 className="text-2xl font-bold text-navy mb-4">Direct Investment</h4>
              <div className="mb-6">
                <p className="text-4xl font-bold text-teal mb-2">$163.1K</p>
                <p className="text-gray-600">Total Direct Investment ($11,100 infrastructure + $152K training programs)</p>
              </div>
              <div className="space-y-2 text-base mb-6">
                <div className="flex justify-between">
                  <span className="text-gray-600">Phase 1:</span>
                  <span className="font-semibold">$62,400</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Phase 2:</span>
                  <span className="font-semibold">$43,600</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Phase 3:</span>
                  <span className="font-semibold">$31,200</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Phase 4:</span>
                  <span className="font-semibold">$15,500</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Phase 5:</span>
                  <span className="font-semibold">$10,400</span>
                </div>
              </div>
              <div className="pt-4 border-t border-gray-200">
                <p className="text-gray-600 mb-1">vs Traditional AI Deployment</p>
                <p className="text-2xl font-bold text-gray-400 line-through">$2M - $10M+</p>
              </div>
            </Card>

            {/* Right: Strategic Outcomes */}
            <div className="space-y-4">
              <div className="bg-teal/5 border-l-4 border-teal p-4 rounded">
                <h5 className="font-bold text-navy mb-2">Competitive Moat</h5>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Company-specific models trained on proprietary data</li>
                  <li>• Cannot be replicated by competitors</li>
                  <li>• Intelligence compounds over time</li>
                </ul>
              </div>

              <div className="bg-amber/5 border-l-4 border-amber p-4 rounded">
                <h5 className="font-bold text-navy mb-2">Deployment Flexibility</h5>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Cloud, local, or hybrid infrastructure</li>
                  <li>• No vendor lock-in</li>
                  <li>• Adaptable to changing needs</li>
                </ul>
              </div>

              <div className="bg-magenta/5 border-l-4 border-magenta p-4 rounded">
                <h5 className="font-bold text-navy mb-2">Strategic Optionality</h5>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Could stop at any phase with value retained</li>
                  <li>• Bounded risk: &lt;$5K per phase investment</li>
                  <li>• No all-or-nothing commitment</li>
                </ul>
              </div>

              <div className="bg-navy/5 border-l-4 border-navy p-4 rounded">
                <h5 className="font-bold text-navy mb-2">Sustainable Advantage</h5>
                <ul className="text-base text-gray-700 space-y-1">
                  <li>• Capability persists regardless of which innovations materialize</li>
                  <li>• Adapts as business priorities shift</li>
                  <li>• Built from organizational core outward</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Closing Callout */}
          <div className="bg-amber/10 border-l-4 border-amber p-6 rounded">
            <p className="text-lg text-gray-800">
              These economics enable experimentation at scale. Build proprietary intelligence
              for $11,100, not $2M+. Maintain optionality throughout. Create competitive
              advantage that compounds over time, regardless of which discovered innovations
              you choose to pursue.
            </p>
          </div>
        </div>
      </Container>
    </section>
  );
}
