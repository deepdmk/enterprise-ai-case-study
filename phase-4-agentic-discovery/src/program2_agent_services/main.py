"""
Program 2: Agent Services
Main entry point for A2A agent services.

Usage:
    # Start all agents
    python -m src.program2_agent_services.main --start-all

    # Start specific agent
    python -m src.program2_agent_services.main --start fundraising-agent

    # Test mode (mock models)
    python -m src.program2_agent_services.main --start-all --test-mode
"""

import argparse
import asyncio
from pathlib import Path
import uvicorn
from typing import Dict

from .agents import fundraising, business_development, field_operations
from .service_factory import create_multi_agent_system
from ..shared.discovery_backend import InMemoryDiscoveryBackend
from ..shared.call_logger import A2ACallLogger


def get_all_capabilities() -> Dict:
    """Get capabilities for all agents"""
    return {
        "fundraising-agent": fundraising.get_capability(),
        "business-development-agent": business_development.get_capability(),
        "field-operations-agent": field_operations.get_capability()
    }


def start_all_agents(test_mode: bool = False, port: int = 8000):
    """
    Start all agent services.

    Args:
        test_mode: If True, use mock implementations
        port: Base port number (agents will use port+1, port+2, etc.)
    """
    print(f"\n{'='*60}")
    print("Starting A2A Agent Services")
    print(f"{'='*60}\n")

    # Get all capabilities
    capabilities = get_all_capabilities()

    # Create discovery backend
    discovery_backend = InMemoryDiscoveryBackend()

    # Create call logger
    log_dir = Path("data/logs/agent_services")
    call_logger = A2ACallLogger(log_dir)

    # Create multi-agent system
    print("Creating agent services...")
    services = create_multi_agent_system(
        capabilities=capabilities,
        base_port=port,
        discovery_backend=discovery_backend,
        call_logger=call_logger,
        test_mode=test_mode
    )

    print("\nAgent services created:")
    for agent_id, (app, agent, agent_port) in services.items():
        print(f"  {agent_id}: http://localhost:{agent_port}")

    # Start all services
    print("\nStarting services...")
    print("Note: In production, each service would run in its own process.")
    print("For development, starting services sequentially.\n")

    # For simplicity, we'll just start the first service
    # In production, each would run in a separate process/container
    first_agent_id = list(services.keys())[0]
    app, agent, agent_port = services[first_agent_id]

    print(f"Starting {first_agent_id} on port {agent_port}")
    print(f"\nEndpoints:")
    print(f"  Health: http://localhost:{agent_port}/health")
    print(f"  Capability: http://localhost:{agent_port}/capability")
    print(f"  A2A: http://localhost:{agent_port}/a2a")
    print(f"  Query: http://localhost:{agent_port}/query")
    print(f"\nPress Ctrl+C to stop\n")

    # Run the service
    uvicorn.run(app, host="0.0.0.0", port=agent_port)


def start_single_agent(agent_id: str, test_mode: bool = False, port: int = 8001):
    """
    Start a single agent service.

    Args:
        agent_id: Agent identifier
        test_mode: If True, use mock implementation
        port: Port number
    """
    print(f"\n{'='*60}")
    print(f"Starting {agent_id} Service")
    print(f"{'='*60}\n")

    # Get capability
    capabilities = get_all_capabilities()
    if agent_id not in capabilities:
        print(f"Error: Unknown agent '{agent_id}'")
        print(f"Available agents: {', '.join(capabilities.keys())}")
        return

    capability = capabilities[agent_id]

    # Create discovery backend
    discovery_backend = InMemoryDiscoveryBackend()

    # Create call logger
    log_dir = Path("data/logs/agent_services")
    call_logger = A2ACallLogger(log_dir)

    # Build agent registry (map of agent IDs to URLs)
    agent_registry = {
        "fundraising-agent": "http://localhost:8001",
        "business-development-agent": "http://localhost:8002",
        "field-operations-agent": "http://localhost:8003"
    }

    # Create service
    from .service_factory import create_agent_app
    app, agent = create_agent_app(
        agent_id=agent_id,
        capability=capability,
        discovery_backend=discovery_backend,
        call_logger=call_logger,
        agent_registry=agent_registry,
        test_mode=test_mode
    )

    print(f"\nService created: {capability.name}")
    print(f"Port: {port}")
    print(f"Test mode: {test_mode}")
    print(f"\nEndpoints:")
    print(f"  Health: http://localhost:{port}/health")
    print(f"  Capability: http://localhost:{port}/capability")
    print(f"  A2A: http://localhost:{port}/a2a")
    print(f"  Query: http://localhost:{port}/query")
    print(f"\nPress Ctrl+C to stop\n")

    # Run the service
    uvicorn.run(app, host="0.0.0.0", port=port)


def list_agents():
    """List available agents and their capabilities"""
    print(f"\n{'='*60}")
    print("Available A2A Agents")
    print(f"{'='*60}\n")

    capabilities = get_all_capabilities()

    for agent_id, capability in capabilities.items():
        print(f"{capability.name} ({agent_id})")
        print(f"  Description: {capability.description}")
        print(f"  Domains: {', '.join(capability.domains)}")
        print(f"  Dependencies: {', '.join(capability.dependencies)}")
        print(f"  Example queries:")
        for query in capability.example_queries[:3]:
            print(f"    - {query}")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 2: Agent Services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start all agents
  python -m src.program2_agent_services.main --start-all

  # Start specific agent
  python -m src.program2_agent_services.main --start fundraising-agent

  # Test mode (uses mock models)
  python -m src.program2_agent_services.main --start-all --test-mode

  # List available agents
  python -m src.program2_agent_services.main --list
        """
    )

    # Operation mode
    parser.add_argument("--start-all", action="store_true",
                       help="Start all agent services")
    parser.add_argument("--start", type=str,
                       help="Start specific agent service")
    parser.add_argument("--list", action="store_true",
                       help="List available agents")

    # Optional parameters
    parser.add_argument("--port", type=int, default=8000,
                       help="Base port number (default: 8000)")
    parser.add_argument("--test-mode", action="store_true",
                       help="Use test mode (mock models)")

    args = parser.parse_args()

    # Validate that at least one operation is specified
    if not any([args.start_all, args.start, args.list]):
        parser.error("Must specify at least one operation: --start-all, --start, or --list")

    try:
        if args.list:
            list_agents()

        elif args.start_all:
            start_all_agents(test_mode=args.test_mode, port=args.port)

        elif args.start:
            start_single_agent(
                agent_id=args.start,
                test_mode=args.test_mode,
                port=args.port + 1  # Offset by 1 for single agent
            )

    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
        import sys
        sys.exit(1)


if __name__ == "__main__":
    main()
