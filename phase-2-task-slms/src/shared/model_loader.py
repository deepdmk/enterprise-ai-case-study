"""Model loader abstraction for Unsloth and HuggingFace backends."""

import sys
from pathlib import Path
from typing import Any

import torch

# Import local config BEFORE adding phase-0 to path to avoid conflicts
from config.settings import LoRAConfig, ModelConfig, Settings

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger
from src.shared.environment_detector import detect_environment, get_device, get_dtype

logger = get_logger(__name__)


class ModelLoader:
    """Abstract model loading for Unsloth and HuggingFace backends."""

    def __init__(self, settings: Settings | None = None):
        """Initialize the model loader."""
        self.settings = settings or Settings()
        self.env_info = detect_environment()
        self._model = None
        self._tokenizer = None
        self._backend = None

    @property
    def backend(self) -> str:
        """Get the active backend."""
        return self._backend or self.env_info.recommended_backend

    def load_base_model(
        self,
        model_config: ModelConfig | None = None,
        force_backend: str | None = None,
    ) -> tuple[Any, Any]:
        """
        Load the base model and tokenizer.

        Args:
            model_config: Model configuration. Uses settings default if not provided.
            force_backend: Force a specific backend ('unsloth' or 'transformers').

        Returns:
            Tuple of (model, tokenizer)
        """
        config = model_config or self.settings.model
        backend = force_backend or self.env_info.recommended_backend

        logger.info(
            "loading_base_model",
            model=config.base_model,
            backend=backend,
            max_seq_length=config.max_seq_length,
        )

        if backend == "unsloth" and self.env_info.can_use_unsloth:
            model, tokenizer = self._load_with_unsloth(config)
            self._backend = "unsloth"
        else:
            model, tokenizer = self._load_with_transformers(config)
            self._backend = "transformers"

        self._model = model
        self._tokenizer = tokenizer

        logger.info("model_loaded", backend=self._backend)
        return model, tokenizer

    def _load_with_unsloth(self, config: ModelConfig) -> tuple[Any, Any]:
        """Load model using Unsloth (fast path)."""
        try:
            from unsloth import FastLanguageModel

            model, tokenizer = FastLanguageModel.from_pretrained(
                model_name=config.base_model,
                max_seq_length=config.max_seq_length,
                dtype=None,  # Auto-detect
                load_in_4bit=config.load_in_4bit,
            )
            return model, tokenizer
        except ImportError as e:
            logger.warning("unsloth_import_failed", error=str(e))
            return self._load_with_transformers(config)

    def _load_with_transformers(self, config: ModelConfig) -> tuple[Any, Any]:
        """Load model using HuggingFace Transformers (fallback path)."""
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        # Configure quantization if requested
        quantization_config = None
        if config.load_in_4bit:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=get_dtype(),
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        tokenizer = AutoTokenizer.from_pretrained(
            config.base_model,
            trust_remote_code=True,
        )

        # Ensure tokenizer has padding token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            config.base_model,
            quantization_config=quantization_config,
            device_map="auto" if self.env_info.has_cuda else None,
            torch_dtype=get_dtype(),
            trust_remote_code=True,
        )

        return model, tokenizer

    def apply_lora(
        self,
        model: Any,
        lora_config: LoRAConfig | None = None,
    ) -> Any:
        """
        Apply LoRA adapters to the model.

        Args:
            model: The base model
            lora_config: LoRA configuration. Uses settings default if not provided.

        Returns:
            Model with LoRA adapters applied
        """
        config = lora_config or self.settings.lora

        logger.info(
            "applying_lora",
            r=config.r,
            alpha=config.lora_alpha,
            targets=config.target_modules,
            backend=self._backend,
        )

        if self._backend == "unsloth":
            model = self._apply_lora_unsloth(model, config)
        else:
            model = self._apply_lora_peft(model, config)

        return model

    def _apply_lora_unsloth(self, model: Any, config: LoRAConfig) -> Any:
        """Apply LoRA using Unsloth."""
        from unsloth import FastLanguageModel

        model = FastLanguageModel.get_peft_model(
            model,
            r=config.r,
            lora_alpha=config.lora_alpha,
            lora_dropout=config.lora_dropout,
            target_modules=config.target_modules,
            use_rslora=config.use_rslora,
            bias=config.bias,
        )
        return model

    def _apply_lora_peft(self, model: Any, config: LoRAConfig) -> Any:
        """Apply LoRA using PEFT."""
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

        # Prepare model for training if quantized
        model = prepare_model_for_kbit_training(model)

        peft_config = LoraConfig(
            r=config.r,
            lora_alpha=config.lora_alpha,
            lora_dropout=config.lora_dropout,
            target_modules=config.target_modules,
            bias=config.bias,
            task_type=config.task_type,
        )

        model = get_peft_model(model, peft_config)
        return model

    def load_for_inference(
        self,
        adapter_path: str | Path,
        base_model: str | None = None,
        merge_adapter: bool = False,
    ) -> tuple[Any, Any]:
        """
        Load a trained adapter for inference.

        Args:
            adapter_path: Path to the saved LoRA adapter
            base_model: Base model name (uses settings default if not provided)
            merge_adapter: Whether to merge the adapter into the base model

        Returns:
            Tuple of (model, tokenizer)
        """
        adapter_path = Path(adapter_path)
        base_model = base_model or self.settings.model.base_model

        logger.info(
            "loading_for_inference",
            adapter_path=str(adapter_path),
            base_model=base_model,
            merge_adapter=merge_adapter,
        )

        if self._backend == "unsloth" or self.env_info.can_use_unsloth:
            return self._load_inference_unsloth(adapter_path, merge_adapter)
        else:
            return self._load_inference_peft(adapter_path, base_model, merge_adapter)

    def _load_inference_unsloth(
        self,
        adapter_path: Path,
        merge_adapter: bool,
    ) -> tuple[Any, Any]:
        """Load adapter for inference using Unsloth."""
        from unsloth import FastLanguageModel

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=str(adapter_path),
            max_seq_length=self.settings.model.max_seq_length,
            dtype=None,
            load_in_4bit=self.settings.model.load_in_4bit,
        )

        if merge_adapter:
            model = model.merge_and_unload()

        # Enable faster inference
        FastLanguageModel.for_inference(model)

        return model, tokenizer

    def _load_inference_peft(
        self,
        adapter_path: Path,
        base_model: str,
        merge_adapter: bool,
    ) -> tuple[Any, Any]:
        """Load adapter for inference using PEFT."""
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        tokenizer = AutoTokenizer.from_pretrained(base_model)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        quantization_config = None
        if self.settings.model.load_in_4bit:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=get_dtype(),
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            quantization_config=quantization_config,
            device_map="auto" if self.env_info.has_cuda else None,
            torch_dtype=get_dtype(),
        )

        model = PeftModel.from_pretrained(model, str(adapter_path))

        if merge_adapter:
            model = model.merge_and_unload()

        model.eval()
        return model, tokenizer

    def save_adapter(
        self,
        model: Any,
        tokenizer: Any,
        output_path: str | Path,
        save_merged: bool = False,
    ) -> Path:
        """
        Save the trained LoRA adapter.

        Args:
            model: The trained model with LoRA adapter
            tokenizer: The tokenizer
            output_path: Directory to save the adapter
            save_merged: Whether to save the merged model (larger file)

        Returns:
            Path to the saved adapter
        """
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        logger.info(
            "saving_adapter",
            output_path=str(output_path),
            save_merged=save_merged,
            backend=self._backend,
        )

        if save_merged:
            if self._backend == "unsloth":
                model.save_pretrained_merged(
                    str(output_path),
                    tokenizer,
                    save_method="merged_16bit",
                )
            else:
                merged_model = model.merge_and_unload()
                merged_model.save_pretrained(str(output_path))
                tokenizer.save_pretrained(str(output_path))
        else:
            model.save_pretrained(str(output_path))
            tokenizer.save_pretrained(str(output_path))

        logger.info("adapter_saved", output_path=str(output_path))
        return output_path

    def generate(
        self,
        model: Any,
        tokenizer: Any,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """
        Generate text using the model.

        Args:
            model: The model (with or without LoRA)
            tokenizer: The tokenizer
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter

        Returns:
            Generated text
        """
        device = get_device()

        inputs = tokenizer(prompt, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=temperature > 0,
                pad_token_id=tokenizer.pad_token_id,
            )

        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove the input prompt from the output
        if generated.startswith(prompt):
            generated = generated[len(prompt) :].strip()

        return generated
