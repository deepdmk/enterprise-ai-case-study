"""
Program 3: Inference Server - Main Entry Point

Serves fine-tuned orchestrator model via vLLM or TGI.
"""

import argparse
from pathlib import Path
import sys
import asyncio
import structlog

from config.settings import get_settings
from .vllm_server import vLLMServer
from .tgi_server import TGIServer
from .health_monitor import HealthMonitor

# Configure logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()


def start_server(args, settings):
    """Start inference server"""
    logger.info(
        "starting_inference_server",
        server_type=args.server,
        test_mode=args.test_mode
    )

    # Determine model path
    if args.model_path:
        model_path = Path(args.model_path)
    else:
        model_path = settings.paths.exports_dir / "orchestrator_model"

    if not model_path.exists() and not args.test_mode:
        logger.error("model_not_found", path=str(model_path))
        print(f"Error: Model not found at {model_path}")
        print("Run: phase5-finetune --export --test-mode")
        sys.exit(1)

    # Server configuration
    host = args.host or settings.inference_server.host
    port = args.port or settings.inference_server.port

    # Start appropriate server
    if args.server == "vllm":
        vLLMServer.start_server_cli(
            model_path=model_path,
            host=host,
            port=port,
            test_mode=args.test_mode
        )

    elif args.server == "tgi":
        TGIServer.start_server_cli(
            model_path=model_path,
            host=host,
            port=port,
            test_mode=args.test_mode
        )

    else:
        logger.error("invalid_server_type", server_type=args.server)
        print(f"Error: Invalid server type: {args.server}")
        print("Valid options: vllm, tgi")
        sys.exit(1)


async def health_check(args, settings):
    """Run health check"""
    logger.info("running_health_check")

    server_url = args.server_url or f"http://localhost:{settings.inference_server.port}"

    monitor = HealthMonitor(
        server_url=server_url,
        max_latency_ms=settings.inference_server.max_latency_ms
    )

    # Single health check
    result = await monitor.check_health()

    print("\n" + "="*80)
    print("Health Check Result")
    print("="*80)
    print(f"Server:      {server_url}")
    print(f"Status:      {result['status']}")
    print(f"Latency:     {result['latency_ms']:.0f}ms")
    print(f"Within SLA:  {result['within_sla']}")
    print("="*80 + "\n")

    return result


async def monitor_server(args, settings):
    """Monitor server health continuously"""
    logger.info("starting_continuous_monitoring")

    server_url = args.server_url or f"http://localhost:{settings.inference_server.port}"

    monitor = HealthMonitor(
        server_url=server_url,
        check_interval_seconds=settings.inference_server.health_check_interval_seconds,
        max_latency_ms=settings.inference_server.max_latency_ms
    )

    # Wait for server to be available
    if args.wait_for_server:
        available = await HealthMonitor.wait_for_server(server_url, timeout_seconds=60)
        if not available:
            print(f"Error: Server not available at {server_url}")
            sys.exit(1)

    # Monitor
    duration = args.monitor_duration if hasattr(args, 'monitor_duration') else None
    await monitor.monitor(duration_seconds=duration)


async def test_inference(args, settings):
    """Test inference endpoint"""
    logger.info("testing_inference_endpoint")

    server_url = args.server_url or f"http://localhost:{settings.inference_server.port}"

    monitor = HealthMonitor(server_url=server_url)

    # Wait for server
    if args.wait_for_server:
        available = await HealthMonitor.wait_for_server(server_url, timeout_seconds=60)
        if not available:
            print(f"Error: Server not available at {server_url}")
            sys.exit(1)

    # Test inference
    test_query = args.query or "Evaluate funding opportunity in Kenya for climate project"

    result = await monitor.test_inference(test_query)

    print("\n" + "="*80)
    print("Inference Test Result")
    print("="*80)
    print(f"Query:       {result['query']}")
    print(f"Status:      {result['status']}")
    print(f"Latency:     {result['latency_ms']:.0f}ms")
    print(f"\nResponse:")
    print("-" * 80)
    if result['status'] == 'success':
        response = result['result'].get('generated_text', 'No response')
        print(response)
    else:
        print(f"Error: {result['result']}")
    print("="*80 + "\n")

    return result


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 3: Inference Server - Serve orchestrator model via vLLM or TGI"
    )

    # Actions
    parser.add_argument(
        "--start",
        action="store_true",
        help="Start inference server"
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Run health check"
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Monitor server health continuously"
    )
    parser.add_argument(
        "--test-inference",
        action="store_true",
        help="Test inference endpoint"
    )

    # Server configuration
    parser.add_argument(
        "--server",
        type=str,
        default="vllm",
        choices=["vllm", "tgi"],
        help="Server type (vllm or tgi)"
    )
    parser.add_argument(
        "--host",
        type=str,
        help="Host to bind to (default from config)"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port to bind to (default from config)"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        help="Path to model (default from config)"
    )

    # Monitoring
    parser.add_argument(
        "--server-url",
        type=str,
        help="Server URL for health checks"
    )
    parser.add_argument(
        "--wait-for-server",
        action="store_true",
        help="Wait for server to be available before monitoring/testing"
    )
    parser.add_argument(
        "--monitor-duration",
        type=int,
        help="Monitoring duration in seconds (default: indefinite)"
    )

    # Testing
    parser.add_argument(
        "--query",
        type=str,
        help="Query to test inference with"
    )

    # Configuration
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (mock server)"
    )

    args = parser.parse_args()

    # Load settings
    config_path = Path(args.config)
    settings = get_settings(config_path if config_path.exists() else None)

    # Override test mode from args
    if args.test_mode:
        settings.test_mode = True

    # Check if any action was specified
    if not any([args.start, args.health_check, args.monitor, args.test_inference]):
        parser.print_help()
        sys.exit(1)

    try:
        if args.start:
            start_server(args, settings)

        elif args.health_check:
            asyncio.run(health_check(args, settings))

        elif args.monitor:
            asyncio.run(monitor_server(args, settings))

        elif args.test_inference:
            asyncio.run(test_inference(args, settings))

        logger.info("program_complete")

    except KeyboardInterrupt:
        logger.info("interrupted_by_user")
        sys.exit(0)

    except Exception as e:
        logger.error("program_failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
