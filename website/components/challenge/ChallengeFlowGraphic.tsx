"use client";

import {
  AlertTriangle,
  TrendingDown,
  Users,
  Building2,
  Briefcase,
  UserCheck,
  ArrowRight,
  ArrowDown,
  XCircle,
  DollarSign,
  HeartCrack,
} from "lucide-react";

/**
 * Challenge Flow Graphic - Convergence Style
 *
 * Shows the challenge progression:
 * - Left: Three Crisis Conditions
 * - Center: Stakeholder Tensions
 * - Right: The Core Dilemma
 */
export function ChallengeFlowGraphic() {
  return (
    <div className="w-full">
      <div className="grid grid-cols-1 md:grid-cols-7 gap-4 items-start">
        {/* Left: Crisis Conditions */}
        <div className="md:col-span-2">
          <div className="bg-navy text-white rounded-lg p-4">
            <div className="text-center mb-4">
              <AlertTriangle className="w-6 h-6 mx-auto mb-2" />
              <div className="font-semibold">Crisis Conditions</div>
            </div>
            <div className="space-y-2">
              <div className="bg-white/10 rounded p-3 text-center">
                <TrendingDown className="w-4 h-4 mx-auto mb-1" />
                <div className="text-sm font-medium">Competitive Survival</div>
                <div className="text-xs text-white/70">Market consolidation pressure</div>
              </div>
              <div className="bg-white/10 rounded p-3 text-center">
                <DollarSign className="w-4 h-4 mx-auto mb-1" />
                <div className="text-sm font-medium">Financial Crisis</div>
                <div className="text-xs text-white/70">50% revenue decline projected</div>
              </div>
              <div className="bg-white/10 rounded p-3 text-center">
                <HeartCrack className="w-4 h-4 mx-auto mb-1" />
                <div className="text-sm font-medium">Change Fatigue</div>
                <div className="text-xs text-white/70">Failed transformation damage</div>
              </div>
            </div>
          </div>
        </div>

        {/* Arrow: Left to Center */}
        <div className="hidden md:flex justify-center items-center h-full">
          <ArrowRight className="w-8 h-8 text-gray-400" />
        </div>
        <div className="md:hidden flex justify-center py-2">
          <ArrowDown className="w-6 h-6 text-gray-400" />
        </div>

        {/* Center+Right: Stakeholder Tensions + Dilemma */}
        <div className="md:col-span-4 space-y-4">
          {/* Stakeholder Tensions */}
          <div className="bg-teal/10 border-2 border-teal rounded-lg p-4">
            <div className="inline-flex items-center gap-2 bg-teal text-white px-4 py-2 rounded-lg mb-4">
              <Users className="w-5 h-5" />
              <span className="font-semibold">Stakeholder Tensions</span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              <div className="bg-teal text-white rounded p-3 text-center">
                <Building2 className="w-5 h-5 mx-auto mb-1" />
                <div className="font-semibold text-xs">Board</div>
                <div className="text-xs text-white/70">Quarterly AI progress</div>
              </div>
              <div className="bg-teal text-white rounded p-3 text-center">
                <Briefcase className="w-5 h-5 mx-auto mb-1" />
                <div className="font-semibold text-xs">C-Suite</div>
                <div className="text-xs text-white/70">Zero-risk exit path</div>
              </div>
              <div className="bg-teal text-white rounded p-3 text-center">
                <UserCheck className="w-5 h-5 mx-auto mb-1" />
                <div className="font-semibold text-xs">Teams</div>
                <div className="text-xs text-white/70">Immediate value</div>
              </div>
              <div className="bg-teal text-white rounded p-3 text-center">
                <Users className="w-5 h-5 mx-auto mb-1" />
                <div className="font-semibold text-xs">Customers</div>
                <div className="text-xs text-white/70">No forced changes</div>
              </div>
            </div>
          </div>

          {/* Arrow down to Dilemma */}
          <div className="flex justify-center">
            <ArrowDown className="w-6 h-6 text-gray-400" />
          </div>

          {/* The Dilemma */}
          <div className="bg-magenta/10 border-2 border-magenta rounded-lg p-4">
            <div className="inline-flex items-center gap-2 bg-magenta text-white px-4 py-2 rounded-lg mb-4">
              <XCircle className="w-5 h-5" />
              <span className="font-semibold">The Dilemma</span>
            </div>
            <div className="text-center mb-4 text-gray-700 font-medium">
              Contradictory requirements that seem impossible to satisfy simultaneously
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
              <div className="bg-magenta text-white rounded p-3 text-center">
                <div className="font-semibold text-sm">No Mandates</div>
                <div className="text-xs text-white/70">Decentralized culture resists top-down</div>
              </div>
              <div className="bg-magenta text-white rounded p-3 text-center">
                <div className="font-semibold text-sm">No Budget</div>
                <div className="text-xs text-white/70">50% revenue decline, no runway</div>
              </div>
              <div className="bg-magenta text-white rounded p-3 text-center">
                <div className="font-semibold text-sm">No Commoditization</div>
                <div className="text-xs text-white/70">Must protect knowledge advantage</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
