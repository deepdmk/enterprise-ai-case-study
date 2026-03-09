"""
Model Provider for vLLM/TGI Inference Servers

Integrates the fine-tuned orchestrator SLM (served via vLLM or TGI)
with the Agno framework using built-in VLLM model class.
"""

from habitat_logging import get_logger
from agno.models.vllm import VLLM
from agno.models.openai.like import OpenAILike

logger = get_logger(__name__)


def create_vllm_model(
    inference_url: str,
    model_id: str = "phase5-orchestrator",
    use_openai_compatible: bool = False,
    **kwargs
) -> VLLM | OpenAILike:
    """
    Create VLLM model pointing to our inference server.

    Uses Agno's built-in VLLM class for custom vLLM endpoints.

    Args:
        inference_url: URL of vLLM/TGI inference server
        model_id: Model identifier
        use_openai_compatible: If True, use OpenAI-compatible endpoint (requires /v1 suffix)
        **kwargs: Additional model parameters

    Returns:
        VLLM or OpenAILike model instance
    """
    logger_bound = logger.bind(component="model_provider", model=model_id)

    if use_openai_compatible:
        # Use OpenAI-compatible endpoint (vLLM with --api-key and /v1 endpoint)
        base_url = inference_url if inference_url.endswith('/v1') else f"{inference_url}/v1"

        logger_bound.info(
            "creating_openai_compatible_model",
            base_url=base_url,
            model_id=model_id
        )

        return OpenAILike(
            id=model_id,
            base_url=base_url,
            api_key="not-needed",  # vLLM doesn't require real API key
            **kwargs
        )
    else:
        # Use standard vLLM endpoint
        # Ensure URL ends with / for vLLM compatibility
        base_url = inference_url.rstrip('/') + '/'

        logger_bound.info(
            "creating_vllm_model",
            base_url=base_url,
            model_id=model_id
        )

        return VLLM(
            id=model_id,
            base_url=base_url,
            **kwargs
        )
