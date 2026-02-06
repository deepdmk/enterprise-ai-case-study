import { Building2, Target, Lightbulb, Layers } from "lucide-react";

/**
 * MOCKUP B: Scannable Elevator Pitch
 *
 * Changes from original:
 * - Breaks dense paragraph into 4 scannable cards
 * - Each card has an icon, headline, and brief description
 * - Key metrics are visually highlighted
 * - Lighter background for visual breathing room
 */
export function ElevatorPitchScannable() {
  const points = [
    {
      icon: Building2,
      metric: "$1.3B",
      metricLabel: "Enterprise Scale",
      description:
        "International Project Services Enterprise with complex operations across multiple continents",
    },
    {
      icon: Target,
      metric: "100%",
      metricLabel: "Proprietary",
      description:
        "Custom AI capabilities tailored to the enterprise context, free from vendor platform dependencies",
    },
    {
      icon: Lightbulb,
      metric: "Discovery-Led",
      metricLabel: "Approach",
      description:
        "Capabilities emerge through use, not designed upfront. Strategy, transformation, and tech work together",
    },
    {
      icon: Layers,
      metric: "5 Phases",
      metricLabel: "Framework",
      description:
        "From unified knowledge space to orchestrated agentic AI, each phase delivers value",
    },
  ];

  return (
    <div className="bg-gray-100 pt-8 pb-12 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Section headline */}
        <div className="text-center mb-10">
          <h2 className="text-2xl md:text-3xl font-bold text-navy mb-3">
            Enterprise AI Without the Lock-In
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            This case study shows what&apos;s realistically achievable when strategy,
            transformation expertise, and technical implementation come together.
          </p>
        </div>

        {/* Scannable grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {points.map((point, index) => (
            <div
              key={index}
              className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md hover:border-teal/30 transition-all"
            >
              {/* Icon */}
              <div className="w-12 h-12 bg-navy/10 rounded-lg flex items-center justify-center mb-4">
                <point.icon className="w-6 h-6 text-navy" />
              </div>

              {/* Metric callout */}
              <div className="mb-3">
                <div className="text-2xl font-bold text-teal-on-light">
                  {point.metric}
                </div>
                <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                  {point.metricLabel}
                </div>
              </div>

              {/* Description */}
              <p className="text-gray-600 text-base leading-relaxed">
                {point.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
