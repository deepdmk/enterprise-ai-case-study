"""
Example: Inference Server

Demonstrates how to use the inference server for routing decisions.
"""

import asyncio
import httpx


async def test_health():
    """Test health endpoint"""
    print("\n1. Testing health endpoint...")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8100/health", timeout=5.0)
            if response.status_code == 200:
                result = response.json()
                print(f"   Status: {result.get('status', 'unknown')}")
                print(f"   Test mode: {result.get('test_mode', False)}")
            else:
                print(f"   Error: HTTP {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
            print("   Make sure inference server is running:")
            print("   phase5-inference --start --test-mode")


async def test_generate():
    """Test generation endpoint"""
    print("\n2. Testing generation endpoint...")

    prompt = """<|system|>
You are an AI orchestrator that coordinates multiple specialized agents.
<|end|>
<|user|>
Query: Evaluate funding opportunity in Kenya for climate project<|end|>
<|assistant|>
"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8100/generate",
                json={
                    "prompt": prompt,
                    "max_tokens": 256,
                    "temperature": 0.1
                },
                timeout=10.0
            )

            if response.status_code == 200:
                result = response.json()
                print(f"   Generated text:")
                print(f"   {result.get('generated_text', 'No response')}")
                print(f"   Latency: {result.get('latency_ms', 0):.0f}ms")
            else:
                print(f"   Error: HTTP {response.status_code}")

        except Exception as e:
            print(f"   Error: {e}")


async def main():
    """Run inference examples"""
    print("="*80)
    print("Example: Inference Server")
    print("="*80)

    await test_health()
    await test_generate()

    print("\n" + "="*80)
    print("Example complete!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
