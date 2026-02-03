"""
vLLM Inference Server

Serves fine-tuned orchestrator model using vLLM for fast inference.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import asyncio
import structlog

logger = structlog.get_logger()


class vLLMServer:
    """
    vLLM-based inference server for orchestrator model.

    Features:
    - High-throughput inference
    - Batched requests
    - GPU acceleration
    """

    def __init__(
        self,
        model_path: Path,
        host: str = "0.0.0.0",
        port: int = 8100,
        gpu_memory_utilization: float = 0.9,
        max_model_len: int = 2048,
        tensor_parallel_size: int = 1,
        test_mode: bool = False
    ):
        """
        Initialize vLLM server.

        Args:
            model_path: Path to model
            host: Host to bind to
            port: Port to bind to
            gpu_memory_utilization: GPU memory utilization
            max_model_len: Maximum sequence length
            tensor_parallel_size: Tensor parallel size
            test_mode: If True, use mock server
        """
        self.model_path = Path(model_path)
        self.host = host
        self.port = port
        self.gpu_memory_utilization = gpu_memory_utilization
        self.max_model_len = max_model_len
        self.tensor_parallel_size = tensor_parallel_size
        self.test_mode = test_mode

        self.logger = logger.bind(component="vllm_server")

        self.engine = None
        self.server_process = None

    async def start(self) -> None:
        """Start vLLM server"""
        if self.test_mode:
            self.logger.info("test_mode_mock_server", port=self.port)
            await self._start_mock_server()
        else:
            await self._start_vllm_server()

    async def _start_vllm_server(self) -> None:
        """Start actual vLLM server"""
        try:
            from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams
            from vllm.engine.arg_utils import AsyncEngineArgs

            self.logger.info(
                "starting_vllm_server",
                model=str(self.model_path),
                host=self.host,
                port=self.port
            )

            # Engine arguments
            engine_args = AsyncEngineArgs(
                model=str(self.model_path),
                tensor_parallel_size=self.tensor_parallel_size,
                gpu_memory_utilization=self.gpu_memory_utilization,
                max_model_len=self.max_model_len,
                trust_remote_code=True
            )

            # Create engine
            self.engine = AsyncLLMEngine.from_engine_args(engine_args)

            self.logger.info("vllm_server_started", port=self.port)

        except ImportError:
            self.logger.error(
                "vllm_not_installed",
                message="vLLM not installed. Install with: pip install vllm"
            )
            raise

    async def _start_mock_server(self) -> None:
        """Start mock server for testing"""
        from fastapi import FastAPI
        import uvicorn

        app = FastAPI()

        @app.get("/health")
        async def health():
            return {"status": "healthy", "test_mode": True}

        @app.post("/generate")
        async def generate(request: Dict[str, Any]):
            # Mock response
            return {
                "generated_text": "Entry agent: field-operations-agent\nOptimal depth: 2\n\nRationale: Mock response",
                "tokens_generated": 50,
                "latency_ms": 100
            }

        # Run server
        config = uvicorn.Config(app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.1,
        top_p: float = 0.95
    ) -> Dict[str, Any]:
        """
        Generate text from prompt.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter

        Returns:
            Generated text and metadata
        """
        if self.test_mode:
            return {
                "generated_text": "Entry agent: field-operations-agent\nOptimal depth: 2",
                "tokens_generated": 50,
                "latency_ms": 100
            }

        from vllm import SamplingParams

        # Sampling parameters
        sampling_params = SamplingParams(
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )

        # Generate
        import time
        start_time = time.time()

        results = await self.engine.generate(prompt, sampling_params, request_id=None)

        latency_ms = (time.time() - start_time) * 1000

        # Extract generated text
        generated_text = results.outputs[0].text if results.outputs else ""

        return {
            "generated_text": generated_text,
            "tokens_generated": len(results.outputs[0].token_ids) if results.outputs else 0,
            "latency_ms": latency_ms
        }

    def stop(self) -> None:
        """Stop vLLM server"""
        self.logger.info("stopping_vllm_server")

        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

        self.logger.info("vllm_server_stopped")

    @staticmethod
    def start_server_cli(
        model_path: Path,
        host: str = "0.0.0.0",
        port: int = 8100,
        test_mode: bool = False
    ) -> None:
        """
        Start vLLM server from CLI.

        Args:
            model_path: Path to model
            host: Host to bind to
            port: Port to bind to
            test_mode: If True, use mock server
        """
        import subprocess

        if test_mode:
            logger.info("test_mode_using_fastapi_mock")
            # Use mock server
            server = vLLMServer(model_path, host, port, test_mode=True)
            asyncio.run(server.start())
        else:
            # Use vLLM CLI
            cmd = [
                "python", "-m", "vllm.entrypoints.openai.api_server",
                "--model", str(model_path),
                "--host", host,
                "--port", str(port),
                "--gpu-memory-utilization", "0.9",
                "--max-model-len", "2048"
            ]

            logger.info("starting_vllm_cli", command=" ".join(cmd))

            process = subprocess.Popen(cmd)

            try:
                process.wait()
            except KeyboardInterrupt:
                logger.info("stopping_vllm_server")
                process.terminate()
                process.wait()
