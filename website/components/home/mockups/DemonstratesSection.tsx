import { Card } from "@/components/ui/Card";
import { TrendingUp, Sparkles, Cpu, Building2 } from "lucide-react";

/**
 * MOCKUP: Balanced "What This Demonstrates" Section
 *
 * Changes from original:
 * - 2x2 grid instead of 4 columns
 * - Vertical card layout with more room for content
 * - Meaningful descriptions (not oversimplified)
 * - Cleaner intro paragraph
 */
export function DemonstratesSectionBalanced() {
  const capabilities = [
    {
      icon: TrendingUp,
      title: "Business Strategy & Transformation",
      description:
        "Strategic analysis using established frameworks (Porter's Five Forces, McKinsey 7S, SWOT, Pugh Matrix) consolidated into Critical to Quality specifications that drive the transformation approach.",
    },
    {
      icon: Sparkles,
      title: "Organizational Change & Discovery",
      description:
        "Discovery-led transformation through Kaizen principles: empowering staff at customer value creation points to target AI applications where they add most value, with phased optionality enabling adaptation along the journey.",
    },
    {
      icon: Cpu,
      title: "AI Engineering & Implementation",
      description:
        "Complete technical stack: fine-tuned SLMs using LoRA/QLoRA, MoE division agents, custom embedding space for semantic search, multi-agent orchestration with A2A protocol, and full LLMOps lifecycle from training through production.",
    },
    {
      icon: Building2,
      title: "Enterprise Architecture & Design",
      description:
        "Architecture designed for deployment optionality: self-hosted on local infrastructure, cloud deployment via AWS Bedrock/SageMaker or Azure, or integration as sub-agent with other enterprise solutions. No vendor lock-in.",
    },
  ];

  return (
    <div className="bg-gradient-to-br from-teal/20 to-teal/10 py-8 px-8 rounded-lg border-l-4 border-teal">
      <h2 className="text-2xl font-bold text-navy mb-3">
        What This Case Study Demonstrates
      </h2>

      <p className="text-base text-gray-700 leading-relaxed mb-6 max-w-4xl">
        Capabilities across business strategy, organizational transformation, and
        technical implementation, showing how bidirectional integration creates
        solutions no single discipline achieves alone. Strategic analysis informs
        transformation design, which shapes technical architecture, while
        understanding technical possibilities refines upstream decisions.
      </p>

      {/* 2x2 Grid - vertical cards with more content */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {capabilities.map((cap) => (
          <Card
            key={cap.title}
            className="p-5 bg-white rounded-xl shadow-sm border border-teal/20 hover:border-teal/40 hover:shadow-md transition-all duration-200"
          >
            <div className="flex items-start gap-4">
              <div className="w-11 h-11 bg-teal/10 rounded-lg flex items-center justify-center flex-shrink-0">
                <cap.icon className="w-6 h-6 text-teal-on-light" />
              </div>
              <div>
                <h4 className="text-base font-bold text-navy mb-2">
                  {cap.title}
                </h4>
                <p className="text-base text-gray-600 leading-relaxed">
                  {cap.description}
                </p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

/**
 * MOCKUP: Compact version (oversimplified - keeping for reference)
 */
export function DemonstratesSectionCompact() {
  const capabilities = [
    {
      icon: TrendingUp,
      title: "Business Strategy",
      description:
        "Porter's Five Forces, McKinsey 7S, SWOT analysis consolidated into CTQ specs and strategic approach",
    },
    {
      icon: Sparkles,
      title: "Organizational Change",
      description:
        "Kaizen-driven discovery empowering staff to identify high-value AI applications with phased optionality",
    },
    {
      icon: Cpu,
      title: "AI Engineering",
      description:
        "Fine-tuned SLMs, MoE agents, custom embeddings, A2A orchestration, full LLMOps lifecycle",
    },
    {
      icon: Building2,
      title: "Enterprise Architecture",
      description:
        "Deployment flexibility: self-hosted, AWS Bedrock/SageMaker, Azure, or integrated via AGNO",
    },
  ];

  return (
    <div className="bg-gradient-to-br from-teal/20 to-teal/10 py-8 px-8 rounded-lg border-l-4 border-teal">
      <h2 className="text-2xl font-bold text-navy mb-3">
        What This Case Study Demonstrates
      </h2>

      <p className="text-base text-gray-700 leading-relaxed mb-6 max-w-3xl">
        Capabilities across strategy, transformation, and technical implementation,
        showing how bidirectional integration creates solutions no single
        discipline achieves alone.
      </p>

      {/* 2x2 Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {capabilities.map((cap) => (
          <Card
            key={cap.title}
            className="p-4 bg-white rounded-lg shadow-sm border border-teal/20 hover:border-teal/40 hover:shadow-md transition-all duration-200"
          >
            <div className="flex gap-4">
              <div className="w-10 h-10 bg-teal/10 rounded-lg flex items-center justify-center flex-shrink-0">
                <cap.icon className="w-5 h-5 text-teal-on-light" />
              </div>
              <div>
                <h4 className="text-base font-bold text-navy mb-1">
                  {cap.title}
                </h4>
                <p className="text-base text-gray-600 leading-relaxed">
                  {cap.description}
                </p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

/**
 * VARIANT 2: Even more minimal - list style instead of cards
 */
export function DemonstratesSectionMinimal() {
  const capabilities = [
    {
      icon: TrendingUp,
      title: "Business Strategy",
      items: ["Porter's Five Forces", "McKinsey 7S", "SWOT", "CTQ Specs"],
    },
    {
      icon: Sparkles,
      title: "Organizational Change",
      items: ["Kaizen principles", "Discovery-led", "Phased optionality"],
    },
    {
      icon: Cpu,
      title: "AI Engineering",
      items: ["Fine-tuned SLMs", "MoE agents", "A2A protocol", "LLMOps"],
    },
    {
      icon: Building2,
      title: "Enterprise Architecture",
      items: ["Self-hosted", "AWS/Azure", "AGNO integration"],
    },
  ];

  return (
    <div className="bg-gradient-to-br from-teal/20 to-teal/10 py-8 px-8 rounded-lg border-l-4 border-teal">
      <h2 className="text-2xl font-bold text-navy mb-3">
        What This Case Study Demonstrates
      </h2>

      <p className="text-base text-gray-700 leading-relaxed mb-6 max-w-3xl">
        End-to-end capabilities where strategy informs transformation, which shapes
        architecture, and technical possibilities refine upstream decisions.
      </p>

      {/* 2x2 Grid - minimal style */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {capabilities.map((cap) => (
          <div key={cap.title} className="flex gap-3">
            <div className="w-9 h-9 bg-white rounded-lg flex items-center justify-center flex-shrink-0 shadow-sm">
              <cap.icon className="w-5 h-5 text-teal-on-light" />
            </div>
            <div>
              <h4 className="text-base font-bold text-navy mb-2">{cap.title}</h4>
              <div className="flex flex-wrap gap-1.5">
                {cap.items.map((item) => (
                  <span
                    key={item}
                    className="text-xs bg-white/80 text-gray-600 px-2 py-1 rounded"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
