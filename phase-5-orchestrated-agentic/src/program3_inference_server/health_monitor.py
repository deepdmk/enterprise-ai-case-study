"""
Health Monitor

Monitors inference server health and performance.
"""

from typing import Any, Optional
import time
import asyncio
import httpx
from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


class HealthMonitor:
    """
    Monitors inference server health.

    Checks:
    - Server availability
    - Response latency
    - Error rates
    """

    def __init__(
        self,
        server_url: str,
        check_interval_seconds: int = 30,
        max_latency_ms: int = 200
    ):
        """
        Initialize health monitor.

        Args:
            server_url: URL of inference server
            check_interval_seconds: Health check interval
            max_latency_ms: Maximum acceptable latency
        """
        self.server_url = server_url
        self.check_interval_seconds = check_interval_seconds
        self.max_latency_ms = max_latency_ms

        self.logger = logger.bind(component="health_monitor")

        # Metrics
        self.metrics = {
            "total_checks": 0,
            "successful_checks": 0,
            "failed_checks": 0,
            "avg_latency_ms": 0,
            "max_latency_ms": 0,
            "min_latency_ms": float('inf'),
            "last_check_time": None,
            "last_check_status": None
        }

    async def check_health(self) -> dict[str, Any]:
        """
        Check server health.

        Returns:
            Health check result
        """
        start_time = time.time()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.server_url}/health",
                    timeout=5.0
                )

            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                status = "healthy"
                self.metrics["successful_checks"] += 1
            else:
                status = "unhealthy"
                self.metrics["failed_checks"] += 1

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            status = "error"
            self.metrics["failed_checks"] += 1

            self.logger.error("health_check_failed", error=str(e))

        # Update metrics
        self.metrics["total_checks"] += 1
        self.metrics["last_check_time"] = time.time()
        self.metrics["last_check_status"] = status

        # Update latency metrics
        if status == "healthy":
            self.metrics["max_latency_ms"] = max(self.metrics["max_latency_ms"], latency_ms)
            self.metrics["min_latency_ms"] = min(self.metrics["min_latency_ms"], latency_ms)

            # Update average
            prev_avg = self.metrics["avg_latency_ms"]
            n = self.metrics["successful_checks"]
            self.metrics["avg_latency_ms"] = (prev_avg * (n - 1) + latency_ms) / n

        result = {
            "status": status,
            "latency_ms": latency_ms,
            "timestamp": time.time(),
            "within_sla": latency_ms <= self.max_latency_ms if status == "healthy" else False
        }

        self.logger.info(
            "health_check_complete",
            status=status,
            latency_ms=f"{latency_ms:.0f}ms",
            within_sla=result["within_sla"]
        )

        return result

    async def monitor(self, duration_seconds: Optional[int] = None) -> None:
        """
        Continuously monitor server health.

        Args:
            duration_seconds: How long to monitor (None = indefinite)
        """
        self.logger.info(
            "starting_health_monitoring",
            interval_seconds=self.check_interval_seconds,
            duration_seconds=duration_seconds or "indefinite"
        )

        start_time = time.time()

        try:
            while True:
                await self.check_health()

                # Check if duration exceeded
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    break

                # Wait for next check
                await asyncio.sleep(self.check_interval_seconds)

        except KeyboardInterrupt:
            self.logger.info("monitoring_stopped_by_user")

        self.print_summary()

    def get_metrics(self) -> dict[str, Any]:
        """Get current metrics"""
        return self.metrics.copy()

    def print_summary(self) -> None:
        """Print monitoring summary"""
        print("\n" + "="*80)
        print("Health Monitoring Summary")
        print("="*80)
        print(f"Total checks:       {self.metrics['total_checks']}")
        print(f"Successful:         {self.metrics['successful_checks']}")
        print(f"Failed:             {self.metrics['failed_checks']}")

        if self.metrics['successful_checks'] > 0:
            print(f"Success rate:       {self.metrics['successful_checks'] / self.metrics['total_checks']:.2%}")
            print(f"Avg latency:        {self.metrics['avg_latency_ms']:.0f}ms")
            print(f"Min latency:        {self.metrics['min_latency_ms']:.0f}ms")
            print(f"Max latency:        {self.metrics['max_latency_ms']:.0f}ms")
            print(f"SLA threshold:      {self.max_latency_ms}ms")
            print(f"Within SLA:         {self.metrics['avg_latency_ms'] <= self.max_latency_ms}")

        print("="*80 + "\n")

    async def test_inference(self, test_query: str = "Evaluate funding opportunity in Kenya") -> dict[str, Any]:
        """
        Test inference endpoint.

        Args:
            test_query: Query to test with

        Returns:
            Test result
        """
        self.logger.info("testing_inference", query=test_query)

        prompt = f"""<|system|>
You are an AI orchestrator that coordinates multiple specialized agents.
<|end|>
<|user|>
Query: {test_query}<|end|>
<|assistant|>
"""

        start_time = time.time()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.server_url}/generate",
                    json={
                        "prompt": prompt,
                        "max_tokens": 256,
                        "temperature": 0.1
                    },
                    timeout=10.0
                )

            latency_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                result = response.json()
                status = "success"
            else:
                result = {"error": f"HTTP {response.status_code}"}
                status = "error"

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            result = {"error": str(e)}
            status = "error"

        test_result = {
            "status": status,
            "query": test_query,
            "result": result,
            "latency_ms": latency_ms
        }

        self.logger.info(
            "inference_test_complete",
            status=status,
            latency_ms=f"{latency_ms:.0f}ms"
        )

        return test_result

    @staticmethod
    async def wait_for_server(
        server_url: str,
        timeout_seconds: int = 60,
        check_interval_seconds: int = 2
    ) -> bool:
        """
        Wait for server to become available.

        Args:
            server_url: URL of server
            timeout_seconds: Maximum time to wait
            check_interval_seconds: Check interval

        Returns:
            True if server became available, False if timeout
        """
        logger.info("waiting_for_server", url=server_url, timeout=timeout_seconds)

        start_time = time.time()

        while (time.time() - start_time) < timeout_seconds:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{server_url}/health",
                        timeout=5.0
                    )

                if response.status_code == 200:
                    logger.info("server_available")
                    return True

            except Exception:
                pass

            await asyncio.sleep(check_interval_seconds)

        logger.warning("server_timeout", timeout=timeout_seconds)
        return False
