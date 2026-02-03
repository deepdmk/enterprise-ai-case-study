"use client";

import { useState } from "react";

const elements = {
  strategy: {
    title: "Strategy",
    category: "Hard",
    keyFindings: [
      "Institutional knowledge (115 countries) is primary competitive asset but trapped in silos",
      "Strategic assets: Deep domain expertise, multi-cultural capabilities, established relationships",
      "Resource constraints: Severe budget limitations, AI talent expensive and not integrated",
    ],
    misalignment:
      "Knowledge is strategic asset but organizationally inaccessible (Strategy-Skills-Systems-Staff misaligned)",
  },
  structure: {
    title: "Structure",
    category: "Hard",
    keyFindings: [
      "Multi-layered decentralization: HQ → Regional → Country offices with local autonomy",
      "Decision-making: Country directors control operations based on local context",
      "Coordination capacity: Minimal for enterprise-wide initiatives",
    ],
    misalignment:
      "Decentralized structure enables local responsiveness but prevents coordinated enterprise initiatives",
  },
  systems: {
    title: "Systems",
    category: "Hard",
    keyFindings: [
      "Technology precedent: One major transformation failure (ERP + logistics)",
      "Relational culture, not process culture; systems rely on individual knowledge",
      "Four organizational languages (60% non-English workforce)",
    ],
    misalignment:
      "Needs better systems to scale knowledge but failed precedent creates resistance",
  },
  style: {
    title: "Style",
    category: "Soft",
    keyFindings: [
      "Bottom-up, relational, consensus-driven; 'forgiveness better than permission'",
      "Personality-centric: Systems designed around people rather than standardized practices",
      "Influence through peer relationships; headquarters communications carry limited weight",
    ],
    misalignment:
      "Strong alignment with Structure, Staff, Values makes top-down approaches impossible",
  },
  staff: {
    title: "Staff",
    category: "Soft",
    keyFindings: [
      "Change-fatigued following layoffs, failed systems; trust eroded",
      "90% non-native English speakers living outside US; globally distributed",
      "Mission-driven (social impact, not compensation); intrinsically motivated",
    ],
    misalignment:
      "Mission-driven motivation is strength but change fatigue is weakness",
  },
  skills: {
    title: "Skills",
    category: "Soft",
    keyFindings: [
      "Deep institutional knowledge trapped in silos due to lack of processes/systems",
      "Knowledge access is relational (people networks) not systemic (documented)",
      "Experts won't voluntarily document knowledge; see it as personal value",
    ],
    misalignment:
      "Greatest strategic asset (institutional knowledge) organizationally inaccessible - unusable strength",
  },
  sharedValues: {
    title: "Shared Values",
    category: "Core",
    keyFindings: [
      "Mission-driven, non-corporate, relationship-centric identity",
      "Trust-based collaboration over control; human relationships over process efficiency",
      "Corporate efficiency/standardization language triggers resistance",
    ],
    misalignment:
      "Powerful alignment with Style, Staff, Structure creates coherent cultural architecture",
  },
};

type ElementKey = keyof typeof elements;

function ElementBox({
  elementKey,
  element,
  isSelected,
  onClick,
}: {
  elementKey: string;
  element: (typeof elements)[ElementKey];
  isSelected: boolean;
  onClick: () => void;
}) {
  const colorClass =
    element.category === "Hard"
      ? "bg-blue-500"
      : element.category === "Soft"
        ? "bg-orange-500"
        : "bg-purple-600";

  return (
    <div
      className="cursor-pointer transform transition-all hover:scale-105"
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onClick();
        }
      }}
      aria-label={`${element.title} - ${element.category} element. Click to view details.`}
    >
      <div
        className={`${colorClass} text-white px-3 py-2 rounded-t text-center`}
      >
        <div className="font-bold text-sm">{element.title}</div>
        <div className="text-xs opacity-90">{element.category}</div>
      </div>
      <div
        className={`bg-white border-2 ${isSelected ? "border-gray-800 shadow-xl" : "border-gray-300"} rounded-b p-3 min-h-[100px]`}
      >
        <p className="text-xs text-gray-700 leading-tight">
          {element.keyFindings[0]}
        </p>
      </div>
    </div>
  );
}

