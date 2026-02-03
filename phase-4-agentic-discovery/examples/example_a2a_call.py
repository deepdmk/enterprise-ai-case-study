"""
Example: Making an A2A Protocol Call

This example demonstrates how to make an A2A call to an agent service.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from datetime import datetime
import uuid

from src.shared.a2a_protocol import A2ARequest, A2AResponse, A2AMetadata


def make_a2a_call(
    agent_url: str,
    goal: str,
    max_depth: int = 3
) -> A2AResponse:
    """
    Make an A2A call to an agent.

    Args:
        agent_url: URL of the agent service (e.g., http://localhost:8001)
        goal: What you want from the agent
        max_depth: Maximum cascade depth

    Returns:
        A2A response
    """
    # Create A2A request
    request = A2ARequest(
        goal=goal,
        target="fundraising-agent",  # Determined by URL
        parameters={},
        metadata=A2AMetadata(
            call_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            call_depth=0,
            max_depth=max_depth,
            source_agent="user",
            target_agent="fundraising-agent"
        )
    )

    # Make HTTP call
    response = httpx.post(
        f"{agent_url}/a2a",
        json=request.to_dict(),
        timeout=10.0
    )
    response.raise_for_status()

    # Parse response
    return A2AResponse.from_dict(response.json())


def main():
    """Run example A2A calls"""
    print("\n" + "="*60)
    print("A2A Protocol Call Example")
    print("="*60 + "\n")

    # Make sure agent service is running
    agent_url = "http://localhost:8001"

    print(f"Making A2A call to: {agent_url}\n")

    # Example 1: Simple query (no cascading)
    print("Example 1: Simple Query")
    print("-" * 60)
    response = make_a2a_call(
        agent_url=agent_url,
        goal="What is the investment capacity of investor INV-123?",
        max_depth=1
    )
    print(f"Status: {response.status.value}")
    print(f"Content: {response.content}")
    print(f"Execution time: {response.execution_time_ms:.2f}ms")
    print(f"Cascaded calls: {len(response.cascaded_calls)}")
    print()

    # Example 2: Query that might cascade
    print("Example 2: Query with Potential Cascading")
    print("-" * 60)
    response = make_a2a_call(
        agent_url=agent_url,
        goal="Profile investor INV-456 including competitive landscape",
        max_depth=3
    )
    print(f"Status: {response.status.value}")
    print(f"Content: {response.content}")
    print(f"Execution time: {response.execution_time_ms:.2f}ms")
    print(f"Cascaded calls: {response.cascaded_calls}")
    print()

    # Example 3: At depth limit
    print("Example 3: At Depth Limit")
    print("-" * 60)
    response = make_a2a_call(
        agent_url=agent_url,
        goal="Comprehensive analysis of investor INV-789",
        max_depth=1  # Force depth limit
    )
    print(f"Status: {response.status.value}")
    print(f"Content: {response.content}")
    print()

    print("="*60)
    print("Examples complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Check if service is running
    try:
        response = httpx.get("http://localhost:8001/health", timeout=2.0)
        if response.status_code == 200:
            main()
        else:
            print("Error: Agent service returned unexpected status")
            print("Start the service with: phase4-agent-services --start fundraising-agent --test-mode")
    except httpx.ConnectError:
        print("Error: Agent service not running")
        print("Start the service with: phase4-agent-services --start fundraising-agent --test-mode")
