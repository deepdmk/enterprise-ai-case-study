import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { ChevronLeft, ChevronRight, Grid } from "lucide-react";

interface PhaseNavProps {
  currentPhase: number;
}

export function PhaseNav({ currentPhase }: PhaseNavProps) {
  const phases = [
    { number: 0, slug: "phase-0", title: "Phase 0" },
    { number: 1, slug: "phase-1", title: "Phase 1" },
    { number: 2, slug: "phase-2", title: "Phase 2" },
    { number: 3, slug: "phase-3", title: "Phase 3" },
    { number: 4, slug: "phase-4", title: "Phase 4" },
    { number: 5, slug: "phase-5", title: "Phase 5" },
    { number: 6, slug: "scaling-production", title: "Scaling Production" },
  ];

  const currentIndex = phases.findIndex((p) => p.number === currentPhase);
  const prevPhase = currentIndex > 0 ? phases[currentIndex - 1] : null;
  const nextPhase = currentIndex < phases.length - 1 ? phases[currentIndex + 1] : null;

  return (
    <div className="border-t border-gray-200 py-8 mt-16">
      <Container>
        <div className="flex items-center justify-between">
          <div className="flex-1">
            {prevPhase && (
              <Link
                href={`/solution/${prevPhase.slug}`}
                className="inline-flex items-center gap-2 text-gray-600 hover:text-teal transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
                <span>{prevPhase.title}</span>
              </Link>
            )}
          </div>

          <Link
            href="/solution"
            className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:border-teal hover:text-teal transition-colors"
          >
            <Grid className="w-4 h-4" />
            <span>Portal</span>
          </Link>

          <div className="flex-1 text-right">
            {nextPhase && (
              <Link
                href={`/solution/${nextPhase.slug}`}
                className="inline-flex items-center gap-2 text-gray-600 hover:text-teal transition-colors"
              >
                <span>{nextPhase.title}</span>
                <ChevronRight className="w-5 h-5" />
              </Link>
            )}
          </div>
        </div>
      </Container>
    </div>
  );
}
