import Link from "next/link";
import { Container } from "./Container";
import { SITE_CONFIG } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="bg-navy text-white/80 py-12">
      <Container>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-bold text-white mb-4">AI Habitat Framework</h3>
            <p className="text-sm text-white/60">
              Bottom-up enterprise AI deployment through organic unit-level experimentation.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/" className="hover:text-teal focus:outline-none focus:text-teal focus:underline transition-colors rounded">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/solution" className="hover:text-teal focus:outline-none focus:text-teal focus:underline transition-colors rounded">
                  Phase Portal
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-teal focus:outline-none focus:text-teal focus:underline transition-colors rounded">
                  About
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white mb-4">Contact</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a
                  href={`mailto:${SITE_CONFIG.email}`}
                  className="hover:text-teal focus:outline-none focus:text-teal focus:underline transition-colors rounded"
                >
                  {SITE_CONFIG.email}
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/anthropics"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-teal focus:outline-none focus:text-teal focus:underline transition-colors rounded"
                >
                  GitHub
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-white/10 text-sm text-center text-white/60">
          <p>
            &copy; 2025 Daniel Dimick. Licensed under{' '}
            <a
              href="https://creativecommons.org/licenses/by-nc/4.0/"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-white/80"
            >
              CC BY-NC 4.0
            </a>{' '}
            for educational use.
          </p>
        </div>
      </Container>
    </footer>
  );
}
