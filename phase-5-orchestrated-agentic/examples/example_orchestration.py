"""
Example: Orchestrator Service

Demonstrates how to use the orchestrator service for multi-agent coordination.
"""

import asyncio
import httpx
import json


async def test_health():
    """Test orchestrator health"""
    print("\n1. Testing orchestrator health...")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health", timeout=5.0)
            if response.status_code == 200:
                result = response.json()
                print(f"   Status: {result.get('status')}")
                print(f"   Agents available: {result.get('agents_available')}/{result.get('agents_total')}")
                print(f"   Agent health: {result.get('agent_health')}")
            else:
                print(f"   Error: HTTP {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
            print("   Make sure orchestrator is running:")
            print("   phase5-orchestrator --start --test-mode")


async def test_routing():
    """Test routing decision"""
    print("\n2. Testing routing decision...")

    queries = [
        "What is the investment capacity of INV-123?",
        "Evaluate funding opportunity in Kenya for climate project",
        "What RFPs are currently open in education sector?"
    ]

    async with httpx.AsyncClient() as client:
        for query in queries:
            try:
                print(f"\n   Query: {query}")

                response = await client.post(
                    "http://localhost:8000/route",
                    json={"query": query},
                    timeout=5.0
                )

                if response.status_code == 200:
                    result = response.json()
                    decision = result.get("routing_decision", {})

                    print(f"   Entry agent: {decision.get('entry_agent')}")
                    print(f"   Optimal depth: {decision.get('optimal_depth')}")
                    print(f"   Reasoning: {decision.get('reasoning', 'N/A')[:60]}...")
                    print(f"   Latency: {result.get('latency_ms')}ms")
                else:
                    print(f"   Error: HTTP {response.status_code}")

            except Exception as e:
                print(f"   Error: {e}")


async def test_orchestration():
    """Test full orchestration"""
    print("\n3. Testing full orchestration (routing only, no agent execution)...")

    query = "Should we pursue partnership with INV-456?"

    async with httpx.AsyncClient() as client:
        try:
            print(f"\n   Query: {query}")

            response = await client.post(
                "http://localhost:8000/orchestrate",
                json={
                    "query": query,
                    "execute": False  # Don't execute agents (they may not be running)
                },
                timeout=10.0
            )

            if response.status_code == 200:
                result = response.json()
                orchestrated = result.get("orchestrated_response", {})

                print(f"\n   Routing:")
                decision = orchestrated.get("routing_decision", {})
                print(f"     Entry agent: {decision.get('entry_agent')}")
                print(f"     Optimal depth: {decision.get('optimal_depth')}")

                print(f"\n   Response:")
                response_text = orchestrated.get("synthesized_response", "")
                print(f"     {response_text[:200]}...")

                print(f"\n   Performance:")
                print(f"     Total latency: {orchestrated.get('total_latency_ms')}ms")
                print(f"     Success: {orchestrated.get('success')}")
            else:
                print(f"   Error: HTTP {response.status_code}")

        except Exception as e:
            print(f"   Error: {e}")


async def test_stats():
    """Test statistics endpoint"""
    print("\n4. Testing statistics...")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/stats", timeout=5.0)
            if response.status_code == 200:
                result = response.json()
                print(f"   Routing stats:")
                routing = result.get("routing", {})
                print(f"     Total requests: {routing.get('total_requests')}")
                print(f"     Successful: {routing.get('successful_routes')}")
                print(f"     Failed: {routing.get('failed_routes')}")
                print(f"     Fallback: {routing.get('fallback_routes')}")
                print(f"     Avg latency: {routing.get('avg_latency_ms'):.0f}ms")
            else:
                print(f"   Error: HTTP {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")


async def main():
    """Run orchestration examples"""
    print("="*80)
    print("Example: Orchestrator Service")
    print("="*80)

    await test_health()
    await test_routing()
    await test_orchestration()
    await test_stats()

    print("\n" + "="*80)
    print("Example complete!")
    print("\n" + "Note: To test with actual agent execution, start Phase 4 agents:")
    print("  Terminal 1: uvicorn a2a_protocol_implementation:angel_app --port 8001")
    print("  Terminal 2: uvicorn a2a_protocol_implementation:competitive_app --port 8002")
    print("  Terminal 3: uvicorn a2a_protocol_implementation:country_app --port 8003")
    print("  Then run: python examples/example_orchestration.py")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
