"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Container } from "./Container";

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/challenge", label: "Challenge", dividerBefore: true },
  { href: "/strategy", label: "Strategy" },
  { href: "/transformation", label: "Transformation" },
  { href: "/solution", label: "Solution" },
  { href: "/results", label: "Results" },
  { href: "/about", label: "About", dividerBefore: true },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="sticky top-0 z-50 bg-navy border-b border-navy/10 backdrop-blur-sm">
      <Container>
        <div className="flex items-center justify-between h-24">
          <Link
            href="/"
            className="text-lg font-bold text-white hover:text-teal-on-navy transition-colors focus:outline-none focus:ring-2 focus:ring-teal-on-navy focus:ring-offset-2 focus:ring-offset-navy rounded whitespace-nowrap"
          >
            Daniel Dimick | Emergent Enterprise AI
          </Link>

          <div className="flex items-center gap-4 ml-8">
            {navLinks.map((link) => (
              <span key={link.href} className="flex items-center gap-5">
                {link.dividerBefore && (
                  <div className="h-4 w-px bg-white/30" />
                )}
              <Link
                href={link.href}
                className={cn(
                  "text-base font-medium transition-colors hover:text-teal-on-navy focus:outline-none focus:ring-2 focus:ring-teal-on-navy focus:ring-offset-2 focus:ring-offset-navy rounded px-1",
                  pathname === link.href ||
                    (link.href !== "/" && pathname.startsWith(link.href))
                    ? "text-teal-on-navy"
                    : "text-white/90"
                )}
              >
                {link.label}
              </Link>
              </span>
            ))}
          </div>
        </div>
      </Container>
    </nav>
  );
}
