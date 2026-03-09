"""
Program 4: Orchestrator Service - Main Entry Point

FastAPI orchestrator service wrapping the SLM orchestrator.
Supports both API server mode and Gradio UI mode.
"""

import argparse
from pathlib import Path
import sys
import uvicorn
from habitat_logging import get_logger

from config.settings import get_settings
from .service import create_app
from .gradio_app import create_orchestrator_interface

logger = get_logger(__name__)


def start_ui(args, settings):
    """Start Gradio UI interface"""
    logger.info(
        "starting_orchestrator_ui",
        port=args.ui_port or settings.orchestrator_service.gradio.port,
        test_mode=args.test_mode,
    )

    # Get Gradio config
    gradio_config = settings.orchestrator_service.gradio

    # Determine service URL for production mode
    service_url = None
    if not args.test_mode:
        service_url = f"http://{settings.orchestrator_service.host}:{settings.orchestrator_service.port}"

    # Create interface
    interface = create_orchestrator_interface(
        test_mode=args.test_mode,
        service_url=service_url,
        config=gradio_config,
    )

    # Determine host/port
    host = gradio_config.host
    port = args.ui_port or gradio_config.port
    share = args.share or gradio_config.share

    print("\n" + "=" * 80)
    print("Phase 5 Orchestrator Interface")
    print("=" * 80)
    print(f"Host:        {host}")
    print(f"Port:        {port}")
    print(f"Mode:        {'Test (mock responses)' if args.test_mode else 'Production'}")
    print(f"Share:       {share}")
    if not args.test_mode:
        print(f"Service URL: {service_url}")
    print(f"\nOpen in browser: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print("=" * 80 + "\n")

    # Launch interface
    interface.launch(host=host, port=port, share=share)


def start_service(args, settings):
    """Start orchestrator service"""
    # Determine whether to use Agno mode
    use_agno = args.use_agno or getattr(settings.orchestrator_service, 'agno', {}).get('enabled', False)

    logger.info(
        "starting_orchestrator_service",
        port=args.port or settings.orchestrator_service.port,
        test_mode=args.test_mode,
        use_agno=use_agno
    )

    # Service configuration
    host = args.host or settings.orchestrator_service.host
    port = args.port or settings.orchestrator_service.port

    # Get Agno configuration
    agno_config = None
    if use_agno:
        agno_config = getattr(settings.orchestrator_service, 'agno', {})

    # Create FastAPI app
    app = create_app(
        inference_server_url=settings.orchestrator_service.inference_server_url,
        agent_registry=settings.orchestrator_service.agent_registry,
        routing_timeout_ms=settings.orchestrator_service.routing_timeout_ms,
        agent_timeout_ms=settings.orchestrator_service.agent_timeout_ms,
        max_concurrent_agents=settings.orchestrator_service.max_concurrent_agent_calls,
        enable_response_synthesis=settings.orchestrator_service.enable_response_synthesis,
        test_mode=args.test_mode,
        use_agno=use_agno,
        agno_config=agno_config
    )

    print("\n" + "="*80)
    print("Phase 5 Orchestrator Service")
    print("="*80)
    print(f"Host:           {host}")
    print(f"Port:           {port}")
    print(f"Mode:           {'Agno Framework' if use_agno else 'Legacy Routing Engine'}")
    print(f"Test mode:      {args.test_mode}")
    print(f"Inference URL:  {settings.orchestrator_service.inference_server_url}")
    print(f"\nAgent Registry:")
    for agent_name, agent_url in settings.orchestrator_service.agent_registry.items():
        print(f"  {agent_name}: {agent_url}")
    print("\nEndpoints:")
    print(f"  Health:       http://{host}:{port}/health")
    print(f"  Route:        http://{host}:{port}/route")
    print(f"  Orchestrate:  http://{host}:{port}/orchestrate")
    print(f"  Stats:        http://{host}:{port}/stats")
    print(f"  Docs:         http://{host}:{port}/docs")
    if use_agno and agno_config and agno_config.get('agui', {}).get('enabled', False):
        agui_path = agno_config.get('agui', {}).get('path', '/agui')
        print(f"  AG-UI:        http://{host}:{port}{agui_path}")
    print("="*80 + "\n")

    # Run server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Program 4: Orchestrator Service - SLM-based orchestrator service"
    )

    # Actions
    parser.add_argument(
        "--start",
        action="store_true",
        help="Start orchestrator service"
    )
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch Gradio interface instead of API server"
    )

    # Configuration
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
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode (rule-based routing, no SLM)"
    )
    parser.add_argument(
        "--use-agno",
        action="store_true",
        help="Use Agno framework instead of legacy routing engine"
    )

    # UI-specific options
    parser.add_argument(
        "--ui-port",
        type=int,
        help="Gradio UI port (default: from config, typically 7862)"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create public Gradio link"
    )

    args = parser.parse_args()

    # Load settings
    config_path = Path(args.config)
    settings = get_settings(config_path if config_path.exists() else None)

    # Override test mode from args
    if args.test_mode:
        settings.test_mode = True

    # Check if any action was specified
    if not args.start and not args.ui:
        parser.print_help()
        sys.exit(1)

    try:
        if args.ui:
            start_ui(args, settings)
        else:
            start_service(args, settings)

    except KeyboardInterrupt:
        logger.info("service_stopped_by_user")
        print("\nService stopped")
        sys.exit(0)

    except Exception as e:
        logger.error("service_failed", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
