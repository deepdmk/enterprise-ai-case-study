"use client";

import { IntensityBadge } from "./IntensityBadge";

interface ForceData {
  title: string;
  subtitle?: string;
  intensity: "HIGH" | "MOD-HIGH" | "MODERATE";
  trend: string;
  color: string;
  details: string[];
}

const forces: Record<string, ForceData> = {
  center: {
    title: "Competitive Rivalry",
    intensity: "HIGH",
    trend: "Intensifying",
    color: "bg-red-500",
    details: [
      "Market consolidation transformed coexistence to direct confrontation",
      "Traditional business development spending ceased in some areas while oversaturating many remaining areas",
      "Talent market saturated with laid-off talent (outside AI)",
      "Resources diminished substantially; oversaturation in remaining strategic areas",
      "Price pressure as competitors undercut for survival",
    ],
  },
  top: {
    title: "Threat of Substitutes",
    intensity: "HIGH",
    trend: "Critical",
    color: "bg-red-500",
    details: [
      "AI eliminated operational complexity barriers (finance, supply chain, compliance)",
      "Lean local competitors competitive with narrower knowledge but higher efficiency",
      "Large organizations can no longer use extensive knowledge inefficiently",
      "Middle interpretation layers easier with AI tools",
      "Must extract dramatically more value from knowledge than lean competitors",
    ],
  },
  bottom: {
    title: "Threat of New Entrants",
    intensity: "HIGH",
    trend: "Increasing",
    color: "bg-red-500",
    details: [
      "AI drastically reduced institutional knowledge barriers (regulations, funder processes)",
      "Local niche players leverage local talent at local price points",
      "Focus on single country/area vs. global footprint for efficiency",
      "Scale up/down rapidly making them highly agile",
      "Acceptable quality through localization without international overheads",
    ],
  },
  left: {
    title: "Bargaining Power of Suppliers",
    subtitle: "(Talent Market)",
    intensity: "HIGH",
    trend: "Critical",
    color: "bg-red-500",
    details: [
      "Very few AI-skilled professionals in sector (not competitive for such talent)",
      "Sector structurally cannot compete with private sector compensation",
      "Upheaval eliminated stability advantage; strong talent leaving for other markets",
      "Premium compensation cannot attract strong talent from other sectors",
      "Must build internally with existing staff, not recruit AI expertise",
    ],
  },
  right: {
    title: "Bargaining Power of Buyers",
    subtitle: "(Clients, Funders, Government)",
    intensity: "MOD-HIGH",
    trend: "Stable",
    color: "bg-orange-500",
    details: [
      "Clients increasingly price sensitive, expect reduced costs and overheads",
      "Demand consistency while responsive to quality if without cost increase",
      "Resist disruption to established methods",
      "Funders nervous post-crisis, demand prudent spending with innovation evidence",
      "115+ countries with diverse regulatory, compliance, and cultural requirements",
    ],
  },
};

interface ForceCardProps {
  force: ForceData;
  position: "center" | "top" | "bottom" | "left" | "right";
}

