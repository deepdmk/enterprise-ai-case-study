/**
 * MOCKUP E: Social Proof / Technology Strip
 *
 * A compact strip showing:
 * - Key technologies used in the case study
 * - Deployment platform compatibility
 * - Adds credibility through recognized logos/names
 */
export function SocialProofStrip() {
  const technologies = [
    { name: "Python", category: "Core" },
    { name: "PyTorch", category: "ML Framework" },
    { name: "Hugging Face", category: "Models" },
    { name: "LangChain", category: "Orchestration" },
    { name: "ChromaDB", category: "Vector DB" },
    { name: "FastAPI", category: "API" },
  ];

  const platforms = [
    { name: "AWS Bedrock", available: true },
    { name: "AWS SageMaker", available: true },
    { name: "Azure AI", available: true },
    { name: "Self-Hosted", available: true },
  ];

  return (
    <div className="bg-teal/10 border-y border-teal/30 py-6">
      <div className="max-w-6xl mx-auto px-4">
        {/* Technologies */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center gap-6">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap">
              Built With
            </span>
            <div className="flex flex-wrap items-center gap-3">
              {technologies.map((tech) => (
                <div
                  key={tech.name}
                  className="flex items-center gap-1.5 bg-white border border-gray-200 rounded-full px-3 py-1"
                >
                  <span className="text-sm font-medium text-gray-700">
                    {tech.name}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="hidden md:block w-px h-8 bg-gray-300" />

          {/* Deployment platforms */}
          <div className="flex items-center gap-4">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap">
              Deploys To
            </span>
            <div className="flex flex-wrap items-center gap-2">
              {platforms.map((platform) => (
                <span
                  key={platform.name}
                  className="text-sm text-gray-600 flex items-center gap-1"
                >
                  <svg
                    className="w-3.5 h-3.5 text-teal"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                  {platform.name}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * MOCKUP E (Variant 2): Minimal Stats Bar
 *
 * Alternative approach using key metrics instead of technologies
 */
export function StatsBar() {
  const stats = [
    { value: "$1.3B", label: "Enterprise Scale" },
    { value: "18", label: "Month Journey" },
    { value: "5", label: "AI Phases" },
    { value: "3", label: "Deployment Options" },
  ];

  return (
    <div className="bg-navy py-6">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-teal-on-navy">
                {stat.value}
              </div>
              <div className="text-sm text-white/70 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
