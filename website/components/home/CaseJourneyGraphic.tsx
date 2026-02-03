export function CaseJourneyGraphic() {
  return (
    <div className="w-full overflow-x-auto">
      <div className="min-w-[900px]">
        {/* Top Chevrons (pointing right) */}
        <div className="flex items-stretch mb-8">
          <div className="flex-1 relative">
            <div
              className="bg-navy text-white px-6 py-3 text-center font-semibold text-base"
              style={{
                clipPath: "polygon(0 0, calc(100% - 16px) 0, 100% 50%, calc(100% - 16px) 100%, 0 100%)",
                paddingRight: "24px",
              }}
            >
              Strategic Analysis
            </div>
          </div>
          <div className="flex-1 relative -ml-4">
            <div
              className="bg-teal text-white px-8 py-3 text-center font-semibold text-base"
              style={{
                clipPath: "polygon(0 0, calc(100% - 16px) 0, 100% 50%, calc(100% - 16px) 100%, 0 100%, 16px 50%)",
                paddingLeft: "28px",
                paddingRight: "24px",
              }}
            >
              Transformation Framework
            </div>
          </div>
          <div className="flex-1 relative -ml-4">
            <div
              className="bg-amber text-white px-8 py-3 text-center font-semibold text-base"
              style={{
                clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%, 16px 50%)",
                paddingLeft: "28px",
              }}
            >
              Scale Deployment &amp; Optionality
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex gap-6">
          {/* Left: Strategic Priorities with bracket (Navy) */}
          <div className="flex items-stretch">
            <div className="flex flex-col justify-center gap-2">
              <h4 className="text-base font-bold text-navy uppercase tracking-wider mb-2 text-center">
                Strategic Priorities
              </h4>
              <div className="bg-navy/10 border border-navy/30 rounded px-3 py-2 text-sm text-navy shadow-sm max-w-[200px]">
                Differentiate and create a Competitive Moat with own proprietary data
              </div>
              <div className="bg-navy/10 border border-navy/30 rounded px-3 py-2 text-sm text-navy shadow-sm max-w-[200px]">
                Achieve ROI at each Phase (not at the end)
              </div>
              <div className="bg-navy/10 border border-navy/30 rounded px-3 py-2 text-sm text-navy shadow-sm max-w-[200px]">
                Bounded risk with optionality at each phase
              </div>
              <div className="bg-navy/10 border border-navy/30 rounded px-3 py-2 text-sm text-navy shadow-sm max-w-[200px]">
                Build Enterprise Capability to discover and leverage AI solutions
              </div>
              <div className="bg-navy/10 border border-navy/30 rounded px-3 py-2 text-sm text-navy shadow-sm max-w-[200px]">
                Discover transformation through use, not designed upfront
              </div>
            </div>
            {/* Bracket */}
            <div className="flex items-center ml-2">
              <svg width="20" height="200" viewBox="0 0 20 200" fill="none">
                <path
                  d="M2 10 Q 15 10, 15 100 Q 15 190, 2 190"
                  stroke="#374151"
                  strokeWidth="2"
                  fill="none"
                />
                <path d="M15 100 L 20 100" stroke="#374151" strokeWidth="2" />
              </svg>
            </div>
          </div>

          {/* Center: Capability Progression - Horizontal Flow (Teal) */}
          <div className="flex-1 flex flex-col justify-center">
            <div className="text-center mb-4">
              <h4 className="text-base font-bold text-teal uppercase tracking-wider">Enterprise AI Capability Progression</h4>
              <p className="text-sm text-gray-600 mt-1">Each phase builds on the last, from knowledge access to orchestrated intelligence in 18 months</p>
            </div>
            <div className="flex items-center gap-2">
              <div className="bg-teal/10 border-2 border-teal/50 rounded-lg px-3 py-3 text-center shadow-sm min-w-[100px]">
                <div className="text-sm font-semibold text-teal">Unified Knowledge Space</div>
                <div className="text-xs text-gray-700 mt-1">Find relevant documents across any division</div>
              </div>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="mx-1 flex-shrink-0">
                <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="#14b8a6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <div className="bg-teal/10 border-2 border-teal/50 rounded-lg px-3 py-3 text-center shadow-sm min-w-[100px]">
                <div className="text-sm font-semibold text-teal">Task AI Agents</div>
                <div className="text-xs text-gray-700 mt-1">Intelligent assistance for team-specific work</div>
              </div>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="mx-1 flex-shrink-0">
                <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="#14b8a6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <div className="bg-teal/10 border-2 border-teal/50 rounded-lg px-3 py-3 text-center shadow-sm min-w-[100px]">
                <div className="text-sm font-semibold text-teal">Division Expert AI</div>
                <div className="text-xs text-gray-700 mt-1">One division expert agent handling many tasks</div>
              </div>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="mx-1 flex-shrink-0">
                <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="#14b8a6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <div className="bg-teal/10 border-2 border-teal/50 rounded-lg px-3 py-3 text-center shadow-sm min-w-[100px]">
                <div className="text-sm font-semibold text-teal">Cross-Expert Discovery</div>
                <div className="text-xs text-gray-700 mt-1">Connecting agents across divisions</div>
              </div>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="mx-1 flex-shrink-0">
                <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="#14b8a6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <div className="bg-teal/10 border-2 border-teal/50 rounded-lg px-3 py-3 text-center shadow-sm min-w-[100px]">
                <div className="text-sm font-semibold text-teal">Orchestrated Agentic AI System</div>
                <div className="text-xs text-gray-700 mt-1">Single AI window routing to the right experts</div>
              </div>
            </div>
          </div>

          {/* Right: Deployment Options (Amber) */}
          <div className="flex flex-col justify-center gap-2 max-w-[180px]">
            <h4 className="text-base font-bold text-amber uppercase tracking-wider mb-2 text-center">
              Deployment Options
            </h4>
            <div className="bg-amber/10 border border-amber/50 rounded px-3 py-3 text-sm text-amber-700 shadow-sm">
              Local Deployment on Company Infrastructure
            </div>
            <div className="bg-amber/10 border border-amber/50 rounded px-3 py-3 text-sm text-amber-700 shadow-sm">
              Can be Deployed in AWS Platform via Bedrock &amp; SageMaker
            </div>
            <div className="bg-amber/10 border border-amber/50 rounded px-3 py-3 text-sm text-amber-700 shadow-sm">
              Ability to integrate as agent/tool with other proprietary systems or standalone
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
