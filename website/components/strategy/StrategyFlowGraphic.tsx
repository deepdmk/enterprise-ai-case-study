"use client";

import {
  Users,
  Building2,
  Target,
  ArrowRight,
  ArrowDown,
  ListChecks,
  Scale,
  Sparkles,
} from "lucide-react";

/**
 * Strategy Flow Graphic - Convergence Style
 *
 * Shows the strategy development process:
 * - Left: Three analyses (Stakeholder, 7S+SWOT, 5 Forces)
 * - Center: 19 CTQs consolidated
 * - Right: Options Development → Option Scoring → Selected Strategy
 */
export function StrategyFlowGraphic() {
  return (
    <div className="w-full">
      <div className="grid grid-cols-1 md:grid-cols-7 gap-4 items-center">
        {/* Left: Three Analyses */}
        <div className="md:col-span-2 space-y-3">
          <div className="bg-navy text-white rounded-lg p-4 text-center">
            <Users className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">Stakeholder Consultations</div>
            <div className="text-xs text-white/70 mt-1">Board, C-Suite, Staff, Customers</div>
          </div>
          <div className="bg-navy text-white rounded-lg p-4 text-center">
            <Building2 className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">7S + SWOT Analysis</div>
            <div className="text-xs text-white/70 mt-1">Organizational reality mapping</div>
          </div>
          <div className="bg-navy text-white rounded-lg p-4 text-center">
            <Target className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">Porter&apos;s 5 Forces</div>
            <div className="text-xs text-white/70 mt-1">Competitive landscape</div>
          </div>
        </div>

        {/* Arrow */}
        <div className="hidden md:flex justify-center">
          <ArrowRight className="w-8 h-8 text-gray-400" />
        </div>
        <div className="md:hidden flex justify-center py-2">
          <ArrowDown className="w-6 h-6 text-gray-400" />
        </div>

        {/* Center: CTQs */}
        <div className="md:col-span-1">
          <div className="bg-teal text-white rounded-lg p-4 text-center">
            <ListChecks className="w-8 h-8 mx-auto mb-2" />
            <div className="text-2xl font-bold">19</div>
            <div className="font-semibold text-sm">CTQs</div>
            <div className="text-xs text-white/80 mt-2 space-y-1">
              <div>8 Stakeholder</div>
              <div>7 Organizational</div>
              <div>4 Competitive</div>
            </div>
          </div>
        </div>

        {/* Arrow */}
        <div className="hidden md:flex justify-center">
          <ArrowRight className="w-8 h-8 text-gray-400" />
        </div>
        <div className="md:hidden flex justify-center py-2">
          <ArrowDown className="w-6 h-6 text-gray-400" />
        </div>

        {/* Right: Options Development, Scoring & Selection */}
        <div className="md:col-span-2 space-y-3">
          <div className="bg-amber/80 text-white rounded-lg p-4 text-center">
            <ListChecks className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">Options Development</div>
            <div className="text-xs text-white/80 mt-1">3 Strategic Alternatives</div>
          </div>
          <div className="bg-amber text-white rounded-lg p-4 text-center">
            <Scale className="w-6 h-6 mx-auto mb-2" />
            <div className="font-semibold text-sm">Option Scoring</div>
            <div className="text-xs text-white/80 mt-1">Pugh Matrix Analysis</div>
          </div>
          <div className="bg-magenta text-white rounded-lg p-4 text-center border-2 border-white/30">
            <Sparkles className="w-6 h-6 mx-auto mb-2" />
            <div className="font-bold">Phased Internal Build</div>
            <div className="text-xs text-white/80 mt-1">Selected Strategy</div>
          </div>
        </div>
      </div>
    </div>
  );
}
