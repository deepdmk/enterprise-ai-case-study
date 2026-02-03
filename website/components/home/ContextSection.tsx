import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";

export function ContextSection() {
  const stakeholders = [
    {
      title: "The Board",
      needs: [
        "Fear of missing out on AI opportunities",
        "Wanted visible leadership investment in AI",
        "Demanded fast ROI throughout, not just future promises",
        "Needed to show progress to stakeholders"
      ]
    },
    {
      title: "C-Suite",
      needs: [
        "Risk-averse after past failed initiatives",
        "Required optionality to exit without sunk costs",
        "Needed tangible returns at each stage",
        "Wanted cumulative capabilities that compound"
      ]
    },
    {
      title: "Culture & People",
      needs: [
        "Decentralized organization structure",
        "Must see short-term benefits to support change",
        "Change exhaustion from previous initiatives",
        "Need value delivered at their team/division level"
      ]
    },
    {
      title: "Customer",
      needs: [
        "Wanted improved quality and personalization",
        "Adverse to AI being pushed on them",
        "Resistant to forced changes",
        "Valued consistency from long relationship"
      ]
    },
  ];

  return (
    <section className="py-20 bg-gradient-to-b from-white to-teal/5">
      <Container>
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-navy mb-4">Context</h2>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto">
            Success required navigating competing stakeholder pressures: board urgency,
            executive risk aversion, cultural change exhaustion, and customer resistance
            to imposed AI.
          </p>
        </div>

        {/* Stakeholder Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {stakeholders.map((stakeholder, index) => (
            <Card key={index}>
              <h3 className="text-lg font-bold text-navy mb-3">{stakeholder.title}</h3>
              <ul className="space-y-2 text-base text-gray-700">
                {stakeholder.needs.map((need, needIndex) => (
                  <li key={needIndex} className="flex items-start gap-2">
                    <span className="text-gray-400 mt-0.5">•</span>
                    <span>{need}</span>
                  </li>
                ))}
              </ul>
            </Card>
          ))}
        </div>

        {/* The Organizational Challenge */}
        <div className="mb-8">
          <h3 className="text-2xl font-bold text-navy mb-4">The Organizational Challenge</h3>
          <p className="text-lg text-gray-700">
            The Board demanded visible AI progress on quarterly timelines while the C-Suite
            required the ability to exit without sunk costs. Teams needed immediate value at
            the division level, but customers resisted changes to established workflows.
            Traditional AI deployment can&apos;t satisfy these contradictions: you can&apos;t have
            all-or-nothing implementation while maintaining optionality, and you can&apos;t
            centralize while respecting decentralization.
          </p>
        </div>

        {/* Why This Required a Different Approach */}
        <div className="bg-teal/5 border-l-4 border-teal p-6 rounded">
          <h3 className="text-2xl font-bold text-navy mb-4">Why This Required a Different Approach</h3>
          <ul className="space-y-2 text-gray-700">
            <li className="flex items-start gap-2">
              <span className="text-teal mt-1">✓</span>
              <span><strong>Incremental delivery</strong> - value at every phase, not just at completion</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal mt-1">✓</span>
              <span><strong>Bounded risk</strong> - ability to stop without losing investment</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal mt-1">✓</span>
              <span><strong>Bottom-up adoption</strong> - teams discover value, not mandated from above</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal mt-1">✓</span>
              <span><strong>Customer choice</strong> - improved capability without forced change</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-teal mt-1">✓</span>
              <span><strong>Cumulative intelligence</strong> - each phase builds on the last</span>
            </li>
          </ul>
        </div>
      </Container>
    </section>
  );
}
