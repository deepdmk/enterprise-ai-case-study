"""
TGI Inference Server

Serves fine-tuned orchestrator model using HuggingFace Text Generation Inference.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import subprocess
import structlog

logger = structlog.get_logger()


class TGIServer:
    """
    Text Generation Inference (TGI) server for orchestrator model.

    Features:
    - HuggingFace ecosystem integration
    - Docker-based deployment
    - Production-ready serving
    """

    def __init__(
        self,
        model_path: Path,
        host: str = "0.0.0.0",
        port: int = 8100,
        max_concurrent_requests: int = 128,
        max_batch_total_tokens: int = 16384,
        test_mode: bool = False
    ):
        """
        Initialize TGI server.

        Args:
            model_path: Path to model
            host: Host to bind to
            port: Port to bind to
            max_concurrent_requests: Maximum concurrent requests
            max_batch_total_tokens: Maximum batch total tokens
            test_mode: If True, use mock server
        """
        self.model_path = Path(model_path)
        self.host = host
        self.port = port
        self.max_concurrent_requests = max_concurrent_requests
        self.max_batch_total_tokens = max_batch_total_tokens
        self.test_mode = test_mode

        self.logger = logger.bind(component="tgi_server")

        self.server_process = None

    def start(self) -> None:
        """Start TGI server"""
        if self.test_mode:
            self.logger.info("test_mode_tgi_server", port=self.port)
            self._start_mock_server()
        else:
            self._start_tgi_server()

    def _start_tgi_server(self) -> None:
        """Start actual TGI server using Docker"""
        self.logger.info(
            "starting_tgi_server",
            model=str(self.model_path),
            host=self.host,
            port=self.port
        )

        # TGI Docker command
        cmd = [
            "docker", "run", "--gpus", "all",
            "-p", f"{self.port}:80",
            "-v", f"{self.model_path.absolute()}:/data",
            "--env", f"MAX_CONCURRENT_REQUESTS={self.max_concurrent_requests}",
            "--env", f"MAX_BATCH_TOTAL_TOKENS={self.max_batch_total_tokens}",
            "ghcr.io/huggingface/text-generation-inference:latest",
            "--model-id", "/data"
        ]

        self.logger.info("starting_tgi_docker", command=" ".join(cmd))

        try:
            self.server_process = subprocess.Popen(cmd)
            self.logger.info("tgi_server_started", port=self.port)

        except Exception as e:
            self.logger.error("tgi_start_failed", error=str(e))
            raise

    def _start_mock_server(self) -> None:
        """Start mock TGI server for testing"""
        import asyncio
        from fastapi import FastAPI
        import uvicorn

        app = FastAPI()

        @app.get("/health")
        async def health():
            return {"status": "healthy", "test_mode": True, "server_type": "tgi"}

        @app.post("/generate")
        async def generate(request: Dict[str, Any]):
            # Mock TGI response format
            return {
                "generated_text": "Entry agent: field-operations-agent\nOptimal depth: 2\n\nRationale: Mock TGI response",
                "details": {
                    "generated_tokens": 50,
                    "finish_reason": "length"
                }
            }

        # Run server
        config = uvicorn.Config(app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        asyncio.run(server.serve())

    def stop(self) -> None:
        """Stop TGI server"""
        self.logger.info("stopping_tgi_server")

        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

        self.logger.info("tgi_server_stopped")

    @staticmethod
    def start_server_cli(
        model_path: Path,
        host: str = "0.0.0.0",
        port: int = 8100,
        test_mode: bool = False
    ) -> None:
        """
        Start TGI server from CLI.

        Args:
            model_path: Path to model
            host: Host to bind to
            port: Port to bind to
            test_mode: If True, use mock server
        """
        server = TGIServer(model_path, host, port, test_mode=test_mode)

        try:
            server.start()
            if not test_mode:
                # Wait for Docker process
                server.server_process.wait()
        except KeyboardInterrupt:
            logger.info("stopping_tgi_server")
            server.stop()
