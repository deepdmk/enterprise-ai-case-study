import { Container } from "@/components/layout/Container";
import { ValueProgressionBar } from "@/components/home/ValueProgressionBar";

export function HeroSection() {
  return (
    <section className="bg-gradient-to-br from-navy via-navy to-teal text-white py-20 md:py-24">
      <Container>
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
            Strategic AI Built From an Organization&apos;s Core
          </h1>
          <p className="text-lg md:text-xl lg:text-2xl text-white/90 max-w-4xl mx-auto leading-relaxed">
            A working demonstration showing how to build proprietary AI tailored to the
            organization with ROI and strategic optionality at every phase
          </p>

          <div className="border-t border-white/20 mt-10 pt-10">
            <h2 className="text-2xl font-bold text-white text-center mb-3">
              Building AI Capabilities Progressively
            </h2>
            <p className="text-lg text-white/90 text-center mb-8">
              Each phase delivers immediate value while building toward enterprise-wide orchestrated AI.
            </p>

            <ValueProgressionBar />
          </div>
        </div>
      </Container>
    </section>
  );
}
