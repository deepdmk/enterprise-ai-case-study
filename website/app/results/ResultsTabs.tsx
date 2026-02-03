"use client";

import { useState } from "react";

function TabContainer({
  tabs,
  className,
  style,
}: {
  tabs: { label: string; content: React.ReactNode }[];
  className?: string;
  style?: React.CSSProperties;
}) {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div className={className} style={style}>
      <div className="bg-navy/10 p-1 m-4 rounded-lg">
        <div className="flex">
          {tabs.map((tab, i) => (
            <button
              key={tab.label}
              onClick={() => setActiveTab(i)}
              className={`flex-1 px-6 py-3 text-sm font-semibold rounded-md transition-colors focus:outline-none ${
                activeTab === i
                  ? "text-white bg-navy shadow-sm"
                  : "text-navy bg-transparent hover:bg-navy/10"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>
      <div className="px-4 pb-4">{tabs[activeTab].content}</div>
    </div>
  );
}

export function InvestmentTabs() {
  return (
    <TabContainer
      className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200"
      tabs={[
        {
          label: "Approach Comparison",
          content: (
            <table className="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-navy">Factor</th>
                  <th className="px-4 py-3 text-center font-semibold text-teal">This Approach</th>
                  <th className="px-4 py-3 text-center font-semibold text-gray-600">Typical Vendor Platform</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="px-4 py-3 font-medium">Direct Investment</td>
                  <td className="px-4 py-3 text-center font-bold text-teal">$163.1K</td>
                  <td className="px-4 py-3 text-center text-gray-600">$2M&ndash;$7M</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Timeline to Value</td>
                  <td className="px-4 py-3 text-center font-bold text-teal">Weeks per phase</td>
                  <td className="px-4 py-3 text-center text-gray-600">18&ndash;36 months</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium">Risk Exposure</td>
                  <td className="px-4 py-3 text-center font-bold text-teal">$62.4K max per phase</td>
                  <td className="px-4 py-3 text-center text-gray-600">Full commitment upfront</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Exit Options</td>
                  <td className="px-4 py-3 text-center font-bold text-teal">Stop at any phase</td>
                  <td className="px-4 py-3 text-center text-gray-600">Locked in</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium">Data Ownership</td>
                  <td className="px-4 py-3 text-center font-bold text-teal">Proprietary models</td>
                  <td className="px-4 py-3 text-center text-gray-600">Vendor-controlled</td>
                </tr>
              </tbody>
            </table>
          ),
        },
        {
          label: "Investment by Phase",
          content: (
            <table className="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-navy">Phase</th>
                  <th className="px-4 py-3 text-right font-semibold text-navy">Phase Investment</th>
                  <th className="px-4 py-3 text-right font-semibold text-navy">Cumulative</th>
                  <th className="px-4 py-3 text-left font-semibold text-navy">Capability Unlocked</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="px-4 py-3 font-medium">Phase 0</td>
                  <td className="px-4 py-3 text-right">$0</td>
                  <td className="px-4 py-3 text-right">$0</td>
                  <td className="px-4 py-3 text-gray-600">MLOps foundation</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Phase 1</td>
                  <td className="px-4 py-3 text-right">$62,400</td>
                  <td className="px-4 py-3 text-right">$62,400</td>
                  <td className="px-4 py-3 text-gray-600">Universal knowledge access</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium">Phase 2</td>
                  <td className="px-4 py-3 text-right">$43,600</td>
                  <td className="px-4 py-3 text-right">$106,000</td>
                  <td className="px-4 py-3 text-gray-600">Task-level automation</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Phase 3</td>
                  <td className="px-4 py-3 text-right">$31,200</td>
                  <td className="px-4 py-3 text-right">$137,200</td>
                  <td className="px-4 py-3 text-gray-600">Division-level intelligence</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium">Phase 4</td>
                  <td className="px-4 py-3 text-right">$15,500</td>
                  <td className="px-4 py-3 text-right">$152,700</td>
                  <td className="px-4 py-3 text-gray-600">Cross-division discovery</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Phase 5</td>
                  <td className="px-4 py-3 text-right">$10,400</td>
                  <td className="px-4 py-3 text-right font-bold text-teal">$163,100</td>
                  <td className="px-4 py-3 text-gray-600">Orchestrated enterprise AI</td>
                </tr>
              </tbody>
            </table>
          ),
        },
      ]}
    />
  );
}

export function TechnicalTabs() {
  return (
    <TabContainer
      className="rounded-lg shadow-md overflow-hidden border border-gray-200"
      style={{ backgroundColor: "rgba(255, 255, 255, 0.7)" }}
      tabs={[
        {
          label: "Technical Stack",
          content: (
            <table className="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-3 text-left font-semibold text-navy">Component</th>
                  <th className="px-4 py-3 text-left font-semibold text-navy">Specification</th>
                  <th className="px-4 py-3 text-left font-semibold text-navy">Technical Approach</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="px-4 py-3 font-medium">Custom Embedding Model</td>
                  <td className="px-4 py-3 text-gray-600">Fine-tuned all-MiniLM-L6-v2</td>
                  <td className="px-4 py-3 text-gray-600">Sentence-Transformers, organizational corpus</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Reranker Model</td>
                  <td className="px-4 py-3 text-gray-600">BGE-110M</td>
                  <td className="px-4 py-3 text-gray-600">Cross-encoder for retrieval refinement</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium">Vector Database</td>
                  <td className="px-4 py-3 text-gray-600">ChromaDB</td>
                  <td className="px-4 py-3 text-gray-600">Unified embedding space across divisions</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">14 Task SLMs</td>
                  <td className="px-4 py-3 text-gray-600">Llama 3.1 8B base</td>
                  <td className="px-4 py-3 text-gray-600">LoRA/QLoRA fine-tuning via Unsloth</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium">3 MoE Division Agents</td>
                  <td className="px-4 py-3 text-gray-600">32B parameters each</td>
                  <td className="px-4 py-3 text-gray-600">Mixtral-style architecture via mergekit</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Agent Protocol</td>
                  <td className="px-4 py-3 text-gray-600">FastAPI A2A</td>
                  <td className="px-4 py-3 text-gray-600">Custom agent-to-agent communication</td>
                </tr>
                <tr>
                  <td className="px-4 py-3 font-medium">Learned Orchestrator</td>
                  <td className="px-4 py-3 text-gray-600">Llama 3.1 8B</td>
                  <td className="px-4 py-3 text-gray-600">Trained on Phase 4 discovery data</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-4 py-3 font-medium">Production Framework</td>
                  <td className="px-4 py-3 text-gray-600">Agno</td>
                  <td className="px-4 py-3 text-gray-600">Multi-agent orchestration, deployment-ready</td>
                </tr>
              </tbody>
            </table>
          ),
        },
        {
          label: "AWS Deployment",
          content: (
            <>
              <table className="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-3 text-left font-semibold text-navy">Component</th>
                    <th className="px-4 py-3 text-left font-semibold text-navy">Local Deployment</th>
                    <th className="px-4 py-3 text-left font-semibold text-navy">AWS Service</th>
                    <th className="px-4 py-3 text-left font-semibold text-navy">Scaling Approach</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr>
                    <td className="px-4 py-3 font-medium">Embedding Model</td>
                    <td className="px-4 py-3 text-gray-600">Sentence-Transformers</td>
                    <td className="px-4 py-3 text-gray-600">SageMaker Endpoint</td>
                    <td className="px-4 py-3 text-gray-600">Auto-scaling inference</td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-4 py-3 font-medium">Vector Database</td>
                    <td className="px-4 py-3 text-gray-600">ChromaDB</td>
                    <td className="px-4 py-3 text-gray-600">Aurora PostgreSQL + pgvector</td>
                    <td className="px-4 py-3 text-gray-600">Multi-AZ, read replicas</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 font-medium">Model Registry</td>
                    <td className="px-4 py-3 text-gray-600">File-based</td>
                    <td className="px-4 py-3 text-gray-600">Aurora PostgreSQL</td>
                    <td className="px-4 py-3 text-gray-600">Managed with auto backups</td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-4 py-3 font-medium">14 Task SLMs</td>
                    <td className="px-4 py-3 text-gray-600">Llama 3.1 8B + LoRA</td>
                    <td className="px-4 py-3 text-gray-600">SageMaker Multi-Model</td>
                    <td className="px-4 py-3 text-gray-600">Models loaded from S3</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 font-medium">3 MoE Agents</td>
                    <td className="px-4 py-3 text-gray-600">mergekit (32B each)</td>
                    <td className="px-4 py-3 text-gray-600">SageMaker Endpoints</td>
                    <td className="px-4 py-3 text-gray-600">Custom containers</td>
                  </tr>
                  <tr className="bg-gray-50">
                    <td className="px-4 py-3 font-medium">Agent Protocol</td>
                    <td className="px-4 py-3 text-gray-600">FastAPI A2A</td>
                    <td className="px-4 py-3 text-gray-600">API Gateway + Lambda/ECS</td>
                    <td className="px-4 py-3 text-gray-600">Serverless or container</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 font-medium">Orchestrator</td>
                    <td className="px-4 py-3 text-gray-600">Agno Framework</td>
                    <td className="px-4 py-3 text-gray-600">SageMaker or Bedrock Agents</td>
                    <td className="px-4 py-3 text-gray-600">Managed orchestration</td>
                  </tr>
                </tbody>
              </table>
              <div className="bg-teal/10 px-6 py-4 rounded-lg mt-4">
                <p className="text-base">
                  <span className="font-semibold text-navy">Estimated AWS Monthly Cost:</span>
                  <span className="text-gray-700 ml-2">~$800 (pilot, 100 users) &rarr; ~$2,400 (mid, 1,000 users) &rarr; ~$7,500 (enterprise, 8,000 users)</span>
                </p>
                <p className="text-base text-gray-500 mt-1">Local deployment costs vary by hardware but typically have lower ongoing costs after initial infrastructure investment.</p>
              </div>
            </>
          ),
        },
      ]}
    />
  );
}
