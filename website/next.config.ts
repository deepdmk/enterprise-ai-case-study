import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/enterprise-ai-case-study',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
