"use client";

import { useState } from "react";

const PughMatrixVisual = () => {
  const [activeTab, setActiveTab] = useState("stakeholder");

  // Primary CTQs: Stakeholder Requirements (S1-S8)
  const stakeholderCTQs = [
    {
      id: "S1",
      requirement: "Quarterly results + 5-year strategic optionality",
      vendorScore: -2,
      vendorNote: "3-4 years to ROI violates quarterly results requirement",
      customScore: -2,
      customNote:
        "18-24 month development + 6-12 deployment violates quarterly results",
      phasedScore: 2,
      phasedNote:
        "Value from Month 1 (quarterly) + 18-month transformation (5-year optionality)",
    },
    {
      id: "S2",
      requirement: "Decisive investment + exit ability at any phase",
      vendorScore: -2,
      vendorNote: "$2-5M upfront commitment, no exit optionality",
      customScore: -2,
      customNote: "$3-7M total commitment, cannot stop mid-development",
      phasedScore: 2,
      phasedNote:
        "Progressive investment with decision points at every horizon boundary",
    },
    {
      id: "S3",
      requirement: "Enterprise-wide intelligence + decentralized culture",
      vendorScore: -2,
      vendorNote:
        "Centralized rollout requires mandates, violates decentralized culture",
      customScore: -2,
      customNote:
        "Coordinated enterprise rollout impossible in decentralized structure",
      phasedScore: 2,
      phasedNote:
        "Enterprise capabilities through self-initiated country-by-country adoption",
    },
    {
      id: "S4",
      requirement: "Incremental delivery (value at every phase)",
      vendorScore: -1,
      vendorNote: "Value only after full deployment (3-4 years)",
      customScore: -2,
      customNote: "No value until complete system deployed (24-36 months)",
      phasedScore: 2,
      phasedNote:
        "Value delivered every phase, can stop at any phase with functioning capability",
    },
    {
      id: "S5",
      requirement: "Bounded risk (stop any phase, keep value)",
      vendorScore: -2,
      vendorNote: "All-or-nothing investment, sunk cost if stopped",
      customScore: -2,
      customNote:
        "Cannot stop mid-development without losing entire investment",
      phasedScore: 2,
      phasedNote:
        "Progressive de-risking: each phase delivers standalone value",
    },
    {
      id: "S6",
      requirement: "Bottom-up adoption (teams discover value)",
      vendorScore: -2,
      vendorNote: "Requires top-down mandates and standardized training",
      customScore: -2,
      customNote: "Mandatory enterprise-wide rollout required for ROI",
      phasedScore: 2,
      phasedNote:
        "Self-initiated adoption through peer demonstration and mission framing",
    },
    {
      id: "S7",
      requirement: "Customer choice (improved capability, no forced change)",
      vendorScore: -1,
      vendorNote: "Workflow changes required to use platform capabilities",
      customScore: -1,
      customNote: "Custom workflows may require client-facing changes",
      phasedScore: 2,
      phasedNote:
        "Capability enhancement only, zero workflow disruption required",
    },
    {
      id: "S8",
      requirement: "No vendor dependency (platform agnostic)",
      vendorScore: -2,
      vendorNote: "Complete vendor lock-in to platform and ecosystem",
      customScore: 0,
      customNote:
        "Platform agnostic but requires external consultants initially",
      phasedScore: 2,
      phasedNote:
        "Fully internal, platform-agnostic, no vendor dependencies",
    },
  ];

  // Supporting CTQs: Competitive Requirements (C1-C4)
  const competitiveCTQs = [
    {
      id: "C1",
      requirement: "Proprietary capabilities (non-commoditizable)",
      vendorScore: -2,
      vendorNote:
        "Platform available to all competitors, commoditizes advantage",
      customScore: 1,
      customNote: "Custom build creates proprietary capabilities",
      phasedScore: 2,
      phasedNote:
        "Proprietary AI built on unique 115-country institutional knowledge",
    },
    {
      id: "C2",
      requirement: "Dramatic efficiency gains (outperform lean competitors)",
      vendorScore: 0,
      vendorNote:
        "Standard efficiency gains available to all platform users",
      customScore: 1,
      customNote:
        "Custom optimization possible but requires specialist expertise",
      phasedScore: 2,
      phasedNote:
        "AI-speed knowledge access from trapped institutional expertise",
    },
    {
      id: "C3",
      requirement: "Defensible differentiation (non-substitutable)",
      vendorScore: -2,
      vendorNote:
        "Competitors can purchase same platform and capabilities",
      customScore: 1,
      customNote: "Custom capabilities harder to replicate",
      phasedScore: 2,
      phasedNote:
        "Differentiation competitors cannot purchase or quickly replicate",
    },
    {
      id: "C4",
      requirement: "Build with existing staff (not external AI talent)",
      vendorScore: -1,
      vendorNote:
        "Requires AI specialists for platform optimization and integration",
      customScore: -2,
      customNote:
        "Requires $1.5-3.75M for AI specialist recruitment (inaccessible)",
      phasedScore: 2,
      phasedNote:
        "Progressive upskilling of existing staff, no external AI talent needed",
    },
  ];

  // Supporting CTQs: Organizational Requirements (O1-O7)
  const organizationalCTQs = [
    {
      id: "O1",
      requirement: "Total investment <$1M",
      vendorScore: -2,
      vendorNote: "$2-5M exceeds budget constraint by 20-50x",
      customScore: -2,
      customNote: "$3-7M total exceeds budget constraint by 30-70x",
      phasedScore: 2,
      phasedNote: "$163.1K total investment well within constraint",
    },
    {
      id: "O2",
      requirement: "Decentralized self-initiated adoption (no mandates)",
      vendorScore: -2,
      vendorNote:
        "Centralized rollout requires mandates (organizationally impossible)",
      customScore: -2,
      customNote:
        "Coordinated deployment requires mandates (culturally impossible)",
      phasedScore: 2,
      phasedNote:
        "Country-by-country self-initiated adoption respecting autonomy",
    },
    {
      id: "O3",
      requirement: "Quick value with zero training prerequisites",
      vendorScore: -2,
      vendorNote: "Requires extensive training before value delivery",
      customScore: -1,
      customNote: "Training required for custom system usage",
      phasedScore: 2,
      phasedNote:
        "Immediate value with embedded learning, no prerequisites",
    },
    {
      id: "O4",
      requirement: "Four-language support from day one",
      vendorScore: -2,
      vendorNote: "English-only initially, excludes 90% of workforce",
      customScore: -1,
      customNote:
        "Multi-language possible but adds development complexity/cost",
      phasedScore: 2,
      phasedNote:
        "Four languages (English, French, Spanish, Portuguese) from Phase 1",
    },
    {
      id: "O5",
      requirement: "Leverage peer networks and mission framing",
      vendorScore: -1,
      vendorNote:
        "Corporate efficiency framing conflicts with mission culture",
      customScore: -1,
      customNote: "Technology framing conflicts with relational culture",
      phasedScore: 2,
      phasedNote:
        'Mission framing ("help more people faster") + peer demonstration',
    },
    {
      id: "O6",
      requirement: "Passive knowledge capture (no expert disruption)",
      vendorScore: -1,
      vendorNote:
        "Requires documentation and standardization (experts resist)",
      customScore: -1,
      customNote:
        "Requires expert participation in system design (creates resistance)",
      phasedScore: 2,
      phasedNote:
        "Captures knowledge from relational networks without expert disruption",
    },
    {
      id: "O7",
      requirement: "Respect strongly aligned cultural elements",
      vendorScore: -2,
      vendorNote: "Violates Style-Staff-Structure-Values alignment",
      customScore: -2,
      customNote:
        "Requires organizational change impossible on transformation timeline",
      phasedScore: 2,
      phasedNote:
        "Works with cultural alignment rather than requiring change",
    },
  ];

  const calculateSubtotal = (
    ctqs: typeof stakeholderCTQs,
    alternative: string
  ) => {
    return ctqs.reduce((sum, ctq) => {
      if (alternative === "vendor") return sum + ctq.vendorScore;
      if (alternative === "custom") return sum + ctq.customScore;
      if (alternative === "phased") return sum + ctq.phasedScore;
      return sum;
    }, 0);
  };

  const getCurrentCTQs = () => {
    if (activeTab === "stakeholder") return stakeholderCTQs;
    if (activeTab === "competitive") return competitiveCTQs;
    if (activeTab === "organizational") return organizationalCTQs;
    return [];
  };

  const getTabLabel = (tab: string) => {
    if (tab === "stakeholder") return "Primary: Stakeholder (S1-S8)";
    if (tab === "competitive") return "Supporting: Competitive (C1-C4)";
    if (tab === "organizational")
      return "Supporting: Organizational (O1-O7)";
    return "";
  };

  const getTabDescription = (tab: string) => {
    if (tab === "stakeholder")
      return "What stakeholders explicitly said they need";
    if (tab === "competitive") return "Porter's Five Forces validation";
    if (tab === "organizational") return "McKinsey 7S + SWOT validation";
    return "";
  };

  const getScoreColor = (score: number) => {
    if (score >= 2)
      return "bg-green-100 text-green-800 border border-green-300";
    if (score === 1)
      return "bg-green-50 text-green-700 border border-green-200";
    if (score === 0)
      return "bg-gray-100 text-gray-700 border border-gray-300";
    if (score === -1)
      return "bg-orange-50 text-orange-700 border border-orange-200";
    return "bg-red-100 text-red-800 border border-red-300";
  };

  const currentCTQs = getCurrentCTQs();
  const vendorSubtotal = calculateSubtotal(currentCTQs, "vendor");
  const customSubtotal = calculateSubtotal(currentCTQs, "custom");
  const phasedSubtotal = calculateSubtotal(currentCTQs, "phased");

  const vendorTotal =
    calculateSubtotal(stakeholderCTQs, "vendor") +
    calculateSubtotal(competitiveCTQs, "vendor") +
    calculateSubtotal(organizationalCTQs, "vendor");
  const customTotal =
    calculateSubtotal(stakeholderCTQs, "custom") +
    calculateSubtotal(competitiveCTQs, "custom") +
    calculateSubtotal(organizationalCTQs, "custom");
  const phasedTotal =
    calculateSubtotal(stakeholderCTQs, "phased") +
    calculateSubtotal(competitiveCTQs, "phased") +
    calculateSubtotal(organizationalCTQs, "phased");

  return (
    <div className="w-full max-w-7xl mx-auto p-6 bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="mb-8">
        <h3 className="text-2xl font-bold text-navy mb-3">
          Interactive Pugh Matrix Evaluation
        </h3>
        <p className="text-gray-600 text-lg">
          Detailed scoring of three alternatives against Critical-To-Quality
          requirements from stakeholder voice and analytical validation
        </p>
      </div>

      {/* Combined Totals Section - Shows final decision first */}
      <div className="mb-8 p-6 bg-navy/5 rounded-lg border border-navy/10">
        <h4 className="text-xl font-bold text-navy mb-4">
          Combined Totals Across All CTQs
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Vendor Platform */}
          <div className="text-center">
            <p className="text-base font-semibold text-gray-600 mb-2">
              Vendor Platform
            </p>
            <div className="bg-white rounded-lg p-4 border-2 border-red-300">
              <p className="text-4xl font-bold text-red-700 mb-2">
                {vendorTotal}
              </p>
              <p className="text-base text-red-600 font-semibold">REJECTED</p>
              <p className="text-base text-gray-600 mt-2">
                Fails stakeholder requirements
              </p>
            </div>
          </div>

          {/* Custom Big Bang */}
          <div className="text-center">
            <p className="text-base font-semibold text-gray-600 mb-2">
              Custom Big Bang
            </p>
            <div className="bg-white rounded-lg p-4 border-2 border-orange-300">
              <p className="text-4xl font-bold text-orange-700 mb-2">
                {customTotal}
              </p>
              <p className="text-base text-orange-600 font-semibold">
                REJECTED
              </p>
              <p className="text-base text-gray-600 mt-2">
                Fails stakeholder requirements
              </p>
            </div>
          </div>

          {/* Phased Internal Build */}
          <div className="text-center">
            <p className="text-base font-semibold text-gray-600 mb-2">
              Phased Internal Build
            </p>
            <div className="bg-white rounded-lg p-4 border-4 border-green-500 shadow-md">
              <p className="text-4xl font-bold text-green-700 mb-2">
                +{phasedTotal}
              </p>
              <p className="text-base text-green-600 font-semibold">
                SELECTED ✓
              </p>
              <p className="text-base text-gray-600 mt-2">
                Only viable solution
              </p>
            </div>
          </div>
        </div>

        {/* Breakdown by Category */}
        <div className="mt-6 p-4 bg-white rounded border border-gray-200">
          <h4 className="font-semibold text-navy mb-3">
            Score Breakdown by Category:
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-base">
            <div>
              <p className="font-medium text-gray-700 mb-1">
                Primary: Stakeholder
              </p>
              <p className="text-gray-600">
                Vendor: {calculateSubtotal(stakeholderCTQs, "vendor")} |
                Custom: {calculateSubtotal(stakeholderCTQs, "custom")} |
                Phased: +{calculateSubtotal(stakeholderCTQs, "phased")}
              </p>
            </div>
            <div>
              <p className="font-medium text-gray-700 mb-1">
                Supporting: Competitive
              </p>
              <p className="text-gray-600">
                Vendor: {calculateSubtotal(competitiveCTQs, "vendor")} |
                Custom: +{calculateSubtotal(competitiveCTQs, "custom")} |
                Phased: +{calculateSubtotal(competitiveCTQs, "phased")}
              </p>
            </div>
            <div>
              <p className="font-medium text-gray-700 mb-1">
                Supporting: Organizational
              </p>
              <p className="text-gray-600">
                Vendor: {calculateSubtotal(organizationalCTQs, "vendor")} |
                Custom: {calculateSubtotal(organizationalCTQs, "custom")} |
                Phased: +{calculateSubtotal(organizationalCTQs, "phased")}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs - Select which CTQ category to explore */}
      <div className="flex flex-col sm:flex-row gap-2 mb-8">
        {(["stakeholder", "competitive", "organizational"] as const).map(
          (tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex-1 px-4 py-3 font-bold text-sm sm:text-base rounded-lg transition-all border-2 ${
                activeTab === tab
                  ? "bg-navy text-white border-navy shadow-md"
                  : "bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100 hover:border-gray-300"
              }`}
            >
              {getTabLabel(tab)}
            </button>
          )
        )}
      </div>

      {/* Tab Description */}
      <div className="mb-6 p-4 bg-navy/5 border-l-4 border-navy rounded">
        <p className="text-navy font-medium">
          {getTabDescription(activeTab)}
        </p>
      </div>

      {/* Pugh Matrix Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-navy text-white">
              <th className="border border-navy/70 p-3 text-left font-semibold w-64">
                CTQ Requirement
              </th>
              <th className="border border-navy/70 p-3 text-center font-semibold w-32">
                Vendor Platform
              </th>
              <th className="border border-navy/70 p-3 text-center font-semibold w-32">
                Custom Big Bang
              </th>
              <th className="border border-navy/70 p-3 text-center font-semibold w-32">
                Phased Internal Build
              </th>
            </tr>
          </thead>
          <tbody>
            {currentCTQs.map((ctq, index) => (
              <tr
                key={ctq.id}
                className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}
              >
                <td className="border border-gray-200 p-3">
                  <span className="font-semibold text-navy">{ctq.id}:</span>{" "}
                  <span className="text-gray-700">{ctq.requirement}</span>
                </td>
                <td className="border border-gray-200 p-3">
                  <div className="flex flex-col items-center space-y-2">
                    <span
                      className={`px-3 py-1 rounded font-bold ${getScoreColor(ctq.vendorScore)}`}
                    >
                      {ctq.vendorScore > 0 ? "+" : ""}
                      {ctq.vendorScore}
                    </span>
                    <p className="text-xs text-gray-600 text-center">
                      {ctq.vendorNote}
                    </p>
                  </div>
                </td>
                <td className="border border-gray-200 p-3">
                  <div className="flex flex-col items-center space-y-2">
                    <span
                      className={`px-3 py-1 rounded font-bold ${getScoreColor(ctq.customScore)}`}
                    >
                      {ctq.customScore > 0 ? "+" : ""}
                      {ctq.customScore}
                    </span>
                    <p className="text-xs text-gray-600 text-center">
                      {ctq.customNote}
                    </p>
                  </div>
                </td>
                <td className="border border-gray-200 p-3">
                  <div className="flex flex-col items-center space-y-2">
                    <span
                      className={`px-3 py-1 rounded font-bold ${getScoreColor(ctq.phasedScore)}`}
                    >
                      {ctq.phasedScore > 0 ? "+" : ""}
                      {ctq.phasedScore}
                    </span>
                    <p className="text-xs text-gray-600 text-center">
                      {ctq.phasedNote}
                    </p>
                  </div>
                </td>
              </tr>
            ))}
            {/* Subtotal Row */}
            <tr className="bg-navy/10 font-bold">
              <td className="border border-gray-200 p-3 text-right text-navy">
                {getTabLabel(activeTab)} Subtotal:
              </td>
              <td className="border border-gray-200 p-3 text-center">
                <span
                  className={`px-4 py-2 rounded font-bold text-lg ${getScoreColor(vendorSubtotal)}`}
                >
                  {vendorSubtotal > 0 ? "+" : ""}
                  {vendorSubtotal}
                </span>
              </td>
              <td className="border border-gray-200 p-3 text-center">
                <span
                  className={`px-4 py-2 rounded font-bold text-lg ${getScoreColor(customSubtotal)}`}
                >
                  {customSubtotal > 0 ? "+" : ""}
                  {customSubtotal}
                </span>
              </td>
              <td className="border border-gray-200 p-3 text-center">
                <span
                  className={`px-4 py-2 rounded font-bold text-lg ${getScoreColor(phasedSubtotal)}`}
                >
                  {phasedSubtotal > 0 ? "+" : ""}
                  {phasedSubtotal}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export { PughMatrixVisual };
export default PughMatrixVisual;
