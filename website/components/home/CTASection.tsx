import { Container } from "@/components/layout/Container";
import { Button } from "@/components/ui/Button";
import { SITE_CONFIG } from "@/lib/constants";

export function CTASection() {
  return (
    <section className="py-20 bg-gradient-to-br from-navy via-navy to-teal text-white">
      <Container>
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">Learn More About the Architect of This Project</h2>
          <p className="text-xl text-white/90 mb-8">
            Interested in the strategic and technical thinking behind this implementation?
            Explore the convergence of enterprise strategy and AI engineering expertise.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button href="/about" variant="primary">
              View Profile
            </Button>
            <Button
              href={SITE_CONFIG.linkedin}
              variant="secondary"
              className="!border-white !text-white hover:!bg-white hover:!text-navy"
            >
              LinkedIn
            </Button>
            <Button
              href={SITE_CONFIG.github}
              variant="secondary"
              className="!border-white !text-white hover:!bg-white hover:!text-navy"
            >
              GitHub
            </Button>
          </div>
        </div>
      </Container>
    </section>
  );
}
