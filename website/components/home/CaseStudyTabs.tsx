"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import { Card } from "@/components/ui/Card";
import { CaseJourneyGraphic } from "@/components/home/CaseJourneyGraphic";
import { TrendingUp, Sparkles, Cpu, Building2 } from "lucide-react";

export function CaseStudyTabs() {
  return (
    <div className="bg-gray-200 rounded-b-lg">
      <Tabs defaultValue="journey" className="w-full">
        <TabsList className="w-full justify-start bg-gray-300/50 rounded-none p-0 h-auto border-b border-gray-400">
          <TabsTrigger
            value="journey"
            className="rounded-none data-[state=active]:bg-gray-200 data-[state=active]:shadow-none px-8 py-4 text-base font-semibold data-[state=active]:border-b-2 data-[state=active]:border-navy"
          >
            The Journey
          </TabsTrigger>
          <TabsTrigger
            value="demonstrates"
            className="rounded-none data-[state=active]:bg-gray-200 data-[state=active]:shadow-none px-8 py-4 text-base font-semibold data-[state=active]:border-b-2 data-[state=active]:border-navy"
          >
            What This Demonstrates
          </TabsTrigger>
        </TabsList>

        <TabsContent value="journey" className="p-10 mt-0">
          <h3 className="text-xl font-bold text-navy text-center mb-6">
            Enterprise 18-month Journey from Strategy &rarr; Transformation
            &rarr; Deployment
          </h3>
          <CaseJourneyGraphic />
        </TabsContent>

        <TabsContent value="demonstrates" className="p-10 mt-0">
          <div className="bg-gradient-to-br from-teal/25 to-teal/15 py-10 pr-10 pl-12 rounded-lg border-l-4 border-teal">
            <h2 className="text-3xl font-bold text-navy mb-6">
              What This Case Study Demonstrates
            </h2>

            <p className="text-lg text-gray-700 leading-relaxed mb-10 max-w-4xl">
              This case study demonstrates capabilities across multiple domains —
              business strategy, organizational transformation, and technical
              implementation — as well as the synergistic value created when these
              disciplines work together. Strategic analysis informs transformation
              design, which shapes technical architecture. Equally, understanding
              downstream technical possibilities allows upstream phases to be
              honed for optionality — designing strategy that accommodates
              what&apos;s architecturally feasible, and shaping transformation to
              leverage what the technology enables. This bidirectional integration
              creates solutions no single discipline achieves alone.
            </p>

            <h3 className="text-xl font-semibold text-navy mb-6">
              What You&apos;ll Find
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <TrendingUp className="w-6 h-6 text-teal-on-light" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  Business Strategy &amp; Transformation
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Strategic analysis using established frameworks (Porter&apos;s
                  Five Forces, McKinsey 7S, SWOT, Pugh Matrix), consolidating
                  into Critical to Quality specifications and strategic approach
                  for transformation
                </p>
              </Card>

              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <Sparkles className="w-6 h-6 text-teal-on-light" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  Organizational Change &amp; Discovery
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Discovery-led transformation through Kaizen principles:
                  empowering staff at customer value creation points to target AI
                  uses where they add most value, building ownership and agency
                  through targeted experimentation, with phased optionality
                  enabling adaptation and pivots along the journey
                </p>
              </Card>

              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <Cpu className="w-6 h-6 text-teal-on-light" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  AI Engineering &amp; Technical Implementation
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Complete technical stack: fine-tuned SLMs using LoRA/QLoRA, MoE
                  division agents, custom embedding space for semantic search,
                  multi-agent orchestration with A2A protocol, full LLMOps
                  lifecycle from model training through production, leveraging
                  AGNO framework for seamless integration with AWS, Azure, and
                  other platforms
                </p>
              </Card>

              <Card className="p-6 bg-white rounded-xl shadow-md border border-teal/20 hover:border-teal/50 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
                <div className="w-12 h-12 bg-teal/10 rounded-lg flex items-center justify-center mb-4">
                  <Building2 className="w-6 h-6 text-teal-on-light" />
                </div>
                <h4 className="text-lg font-bold text-navy mb-3">
                  Enterprise Architecture &amp; System Design
                </h4>
                <p className="text-gray-600 text-base leading-relaxed">
                  Architecture designed for deployment optionality: feasible
                  self-deployment on local infrastructure, scalable deployment on
                  cloud platforms (AWS Bedrock, SageMaker, Azure), or integration
                  as sub-agent/tool with other enterprise solutions via AGNO — no
                  vendor lock-in, strategic flexibility preserved
                </p>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
