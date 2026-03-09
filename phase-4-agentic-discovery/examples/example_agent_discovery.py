"""
Example: Agent Discovery

This example demonstrates how to use the discovery backend to find agents
based on semantic queries.
"""

from pathlib import Path

# Configure paths for cross-phase imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.shared.path_config import configure_paths
configure_paths()

from src.shared.discovery_backend import InMemoryDiscoveryBackend
from src.shared.a2a_protocol import A2ACapability


def create_sample_agents():
    """Create sample agent capabilities"""
    return [
        A2ACapability(
            agent_id="fundraising-agent",
            name="Fundraising",
            description="Provides investor profiles, investment capacity analysis, and sector interest matching",
            domains=[
                "investor profiles",
                "investment capacity",
                "sector interests",
                "investor matching"
            ],
            example_queries=[
                "What is the investment capacity of INV-123?",
                "Which sectors does investor INV-456 focus on?",
                "Find investors interested in healthcare startups"
            ],
            dependencies=["business-development-agent", "field-operations-agent"]
        ),
        A2ACapability(
            agent_id="business-development-agent",
            name="Business Development",
            description="Tracks RFP opportunities, analyzes competitive funding landscape",
            domains=[
                "RFP data",
                "competitive landscape",
                "funding opportunities",
                "funding trends"
            ],
            example_queries=[
                "What RFPs are available in the health sector?",
                "Show competitive landscape for education funding",
                "List recent funding opportunities"
            ],
            dependencies=["fundraising-agent", "field-operations-agent"]
        ),
        A2ACapability(
            agent_id="field-operations-agent",
            name="Field Operations",
            description="Provides local capacity analysis, project performance tracking",
            domains=[
                "local capacity",
                "project performance",
                "regional data"
            ],
            example_queries=[
                "What is the capacity of Kenya office?",
                "Show project performance in Ghana",
                "List active projects in East Africa"
            ],
            dependencies=["fundraising-agent", "business-development-agent"]
        )
    ]


def main():
    """Run agent discovery examples"""
    print("\n" + "="*60)
    print("Agent Discovery Example")
    print("="*60 + "\n")

    # Initialize discovery backend
    print("Initializing discovery backend...")
    backend = InMemoryDiscoveryBackend()

    # Register agents
    print("Registering agents...\n")
    agents = create_sample_agents()
    for agent in agents:
        backend.register_agent(agent)
        print(f"  Registered: {agent.name}")

    print()

    # Example 1: Find agent for investor queries
    print("Example 1: Finding agent for investor queries")
    print("-" * 60)
    query = "I need information about investor capacity and interests"
    print(f"Query: {query}\n")

    results = backend.discover_agents(query, top_k=2)
    for capability, score in results:
        print(f"  {capability.name} (score: {score:.2f})")
        print(f"    ID: {capability.agent_id}")
        print(f"    Domains: {', '.join(capability.domains[:3])}")
        print()

    # Example 2: Find agent for funding opportunities
    print("Example 2: Finding agent for funding opportunities")
    print("-" * 60)
    query = "What RFPs and funding opportunities are available?"
    print(f"Query: {query}\n")

    results = backend.discover_agents(query, top_k=2)
    for capability, score in results:
        print(f"  {capability.name} (score: {score:.2f})")
        print(f"    ID: {capability.agent_id}")
        print()

    # Example 3: Find agent for regional data
    print("Example 3: Finding agent for regional information")
    print("-" * 60)
    query = "I need data about local capacity and project performance"
    print(f"Query: {query}\n")

    results = backend.discover_agents(query, top_k=2)
    for capability, score in results:
        print(f"  {capability.name} (score: {score:.2f})")
        print(f"    ID: {capability.agent_id}")
        print()

    # Example 4: List all agents
    print("Example 4: List all registered agents")
    print("-" * 60)
    all_agents = backend.list_agents()
    print(f"Total agents: {len(all_agents)}\n")
    for agent in all_agents:
        print(f"  {agent.name} ({agent.agent_id})")
        print(f"    Dependencies: {', '.join(agent.dependencies)}")
        print()

    # Example 5: Get specific agent
    print("Example 5: Get specific agent by ID")
    print("-" * 60)
    agent_id = "fundraising-agent"
    agent = backend.get_agent(agent_id)
    if agent:
        print(f"Agent: {agent.name}")
        print(f"Description: {agent.description}")
        print(f"Domains: {', '.join(agent.domains)}")
        print(f"\nExample queries:")
        for query in agent.example_queries[:3]:
            print(f"  - {query}")
    print()

    print("="*60)
    print("Discovery examples complete!")
    print("="*60 + "\n")

    print("Note: For semantic discovery with embeddings, use ChromaDBDiscoveryBackend")
    print("See PHASE0_INTEGRATION.md for integration with Phase 1 embeddings")


if __name__ == "__main__":
    main()
