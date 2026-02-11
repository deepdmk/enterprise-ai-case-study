"use client";

import Link from "next/link";
import { AlertTriangle, BarChart3, RefreshCw, Code, Clock } from "lucide-react";

/**
 * Four Paths with Reader Guidance
 *
 * Features:
 * - Added persona hints ("Best for executives", etc.)
 * - Added reading time/depth indicators
 * - Clearer visual hierarchy between paths
 * - Icons use lucide-react for consistency
 */
export function FourPathsWithGuidance() {
  const paths = [
    {
      href: "#the-challenge",
      title: "Case Summary",
      description: "Overview of the challenge, approach, solution, and results",
      persona: "Best for: Everyone",
      readTime: "5 min read",
      icon: AlertTriangle,
      color: {
        border: "#64748b",
        bg: "rgba(100, 116, 139, 0.15)",
        iconBg: "rgba(100, 116, 139, 0.2)",
        text: "#475569",
      },
    },
    {
      href: "/strategy",
      title: "Strategic Analysis",
      description: "Business context and strategic approach",
      persona: "Best for: Executives & strategists",
      readTime: "15 min read",
      icon: BarChart3,
      color: {
        border: "#1e3a5f",
        bg: "rgba(30, 58, 95, 0.15)",
        iconBg: "rgba(30, 58, 95, 0.2)",
        text: "#1e3a5f",
      },
    },
    {
      href: "/transformation",
      title: "Transformation Approach",
      description: "Change management and phased rollout",
      persona: "Best for: Change leaders & PMs",
      readTime: "20 min read",
      icon: RefreshCw,
      color: {
        border: "#14b8a6",
        bg: "rgba(20, 184, 166, 0.15)",
        iconBg: "rgba(20, 184, 166, 0.2)",
        text: "#085C4F",
      },
    },
    {
      href: "/solution",
      title: "Technical Solution",
      description: "Architecture, models, and implementation",
      persona: "Best for: Engineers & architects",
      readTime: "30 min read",
      icon: Code,
      color: {
        border: "#f59e0b",
        bg: "rgba(245, 158, 11, 0.15)",
        iconBg: "rgba(245, 158, 11, 0.2)",
        text: "#92400E",
      },
    },
  ];

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 py-6 px-6">
      <div className="text-center mb-4">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-2">
          Explore the Case Study
        </h2>
        <p className="text-lg text-slate-300">
          Choose the angle that matches your interests and available time
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {paths.map((path) => {
          const isHashLink = path.href.startsWith("#");
          const LinkComponent = isHashLink ? "a" : Link;
          return (
          <LinkComponent key={path.href} href={path.href} className="group block h-full">
            <div className="relative bg-white rounded-lg h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 overflow-hidden">
              <div
                className="p-3 h-full border-b-4"
                style={{
                  backgroundColor: path.color.bg,
                  borderColor: path.color.border,
                }}
              >
                {/* Icon and title row */}
                <div className="flex items-center gap-2 mb-2">
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center shadow-sm flex-shrink-0"
                    style={{ backgroundColor: path.color.iconBg }}
                  >
                    <path.icon
                      className="w-4 h-4"
                      style={{ color: path.color.text }}
                    />
                  </div>
                  <h3
                    className="text-base font-bold leading-tight"
                    style={{ color: path.color.text }}
                  >
                    {path.title}
                  </h3>
                </div>

                {/* Description */}
                <p className="text-gray-700 text-sm mb-2">{path.description}</p>

                {/* Metadata row */}
                <div className="flex items-center justify-between text-xs pt-2 border-t border-gray-300/50">
                  <span className="text-gray-600 font-medium">{path.persona}</span>
                  <span className="flex items-center gap-1 text-gray-500">
                    <Clock className="w-3 h-3" />
                    {path.readTime}
                  </span>
                </div>
              </div>
            </div>
          </LinkComponent>
          );
        })}
      </div>
    </div>
  );
}
