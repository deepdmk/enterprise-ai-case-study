import {
  Database,
  Bot,
  Users,
  Network,
  Workflow,
  ChevronRight,
  ChevronUp,
  ArrowUp,
} from "lucide-react";

/**
 * Responsive Journey Graphic
 *
 * Cascading upward layout:
 * - Phases build from bottom to top
 * - Shows progression as growth
 * - Strategic Priorities on left, Deployment Options on right
 */
export function JourneyGraphicResponsive() {
  const phases = [
    {
      number: 1,
      title: "Unified Knowledge Space",
      description: "Find relevant documents across any division",
      icon: Database,
    },
    {
      number: 2,
      title: "Task AI Agents",
      description: "Intelligent assistance for team-specific work",
      icon: Bot,
    },
    {
      number: 3,
      title: "Division Expert AI",
      description: "One expert agent handling many tasks per division",
      icon: Users,
    },
    {
      number: 4,
      title: "Cross-Expert Discovery",
      description: "Connecting agents across divisions",
      icon: Network,
    },
    {
      number: 5,
      title: "Orchestrated AI System",
      description: "Single AI window routing to right experts",
      icon: Workflow,
    },
  ];

  const strategicPriorities = [
    "Differentiate with proprietary data",
    "Achieve ROI at each phase",
    "Bounded risk with optionality",
    "Build enterprise AI capability",
    "Discover through use, not upfront design",
  ];

  const deploymentOptions = [
    "Local infrastructure",
    "AWS Bedrock & SageMaker",
    "Azure AI services",
    "Standalone or integrated",
  ];

  // Reverse phases for bottom-to-top display
  const phasesReversed = [...phases].reverse();

  return (
    <div className="w-full">
      {/* Top Chevron Bar */}
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-0 mb-8">
        <div className="flex-1 bg-navy text-white px-4 py-3 text-center font-semibold text-sm sm:rounded-l-lg">
          Strategic Analysis
        </div>
        <div className="flex-1 bg-teal-dark text-white px-4 py-3 text-center font-semibold text-sm flex items-center justify-center gap-1">
          <ChevronRight className="w-4 h-4 hidden sm:block -ml-4" />
          Transformation Framework
        </div>
        <div className="flex-1 bg-amber text-white px-4 py-3 text-center font-semibold text-sm sm:rounded-r-lg flex items-center justify-center gap-1">
          <ChevronRight className="w-4 h-4 hidden sm:block -ml-4" />
          Scale & Deploy
        </div>
      </div>

      {/* Main Content - 3 column on large screens */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Strategic Priorities */}
        <div>
          <h4 className="text-sm font-bold text-navy uppercase tracking-wider mb-3">
            Strategic Priorities
          </h4>
          <div className="space-y-2">
            {strategicPriorities.map((priority, index) => (
              <div
                key={index}
                className="bg-navy/10 border border-navy/30 rounded px-3 py-2 text-sm text-navy"
              >
                {priority}
              </div>
            ))}
          </div>
        </div>

        {/* Phase Timeline - stair-step climbing left to right */}
        <div>
          <h4 className="text-sm font-bold text-teal-on-light uppercase tracking-wider mb-3 text-center">
            18-Month Capability Progression
          </h4>
          <div className="relative w-full">
            {/* Render phases as stairs: bottom-right to top-left */}
            {[...phases].reverse().map((phase, reverseIndex) => {
              const index = phases.length - 1 - reverseIndex; // 0 at bottom, 4 at top
              // Bottom on left, top on right - stairs climb left to right
              const rightPercent = (phases.length - 1 - index) * 12; // 48%, 36%, 24%, 12%, 0%
              return (
                <div key={phase.number} className="relative h-[52px] mb-1">
                  {/* Phase box - positioned from right */}
                  <div
                    className="absolute flex items-center gap-2 bg-teal/10 border-2 border-teal/50 rounded-lg p-2 w-[200px]"
                    style={{ right: `${rightPercent}%` }}
                  >
                    <div className="w-7 h-7 bg-teal/20 rounded-full flex items-center justify-center flex-shrink-0">
                      <phase.icon className="w-3.5 h-3.5 text-teal-on-light" />
                    </div>
                    <div>
                      <div className="text-xs font-semibold text-teal-on-light leading-tight">
                        {phase.title}
                      </div>
                      <p className="text-[10px] text-gray-600 leading-tight">{phase.description}</p>
                    </div>
                  </div>
                  {/* Arrow pointing up to next step (except for bottom phase) */}
                  {reverseIndex < phases.length - 1 && (
                    <div
                      className="absolute"
                      style={{
                        right: `calc(${rightPercent}% + 85px)`,
                        bottom: '-12px'
                      }}
                    >
                      <ChevronUp className="w-5 h-5 text-teal" />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Deployment Options */}
        <div>
          <h4 className="text-sm font-bold text-amber uppercase tracking-wider mb-3">
            Deployment Options
          </h4>
          <div className="space-y-2">
            {deploymentOptions.map((option, index) => (
              <div
                key={index}
                className="bg-amber/10 border border-amber/50 rounded px-3 py-2 text-sm text-amber-on-light"
              >
                {option}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