export function McKinsey7SVisual() {
  const [selectedElement, setSelectedElement] = useState<ElementKey | null>(
    null,
  );

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* 7S Diamond Structure */}
      <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
        <div className="max-w-4xl mx-auto relative">
          {/* SVG Connection Lines */}
          <svg
            className="absolute inset-0 w-full h-full pointer-events-none"
            style={{ zIndex: 0 }}
          >
            <line
              x1="50%"
              y1="38%"
              x2="50%"
              y2="8%"
              stroke="#cbd5e1"
              strokeWidth="2"
            />
            <line
              x1="50%"
              y1="38%"
              x2="16%"
              y2="23%"
              stroke="#cbd5e1"
              strokeWidth="2"
            />
            <line
              x1="50%"
              y1="38%"
              x2="84%"
              y2="23%"
              stroke="#cbd5e1"
              strokeWidth="2"
            />
            <line
              x1="50%"
              y1="38%"
              x2="16%"
              y2="53%"
              stroke="#cbd5e1"
              strokeWidth="2"
            />
            <line
              x1="50%"
              y1="38%"
              x2="84%"
              y2="53%"
              stroke="#cbd5e1"
              strokeWidth="2"
            />
            <line
              x1="50%"
              y1="38%"
              x2="50%"
              y2="68%"
              stroke="#cbd5e1"
              strokeWidth="2"
            />
            <line
              x1="50%"
              y1="8%"
              x2="16%"
              y2="23%"
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray="4"
            />
            <line
              x1="50%"
              y1="8%"
              x2="84%"
              y2="23%"
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray="4"
            />
            <line
              x1="16%"
              y1="23%"
              x2="16%"
              y2="53%"
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray="4"
            />
            <line
              x1="84%"
              y1="23%"
              x2="84%"
              y2="53%"
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray="4"
            />
            <line
              x1="16%"
              y1="53%"
              x2="50%"
              y2="68%"
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray="4"
            />
            <line
              x1="84%"
              y1="53%"
              x2="50%"
              y2="68%"
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray="4"
            />
          </svg>

          {/* Row 1: Strategy (centered) */}
          <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
            <div></div>
            <ElementBox
              elementKey="strategy"
              element={elements.strategy}
              isSelected={selectedElement === "strategy"}
              onClick={() =>
                setSelectedElement(
                  selectedElement === "strategy" ? null : "strategy",
                )
              }
            />
            <div></div>
          </div>

          {/* Row 2: Structure and Systems */}
          <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
            <ElementBox
              elementKey="structure"
              element={elements.structure}
              isSelected={selectedElement === "structure"}
              onClick={() =>
                setSelectedElement(
                  selectedElement === "structure" ? null : "structure",
                )
              }
            />
            <div></div>
            <ElementBox
              elementKey="systems"
              element={elements.systems}
              isSelected={selectedElement === "systems"}
              onClick={() =>
                setSelectedElement(
                  selectedElement === "systems" ? null : "systems",
                )
              }
            />
          </div>

          {/* Row 3: Shared Values (centered) */}
          <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
            <div></div>
            <ElementBox
              elementKey="sharedValues"
              element={elements.sharedValues}
              isSelected={selectedElement === "sharedValues"}
              onClick={() =>
                setSelectedElement(
                  selectedElement === "sharedValues" ? null : "sharedValues",
                )
              }
            />
            <div></div>
          </div>

          {/* Row 4: Style and Skills */}
          <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
            <ElementBox
              elementKey="style"
              element={elements.style}
              isSelected={selectedElement === "style"}
              onClick={() =>
                setSelectedElement(
                  selectedElement === "style" ? null : "style",
                )
              }
            />
            <div></div>
            <ElementBox
              elementKey="skills"
              element={elements.skills}
              isSelected={selectedElement === "skills"}
              onClick={() =>
                setSelectedElement(
                  selectedElement === "skills" ? null : "skills",
                )
              }
            />
          </div>

          {/* Row 5: Staff (centered) */}
          <div className="grid grid-cols-3 gap-4 relative z-10">
            <div></div>
            <ElementBox
              elementKey="staff"
              element={elements.staff}
              isSelected={selectedElement === "staff"}
              onClick={() =>
                setSelectedElement(
                  selectedElement === "staff" ? null : "staff",
                )
              }
            />
            <div></div>
          </div>
        </div>
      </div>

      {/* Element Details Panel */}
      {selectedElement && (
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-300 rounded-lg p-6 mb-8">
          <h3 className="text-xl font-bold text-indigo-900 mb-3">
            {elements[selectedElement].title} - Detailed Assessment
          </h3>
          <div className="bg-white rounded-lg p-4 mb-3">
            <p className="text-base font-semibold text-gray-700 mb-2">
              Key Findings:
            </p>
            <ul className="space-y-2">
              {elements[selectedElement].keyFindings.map((finding, idx) => (
                <li key={idx} className="text-base text-gray-800">
                  &bull; {finding}
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white rounded-lg p-4 border-l-4 border-indigo-500">
            <p className="text-base font-semibold text-gray-700 mb-1">
              Critical Interdependency:
            </p>
            <p className="text-base text-gray-800 italic">
              {elements[selectedElement].misalignment}
            </p>
          </div>
        </div>
      )}

      {/* Alignment Summary */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-green-50 border-2 border-green-500 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="bg-green-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
              Strong Alignment
            </span>
          </div>
          <h3 className="text-lg font-bold text-gray-900 mb-2">
            Bottom-Up Cultural Coherence
          </h3>
          <p className="text-base text-gray-700 mb-3 font-mono">
            Style + Structure + Staff + Shared Values
          </p>
          <p className="text-base text-gray-800 italic">
            When change approaches align with this cultural architecture, peer
            networks accelerate adoption faster than top-down mandates ever
            could
          </p>
        </div>

        <div className="bg-red-50 border-2 border-red-500 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-3">
            <span className="bg-red-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
              Critical Misalignment
            </span>
          </div>
          <h3 className="text-lg font-bold text-gray-900 mb-2">
            Trapped Knowledge
          </h3>
          <p className="text-base text-gray-700 mb-3 font-mono">
            Strategy &ne; Skills &ne; Systems &ne; Staff
          </p>
          <p className="text-base text-gray-800 italic">
            Greatest strategic asset organizationally inaccessible. Four
            elements misaligned around knowledge accessibility - cannot fix by
            changing one element
          </p>
        </div>
      </div>
    </div>
  );
}
