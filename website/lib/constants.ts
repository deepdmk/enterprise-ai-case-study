export const SITE_CONFIG = {
  title: "Emergent Enterprise AI",
  description: "A complete implementation demonstrating bottom-up AI emergence for enterprise funder intelligence",
  email: "d.dimick@eastsoutheast.international",
  author: "Daniel Dimick",
  linkedin: "https://www.linkedin.com/in/dpdimick",
  github: "https://github.com/deepdmk/enterprise-ai-case-study",
} as const;

export const PHASES = [
  {
    number: 0,
    title: "Infrastructure Foundation",
    subtitle: "Data pipeline and staging infrastructure",
    description: "Foundational registries that track models, datasets, and experiments—enabling systematic learning across all phases. Zero infrastructure cost with file-based storage.",
    slug: "phase-0",
    color: "navy" as const,
  },
  {
    number: 1,
    title: "Unified Embedding Space",
    subtitle: "Shared semantic infrastructure across all divisions",
    description: "Search all organizational data with AI embeddings so employees find relevant documents across any division, country, or language (English, French, Spanish, Arabic) more easily.",
    slug: "phase-1",
    color: "teal" as const,
  },
  {
    number: 2,
    title: "Task-Specific SLMs",
    subtitle: "Fine-tuned small language models for division tasks",
    description: "AI learns the organization's team-specific tasks giving employees intelligent assistance for the work they prioritize—15 specialized models trained on the organization's workflows.",
    slug: "phase-2",
    color: "magenta" as const,
  },
  {
    number: 3,
    title: "MoE Division Agents",
    subtitle: "Mixture-of-Experts models from merged SLMs",
    description: "Each division gets expert AI combining their specialized assistants into one agent that handles many tasks to the organization's standards.",
    slug: "phase-3",
    color: "amber" as const,
  },
  {
    number: 4,
    title: "Agentic Discovery",
    subtitle: "A2A protocol for autonomous collaboration",
    description: "Agents learn how to use information across the organization's divisions giving access to task capabilities to enhance other divisions' work.",
    slug: "phase-4",
    color: "teal" as const,
  },
  {
    number: 5,
    title: "Orchestrated System",
    subtitle: "SLM orchestrator trained from discovery data",
    description: "Employees across the organization engage through a single AI window that can leverage data and capabilities across all the enterprise tailored to the organization's knowledge and culture.",
    slug: "phase-5",
    color: "magenta" as const,
  },
] as const;

export const HABITAT_PRINCIPLES = [
  {
    title: "Infrastructure Over Systems",
    description: "Build enabling capabilities, not rigid solutions. Shared embedding space enables units without constraining them.",
    icon: "server",
  },
  {
    title: "Bottom-Up Emergence",
    description: "Intelligence emerges from unit-level experimentation. Each division fine-tunes AI for their workflows.",
    icon: "users",
  },
  {
    title: "Incremental Value",
    description: "Each phase delivers standalone value. Can stop at Phase 3 with working division agents.",
    icon: "target",
  },
  {
    title: "Organizational Learning",
    description: "Build AI capability into teams, not just tools. Units own and evolve their models.",
    icon: "shield-check",
  },
  {
    title: "Enable, Don't Constrain",
    description: "Infrastructure opens possibilities. Phase 4 discovery has no forced collaboration patterns.",
    icon: "eye",
  },
  {
    title: "Capture at Point of Value",
    description: "Data flows from where work happens. No upfront data centralization required.",
    icon: "network",
  },
  {
    title: "Emergent Intelligence",
    description: "System behavior emerges from agent autonomy. Orchestrator learns from discovered patterns.",
    icon: "dollar-sign",
  },
] as const;

export const TRAINING_ECONOMICS = {
  total: 11100,
  phases: [
    { phase: 1, cost: 800, time: "~4 hours", description: "Embedding model fine-tuning" },
    { phase: 2, cost: 3000, time: "~12 hours", description: "14 task SLMs (Unsloth + LoRA)" },
    { phase: 3, cost: 500, time: "~2 hours", description: "3 MoE merges (mergekit)" },
    { phase: 4, cost: 6000, time: "90 days", description: "Discovery phase (A2A network runtime)" },
    { phase: 5, cost: 800, time: "~6 hours", description: "Orchestrator SLM fine-tuning" },
  ],
} as const;

export const ORGANIZATIONAL_UNITS = [
  {
    name: "Angel Investors Unit",
    description: "Tracks individual funder portfolios, investment interests, and capacity",
    tasks: ["Portfolio analysis", "Investor profiling", "Market sizing", "Fit scoring", "Briefing generation"],
  },
  {
    name: "Competitive Funders Unit",
    description: "Monitors RFPs and competitive landscape for funding opportunities",
    tasks: ["RFP analysis", "Positioning strategy", "Win probability", "Proposal writing"],
  },
  {
    name: "Country Office Unit",
    description: "Provides local market intelligence and project performance tracking",
    tasks: ["Market assessment", "Program design", "Risk analysis", "Impact forecasting", "Stakeholder mapping"],
  },
] as const;