function ForceCard({ force, position }: ForceCardProps) {
  const positionClasses: Record<string, string> = {
    center: "col-span-2 row-span-2 col-start-2 row-start-2",
    top: "col-span-2 col-start-2 row-start-1",
    bottom: "col-span-2 col-start-2 row-start-4",
    left: "col-start-1 row-span-2 row-start-2",
    right: "col-start-4 row-span-2 row-start-2",
  };

  return (
    <div className={`${positionClasses[position]} flex items-center justify-center`}>
      <div className="p-6 bg-white rounded-lg shadow-lg border-2 border-gray-200 hover:shadow-xl transition-shadow w-full h-full flex flex-col">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3
              className={`font-bold ${
                position === "center" ? "text-xl" : "text-lg"
              } text-gray-900 mb-1`}
            >
              {force.title}
            </h3>
            {force.subtitle && (
              <p className="text-base text-gray-600 italic">{force.subtitle}</p>
            )}
          </div>
          <IntensityBadge intensity={force.intensity} className="ml-2" />
        </div>

        <div className="mb-3">
          <span className="text-xs text-gray-500 font-medium">Trend: </span>
          <span className="text-xs text-gray-700 font-semibold">{force.trend}</span>
        </div>

        <ul className="space-y-2 flex-1">
          {force.details.map((detail, idx) => (
            <li key={idx} className="text-base text-gray-700 flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>{detail}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export function PortersFiveForcesVisual() {
  return (
    <div className="w-full">
      {/* Main Grid - Desktop */}
      <div
        className="hidden lg:grid grid-cols-4 grid-rows-4 gap-4 mb-8"
        style={{ minHeight: "800px" }}
      >
        <ForceCard force={forces.center} position="center" />
        <ForceCard force={forces.top} position="top" />
        <ForceCard force={forces.bottom} position="bottom" />
        <ForceCard force={forces.left} position="left" />
        <ForceCard force={forces.right} position="right" />
      </div>

      {/* Mobile Layout - Stacked Cards */}
      <div className="lg:hidden space-y-4 mb-8">
        {/* Center force first */}
        <div className="p-6 bg-white rounded-lg shadow-lg border-2 border-gray-200">
          <div className="flex items-start justify-between mb-3">
            <h3 className="font-bold text-xl text-gray-900">{forces.center.title}</h3>
            <IntensityBadge intensity={forces.center.intensity} />
          </div>
          <div className="mb-3">
            <span className="text-xs text-gray-500 font-medium">Trend: </span>
            <span className="text-xs text-gray-700 font-semibold">
              {forces.center.trend}
            </span>
          </div>
          <ul className="space-y-2">
            {forces.center.details.map((detail, idx) => (
              <li key={idx} className="text-base text-gray-700 flex items-start">
                <span className="text-blue-600 mr-2">•</span>
                <span>{detail}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Other forces */}
        {(["top", "bottom", "left", "right"] as const).map((pos) => (
          <div
            key={pos}
            className="p-6 bg-white rounded-lg shadow-lg border-2 border-gray-200"
          >
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="font-bold text-lg text-gray-900">
                  {forces[pos].title}
                </h3>
                {forces[pos].subtitle && (
                  <p className="text-base text-gray-600 italic">
                    {forces[pos].subtitle}
                  </p>
                )}
              </div>
              <IntensityBadge intensity={forces[pos].intensity} />
            </div>
            <div className="mb-3">
              <span className="text-xs text-gray-500 font-medium">Trend: </span>
              <span className="text-xs text-gray-700 font-semibold">
                {forces[pos].trend}
              </span>
            </div>
            <ul className="space-y-2">
              {forces[pos].details.map((detail, idx) => (
                <li key={idx} className="text-base text-gray-700 flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  <span>{detail}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Strategic Insight Box */}
      <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-bold text-blue-900 mb-3">
          Strategic Convergence Point
        </h3>
        <p className="text-gray-800 mb-4">
          All five forces converged on a single vulnerability:{" "}
          <span className="font-semibold">
            institutional knowledge trapped in silos and used inefficiently
          </span>
          . This knowledge represented the only sustainable competitive advantage but
          was inaccessible at the speed and scale needed to compete against AI-enabled
          rivals. AI eliminated operational complexity barriers that previously
          protected inefficient knowledge use, creating vulnerability to lean local
          competitors operating with less knowledge but higher efficiency.
        </p>
        <div className="bg-white rounded p-4 border border-blue-200">
          <p className="text-base font-semibold text-gray-900 mb-2">
            Strategic Imperative:
          </p>
          <p className="text-base text-gray-700">
            Transform trapped institutional knowledge into accessible, proprietary
            competitive advantage through AI that: competitors cannot purchase, new
            entrants cannot replicate, vendor platforms cannot substitute, and
            dramatically increases efficiency of knowledge utilization. Must extract
            far more value from extensive institutional knowledge than lean local
            competitors can extract from narrow knowledge.
          </p>
        </div>
      </div>

      {/* Force Intensity Matrix */}
      <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Force Intensity Matrix</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-gray-300">
                <th className="text-left py-3 px-4 font-semibold text-gray-900">
                  Force
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">
                  Intensity
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">
                  Trend
                </th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900">
                  Strategic Impact
                </th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-gray-200 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">Competitive Rivalry</td>
                <td className="py-3 px-4">
                  <IntensityBadge intensity="HIGH" />
                </td>
                <td className="py-3 px-4 text-gray-700">Intensifying</td>
                <td className="py-3 px-4 text-gray-700">
                  Demands differentiation strategy
                </td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">Threat of New Entrants</td>
                <td className="py-3 px-4">
                  <IntensityBadge intensity="HIGH" />
                </td>
                <td className="py-3 px-4 text-gray-700">Increasing</td>
                <td className="py-3 px-4 text-gray-700">
                  Requires non-replicable advantages
                </td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">Bargaining Power of Buyers</td>
                <td className="py-3 px-4">
                  <IntensityBadge intensity="MOD-HIGH" />
                </td>
                <td className="py-3 px-4 text-gray-700">Stable</td>
                <td className="py-3 px-4 text-gray-700">
                  Must preserve relationships, demonstrate value efficiently
                </td>
              </tr>
              <tr className="border-b border-gray-200 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">Bargaining Power of Suppliers</td>
                <td className="py-3 px-4">
                  <IntensityBadge intensity="HIGH" />
                </td>
                <td className="py-3 px-4 text-gray-700">Critical</td>
                <td className="py-3 px-4 text-gray-700">
                  Must build internally with existing staff
                </td>
              </tr>
              <tr className="hover:bg-gray-50">
                <td className="py-3 px-4 font-medium">Threat of Substitutes</td>
                <td className="py-3 px-4">
                  <IntensityBadge intensity="HIGH" />
                </td>
                <td className="py-3 px-4 text-gray-700">Critical</td>
                <td className="py-3 px-4 text-gray-700">Must avoid commoditization</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Competitive Advantage Analysis */}
      <div className="mt-8 grid md:grid-cols-2 gap-6">
        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-red-900 mb-4">
            Unsustainable Advantages (Vulnerable to Forces)
          </h3>
          <ul className="space-y-2">
            <li className="text-base text-gray-700">
              • Price competitiveness (lean local entrants have 30-40% lower costs)
            </li>
            <li className="text-base text-gray-700">
              • Speed/agility (lean entrants scale up/down rapidly, no legacy
              constraints)
            </li>
            <li className="text-base text-gray-700">
              • Operational complexity barriers (AI eliminated finance, supply chain,
              compliance advantages)
            </li>
            <li className="text-base text-gray-700">
              • Vendor-platform capabilities (substitutable/commoditizable, level
              playing field)
            </li>
            <li className="text-base text-gray-700">
              • Premium AI talent (sector cannot compete with private sector
              compensation)
            </li>
          </ul>
        </div>

        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-bold text-green-900 mb-4">
            Sustainable Advantage (If Leveraged Efficiently)
          </h3>
          <ul className="space-y-2">
            <li className="text-base text-gray-700">
              • Institutional knowledge from 115 countries (scale lean competitors
              cannot match)
            </li>
            <li className="text-base text-gray-700">
              • Deep client relationships built over decades
            </li>
            <li className="text-base text-gray-700">
              • Contextual expertise across diverse regulatory environments
            </li>
            <li className="text-base text-gray-700">
              • Proprietary data from organizational operations
            </li>
            <li className="text-base text-gray-700">
              <span className="font-semibold">Critical requirement:</span> Must be made
              accessible and used efficiently through AI
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
