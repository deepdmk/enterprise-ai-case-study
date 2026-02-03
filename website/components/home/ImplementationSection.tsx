import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { PHASES } from "@/lib/constants";
import { ArrowRight } from "lucide-react";

export function ImplementationSection() {
  const colorMap = {
    navy: "bg-navy",
    teal: "bg-teal",
    amber: "bg-amber",
    magenta: "bg-magenta",
  };

  return (
    <section className="py-20">
      <Container>
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-navy mb-4">
            Six-Phase Implementation
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Six phases of progressive capability building with value delivered at each stage
            and optionality maintained throughout. Click any phase for details.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {PHASES.map((phase) => (
            <Link key={phase.number} href={`/solution/${phase.slug}`}>
              <Card hover className="h-full">
                <div className="flex items-start gap-4">
                  <div
                    className={`${colorMap[phase.color]} text-white text-2xl font-bold w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0`}
                  >
                    {phase.number}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-navy mb-1">
                      {phase.title}
                    </h3>
                    <p className="text-base text-gray-600">{phase.subtitle}</p>
                    <p className="text-base text-gray-500 mt-2">{phase.description}</p>
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>

        <div className="text-center">
          <Link
            href="/solution"
            className="inline-flex items-center gap-2 text-teal font-semibold hover:gap-4 focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2 rounded transition-all"
          >
            Explore the Full Implementation
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </Container>
    </section>
  );
}
