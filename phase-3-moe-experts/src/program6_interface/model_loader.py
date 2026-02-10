"""
MoE Model Loader and Inference Engine.

Loads MoE models from Phase 4 exports and provides inference
with expert activation tracking.
"""

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    TORCH_AVAILABLE = False

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

logger = get_logger(__name__)


@dataclass
class ExpertActivation:
    """Represents activation of a single expert."""

    expert_id: int
    task_id: str
    model_id: str
    activation_score: float


@dataclass
class InferenceResult:
    """Result from MoE inference."""

    response: str
    activations: list[ExpertActivation] = field(default_factory=list)
    tokens_generated: int = 0
    generation_time_ms: float = 0.0


class ExpertActivationTracker:
    """
    Tracks expert activations during MoE forward pass.

    Registers hooks on the router layer to capture expert selection.
    """

    def __init__(self, expert_registry: dict):
        """
        Initialize activation tracker.

        Args:
            expert_registry: Expert registry with task mappings.
        """
        self.expert_registry = expert_registry
        self.activations: dict[int, float] = {}
        self._hooks: list = []

    def clear(self) -> None:
        """Clear accumulated activations."""
        self.activations = {}

    def router_hook(self, module: Any, input: Any, output: Any) -> None:
        """
        Hook function for router layer.

        For Mixtral-style MoE, the router outputs expert weights.
        """
        try:
            # Output shape depends on architecture
            # For Mixtral: (batch, seq_len, num_experts)
            if isinstance(output, tuple):
                router_logits = output[0]
            else:
                router_logits = output

            # Get top-k selections and their weights
            if hasattr(router_logits, "softmax"):
                router_probs = router_logits.softmax(dim=-1)
            else:
                router_probs = torch.softmax(router_logits, dim=-1)

            # Aggregate across batch and sequence
            mean_probs = router_probs.mean(dim=[0, 1])

            # Update activation scores
            for expert_id, score in enumerate(mean_probs.tolist()):
                if expert_id not in self.activations:
                    self.activations[expert_id] = 0.0
                self.activations[expert_id] += score

        except Exception as e:
            logger.warning("router_hook_error", error=str(e))

    def get_top_activations(self, top_k: int = 5) -> list[ExpertActivation]:
        """
        Get top-k expert activations with task mappings.

        Args:
            top_k: Number of top experts to return.

        Returns:
            List of ExpertActivation objects.
        """
        experts = self.expert_registry.get("experts", {})

        # Normalize activations
        total = sum(self.activations.values()) or 1.0
        normalized = {k: v / total for k, v in self.activations.items()}

        # Sort by activation score
        sorted_experts = sorted(
            normalized.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        activations = []
        for expert_id, score in sorted_experts:
            expert_info = experts.get(str(expert_id), {})
            activations.append(
                ExpertActivation(
                    expert_id=expert_id,
                    task_id=expert_info.get("task_id", f"expert_{expert_id}"),
                    model_id=expert_info.get("model_id", f"unknown_{expert_id}"),
                    activation_score=round(score, 4),
                )
            )

        return activations

    def register_hooks(self, model: Any) -> None:
        """
        Register forward hooks on router layers.

        Args:
            model: The MoE model to hook.
        """
        self.remove_hooks()

        # Find router/gate modules (architecture-dependent)
        for name, module in model.named_modules():
            # Mixtral-style: look for gate modules
            if "gate" in name.lower() or "router" in name.lower():
                hook = module.register_forward_hook(self.router_hook)
                self._hooks.append(hook)
                logger.debug("router_hook_registered", module_name=name)

        if not self._hooks:
            logger.warning("no_router_modules_found")

    def remove_hooks(self) -> None:
        """Remove all registered hooks."""
        for hook in self._hooks:
            hook.remove()
        self._hooks = []


class MoEModelLoader:
    """
    Loads and manages MoE models for inference.

    Supports loading multiple unit models and tracking expert activations.
    """

    def __init__(
        self,
        exports_dir: Path,
        device: str = "auto",
        load_in_8bit: bool = False,
        load_in_4bit: bool = False,
    ):
        """
        Initialize model loader.

        Args:
            exports_dir: Path to phase4 exports directory.
            device: Device for inference ("auto", "cuda", "cpu").
            load_in_8bit: Use 8-bit quantization.
            load_in_4bit: Use 4-bit quantization.
        """
        self.exports_dir = Path(exports_dir)
        self.device = device
        self.load_in_8bit = load_in_8bit
        self.load_in_4bit = load_in_4bit

        self.models: dict[str, Any] = {}
        self.tokenizers: dict[str, Any] = {}
        self.expert_registries: dict[str, dict] = {}
        self.activation_trackers: dict[str, ExpertActivationTracker] = {}

        logger.info(
            "moe_model_loader_initialized",
            exports_dir=str(self.exports_dir),
            device=device,
            load_in_8bit=load_in_8bit,
            load_in_4bit=load_in_4bit,
        )

    def get_available_units(self) -> list[str]:
        """Get list of available units from exports directory."""
        units = []
        for unit_dir in self.exports_dir.iterdir():
            if unit_dir.is_dir() and (unit_dir / "model").exists():
                units.append(unit_dir.name)
        return units

    def load_unit(self, unit_id: str) -> bool:
        """
        Load a unit's MoE model.

        Args:
            unit_id: Unit identifier.

        Returns:
            True if loaded successfully.
        """
        if not TORCH_AVAILABLE:
            logger.error("torch_not_available", message="PyTorch is required for model loading")
            return False

        if unit_id in self.models:
            logger.info("model_already_loaded", unit_id=unit_id)
            return True

        unit_dir = self.exports_dir / unit_id
        model_dir = unit_dir / "model"
        routing_dir = unit_dir / "routing"

        if not model_dir.exists():
            logger.error("model_dir_not_found", unit_id=unit_id, path=str(model_dir))
            return False

        try:
            # Import here to avoid loading transformers unnecessarily
            from transformers import AutoModelForCausalLM, AutoTokenizer

            logger.info("loading_model", unit_id=unit_id, path=str(model_dir))

            # Determine device map
            device_map = "auto" if self.device == "auto" else self.device

            # Load model with quantization if specified
            load_kwargs: dict[str, Any] = {
                "device_map": device_map,
                "trust_remote_code": True,
            }

            if self.load_in_8bit:
                load_kwargs["load_in_8bit"] = True
            elif self.load_in_4bit:
                load_kwargs["load_in_4bit"] = True
            else:
                load_kwargs["torch_dtype"] = torch.float16

            model = AutoModelForCausalLM.from_pretrained(
                str(model_dir),
                **load_kwargs,
            )

            tokenizer = AutoTokenizer.from_pretrained(str(model_dir))

            # Set padding token if not set
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            self.models[unit_id] = model
            self.tokenizers[unit_id] = tokenizer

            # Load expert registry
            registry_path = routing_dir / "expert_registry.json"
            if registry_path.exists():
                with open(registry_path) as f:
                    self.expert_registries[unit_id] = json.load(f)
            else:
                self.expert_registries[unit_id] = {"experts": {}}

            # Set up activation tracker
            tracker = ExpertActivationTracker(self.expert_registries[unit_id])
            tracker.register_hooks(model)
            self.activation_trackers[unit_id] = tracker

            logger.info(
                "model_loaded",
                unit_id=unit_id,
                num_experts=len(self.expert_registries[unit_id].get("experts", {})),
            )

            return True

        except Exception as e:
            logger.error("model_load_failed", unit_id=unit_id, error=str(e))
            return False

    def unload_unit(self, unit_id: str) -> None:
        """
        Unload a unit's model to free memory.

        Args:
            unit_id: Unit identifier.
        """
        if unit_id in self.activation_trackers:
            self.activation_trackers[unit_id].remove_hooks()
            del self.activation_trackers[unit_id]

        if unit_id in self.models:
            del self.models[unit_id]

        if unit_id in self.tokenizers:
            del self.tokenizers[unit_id]

        if unit_id in self.expert_registries:
            del self.expert_registries[unit_id]

        # Clear CUDA cache
        if TORCH_AVAILABLE and torch.cuda.is_available():
            torch.cuda.empty_cache()

        logger.info("model_unloaded", unit_id=unit_id)

    def generate(
        self,
        unit_id: str,
        prompt: str,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True,
    ) -> InferenceResult:
        """
        Generate response from MoE model.

        Args:
            unit_id: Unit to use for generation.
            prompt: User prompt.
            max_new_tokens: Maximum new tokens to generate.
            temperature: Sampling temperature.
            top_p: Top-p sampling parameter.
            do_sample: Whether to use sampling.

        Returns:
            InferenceResult with response and activations.
        """
        if unit_id not in self.models:
            if not self.load_unit(unit_id):
                return InferenceResult(
                    response=f"Error: Failed to load model for unit '{unit_id}'",
                    activations=[],
                )

        model = self.models[unit_id]
        tokenizer = self.tokenizers[unit_id]
        tracker = self.activation_trackers[unit_id]

        # Clear previous activations
        tracker.clear()

        try:
            import time

            start_time = time.time()

            # Tokenize input
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=2048,
            )

            # Move to device
            if hasattr(model, "device"):
                inputs = {k: v.to(model.device) for k, v in inputs.items()}

            # Generate
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature if do_sample else 1.0,
                    top_p=top_p if do_sample else 1.0,
                    do_sample=do_sample,
                    pad_token_id=tokenizer.pad_token_id,
                )

            generation_time = (time.time() - start_time) * 1000

            # Decode response
            input_length = inputs["input_ids"].shape[1]
            generated_tokens = outputs[0][input_length:]
            response = tokenizer.decode(generated_tokens, skip_special_tokens=True)

            # Get expert activations
            activations = tracker.get_top_activations(top_k=5)

            logger.info(
                "generation_complete",
                unit_id=unit_id,
                tokens_generated=len(generated_tokens),
                generation_time_ms=generation_time,
                num_activations=len(activations),
            )

            return InferenceResult(
                response=response,
                activations=activations,
                tokens_generated=len(generated_tokens),
                generation_time_ms=generation_time,
            )

        except Exception as e:
            logger.error("generation_failed", unit_id=unit_id, error=str(e))
            return InferenceResult(
                response=f"Error during generation: {str(e)}",
                activations=[],
            )

    def is_loaded(self, unit_id: str) -> bool:
        """Check if a unit's model is loaded."""
        return unit_id in self.models
