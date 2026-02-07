"use client";

import {
  Target,
  ListChecks,
  ArrowRight,
  ArrowDown,
  Layers,
  Clock,
  Map,
  BarChart3,
} from "lucide-react";

/**
 * Transformation Flow Graphic - Convergence Style
 *
 * Shows how strategy flows into the transformation framework:
 * - Left: Strategic Analysis + Strategy Development
 * - Center: Transformation Framework
 * - Right: 3 Horizons, 6-Phase Roadmap, Balanced Scorecard
 */
export function TransformationFlowGraphic() {
  return (
    <div className="w-full">
      <div className="grid grid-cols-1 md:grid-cols-7 gap-4 items-center">
        {/* Left: Strategy Inputs */}
        <div className="md:col-span-2 space-y-3">
          <div className="bg-navy text-white rounded-lg p-4 text-center">
            <Target className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">Strategic Analysis</div>
            <div className="text-xs text-white/70 mt-1">3 Independent Analyses</div>
          </div>
          <div className="bg-teal text-white rounded-lg p-4 text-center">
            <ListChecks className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">Strategy Development</div>
            <div className="text-xs text-white/70 mt-1">19 CTQs → Phased Build</div>
          </div>
        </div>

        {/* Arrow */}
        <div className="hidden md:flex justify-center">
          <ArrowRight className="w-8 h-8 text-gray-400" />
        </div>
        <div className="md:hidden flex justify-center py-2">
          <ArrowDown className="w-6 h-6 text-gray-400" />
        </div>

        {/* Center: Transformation Framework Label */}
        <div className="md:col-span-1">
          <div className="bg-magenta text-white rounded-lg p-4 text-center">
            <Layers className="w-8 h-8 mx-auto mb-2" />
            <div className="font-bold text-sm">Transformation</div>
            <div className="text-xs text-white/80">Framework</div>
          </div>
        </div>

        {/* Arrow */}
        <div className="hidden md:flex justify-center">
          <ArrowRight className="w-8 h-8 text-gray-400" />
        </div>
        <div className="md:hidden flex justify-center py-2">
          <ArrowDown className="w-6 h-6 text-gray-400" />
        </div>

        {/* Right: Three Frameworks */}
        <div className="md:col-span-2 space-y-3">
          <div className="bg-teal/80 text-white rounded-lg p-4 text-center">
            <Clock className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">3 Horizons</div>
            <div className="text-xs text-white/80 mt-1">Strategic Staging</div>
          </div>
          <div className="bg-amber text-white rounded-lg p-4 text-center">
            <Map className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">6-Phase Roadmap</div>
            <div className="text-xs text-white/80 mt-1">Integrated Execution</div>
          </div>
          <div className="bg-navy text-white rounded-lg p-4 text-center">
            <BarChart3 className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">Balanced Scorecard</div>
            <div className="text-xs text-white/80 mt-1">Quarterly Measurement</div>
          </div>
        </div>
      </div>
    </div>
  );
}
