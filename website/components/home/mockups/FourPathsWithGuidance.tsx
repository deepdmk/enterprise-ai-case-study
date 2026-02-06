"use client";

import Link from "next/link";
import { FileText, BarChart3, RefreshCw, Code, Clock, Star } from "lucide-react";

/**
 * MOCKUP C: Four Paths with Reader Guidance
 *
 * Changes from original:
 * - Added persona hints ("Best for executives", etc.)
 * - Added reading time/depth indicators
 * - Case Summary is highlighted as recommended starting point
 * - Clearer visual hierarchy between paths
 * - Icons use lucide-react for consistency
 */
export function FourPathsWithGuidance() {
  const paths = [
    {
      href: "/summary",
      title: "Case Summary",
      description: "Complete overview at a glance",
      persona: "Best for: Everyone",
      readTime: "5 min read",
      recommended: true,
      icon: FileText,
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
      recommended: false,
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
      recommended: false,
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
      recommended: false,
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
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-10">
      <div className="text-center mb-8">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-2">
          Pick Your Path
        </h2>
        <p className="text-lg text-slate-300">
          Choose the angle that matches your interests and available time
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {paths.map((path) => (
          <Link key={path.href} href={path.href} className="group block h-full">
            <div
              className={`relative bg-white rounded-xl h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 overflow-hidden ${
                path.recommended ? "ring-2 ring-teal ring-offset-2 ring-offset-slate-800" : ""
              }`}
            >
              {/* Recommended badge */}
              {path.recommended && (
                <div className="absolute top-0 right-0 bg-teal text-white text-xs font-bold px-3 py-1 rounded-bl-lg flex items-center gap-1">
                  <Star className="w-3 h-3 fill-current" />
                  Start Here
                </div>
              )}

              <div
                className="p-5 h-full border-b-4"
                style={{
                  backgroundColor: path.color.bg,
                  borderColor: path.color.border,
                }}
              >
                {/* Icon and title row */}
                <div className="flex items-start gap-3 mb-3">
                  <div
                    className="w-11 h-11 rounded-lg flex items-center justify-center shadow-md flex-shrink-0"
                    style={{ backgroundColor: path.color.iconBg }}
                  >
                    <path.icon
                      className="w-5 h-5"
                      style={{ color: path.color.text }}
                    />
                  </div>
                  <div>
                    <h3
                      className="text-lg font-bold leading-tight"
                      style={{ color: path.color.text }}
                    >
                      {path.title}
                    </h3>
                  </div>
                </div>

                {/* Description */}
                <p className="text-gray-700 text-sm mb-4">{path.description}</p>

                {/* Metadata row */}
                <div className="flex items-center justify-between text-xs pt-3 border-t border-gray-300/50">
                  <span className="text-gray-700 font-medium">{path.persona}</span>
                  <span className="flex items-center gap-1 text-gray-600">
                    <Clock className="w-3 h-3" />
                    {path.readTime}
                  </span>
                </div>

                {/* Arrow indicator */}
                <div className="flex justify-end mt-3">
                  <svg
                    className="w-5 h-5 group-hover:translate-x-1 transition-transform"
                    style={{ color: path.color.text }}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
