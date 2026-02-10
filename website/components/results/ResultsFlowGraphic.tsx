"use client";

/**
 * Results Flow Graphic
 *
 * Shows the outcome journey of the case study:
 * Investment → Capabilities → Strategic Value → Production Ready
 */

const outcomes = [
  {
    value: "$163.1K",
    label: "Total Investment",
    sublabel: "$11.1K infrastructure",
    color: "bg-navy",
  },
  {
    value: "6",
    label: "Enterprise AI Capabilities",
    sublabel: "Search to orchestration",
    color: "bg-teal",
  },
  {
    value: "💎",
    label: "Proprietary Advantage",
    sublabel: "Institutional knowledge as AI advantage",
    color: "bg-amber",
  },
  {
    value: "✓",
    label: "Production Ready",
    sublabel: "Deploy to any environment",
    color: "bg-magenta",
  },
];

function Arrow() {
  return (
    <div className="hidden md:flex items-center justify-center px-2">
      <svg
        className="w-8 h-8 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M14 5l7 7m0 0l-7 7m7-7H3"
        />
      </svg>
    </div>
  );
}

export function ResultsFlowGraphic() {
  return (
    <div className="w-full">
      <div className="bg-gray-50 rounded-2xl shadow-xl border-2 border-gray-300 p-6 md:p-10">
        {/* Desktop Layout - Horizontal flow */}
        <div className="hidden md:flex items-stretch justify-between">
          {outcomes.map((outcome, idx) => (
            <div key={outcome.label} className="flex items-center">
              <div
                className={`${outcome.color} text-white rounded-xl p-6 min-w-[180px] text-center shadow-lg hover:brightness-110 transition-all duration-200`}
              >
                <div className="text-3xl font-bold mb-2">{outcome.value}</div>
                <div className="text-base font-semibold mb-1">{outcome.label}</div>
                <div className="text-sm opacity-80">{outcome.sublabel}</div>
              </div>
              {idx < outcomes.length - 1 && <Arrow />}
            </div>
          ))}
        </div>

        {/* Mobile Layout - Stacked with downward arrows */}
        <div className="md:hidden flex flex-col gap-3">
          {outcomes.map((outcome, idx) => (
            <div key={outcome.label}>
              <div
                className={`${outcome.color} text-white rounded-lg p-4 text-center shadow-lg`}
              >
                <div className="flex items-center justify-center gap-3">
                  <div className="text-2xl font-bold">{outcome.value}</div>
                  <div className="text-left">
                    <div className="text-sm font-semibold">{outcome.label}</div>
                    <div className="text-xs opacity-80">{outcome.sublabel}</div>
                  </div>
                </div>
              </div>
              {idx < outcomes.length - 1 && (
                <div className="flex justify-center py-2">
                  <svg
                    className="w-6 h-6 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 14l-7 7m0 0l-7-7m7 7V3"
                    />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Helpful hint text */}
      <div className="text-center mt-6">
        <p className="text-gray-700 text-lg font-medium">
          Scroll down to explore the complete breakdown
        </p>
        <div className="mt-3 animate-bounce">
          <svg
            className="w-6 h-6 mx-auto text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}
