"use client";

import Link from "next/link";
import { Container } from "@/components/layout/Container";
import { ChevronLeft, ChevronRight } from "lucide-react";

const pages = [
  { slug: "/", label: "Home" },
  { slug: "/challenge", label: "Challenge" },
  { slug: "/strategy", label: "Strategy" },
  { slug: "/transformation", label: "Transformation" },
  { slug: "/solution", label: "Solution" },
  { slug: "/results", label: "Results" },
];

interface PageNavProps {
  current: string;
}

export function PageNav({ current }: PageNavProps) {
  const currentIndex = pages.findIndex((p) => p.slug === current);
  const prev = currentIndex > 0 ? pages[currentIndex - 1] : null;
  const next = currentIndex < pages.length - 1 ? pages[currentIndex + 1] : null;

  return (
    <div className="bg-slate-200 border-b border-gray-200 py-2">
      <Container>
        <div className="flex items-center justify-between">
          <div className="flex-1">
            {prev && (
              <Link
                href={prev.slug}
                className="inline-flex items-center gap-2 font-semibold text-gray-600 hover:text-teal transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
                <span>{prev.label}</span>
              </Link>
            )}
          </div>

          <div className="flex-1 text-right">
            {next && (
              <Link
                href={next.slug}
                className="inline-flex items-center gap-2 font-semibold text-gray-600 hover:text-teal transition-colors"
              >
                <span>{next.label}</span>
                <ChevronRight className="w-5 h-5" />
              </Link>
            )}
          </div>
        </div>
      </Container>
    </div>
  );
}
