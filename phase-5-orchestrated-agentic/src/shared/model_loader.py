"""
Model Loader

Utilities for loading fine-tuned orchestrator models with LoRA adapters.
"""

from pathlib import Path
from typing import Optional, Any
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
from phase0_infra.habitat_logging import get_logger

logger = get_logger(__name__)


class OrchestratorModelLoader:
    """
    Loads fine-tuned orchestrator models.

    Supports:
    - Base models with LoRA adapters
    - Merged models
    - Quantized models (8-bit, 4-bit)
    """

    def __init__(self, model_dir: Path, device: Optional[str] = None):
        """
        Initialize model loader.

        Args:
            model_dir: Directory containing the model
            device: Device to load on (cuda/cpu/mps). Auto-detect if None.
        """
        self.model_dir = Path(model_dir)
        self.device = device or self._auto_detect_device()
        self.logger = logger.bind(component="model_loader")

    def _auto_detect_device(self) -> str:
        """Auto-detect available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def load_model_and_tokenizer(
        self,
        load_in_8bit: bool = False,
        load_in_4bit: bool = False,
        use_flash_attention: bool = False
    ) -> tuple[Any, Any]:
        """
        Load model and tokenizer.

        Args:
            load_in_8bit: Load in 8-bit mode
            load_in_4bit: Load in 4-bit mode
            use_flash_attention: Use Flash Attention 2

        Returns:
            (model, tokenizer) tuple
        """
        self.logger.info(
            "loading_model",
            model_dir=str(self.model_dir),
            device=self.device,
            load_in_8bit=load_in_8bit,
            load_in_4bit=load_in_4bit
        )

        # Check if this is a LoRA adapter or merged model
        adapter_config = self.model_dir / "adapter_config.json"
        is_adapter = adapter_config.exists()

        if is_adapter:
            return self._load_with_adapter(
                load_in_8bit=load_in_8bit,
                load_in_4bit=load_in_4bit,
                use_flash_attention=use_flash_attention
            )
        else:
            return self._load_merged_model(
                load_in_8bit=load_in_8bit,
                load_in_4bit=load_in_4bit,
                use_flash_attention=use_flash_attention
            )

    def _load_with_adapter(
        self,
        load_in_8bit: bool = False,
        load_in_4bit: bool = False,
        use_flash_attention: bool = False
    ) -> tuple[Any, Any]:
        """Load base model with LoRA adapter"""
        self.logger.info("loading_with_adapter")

        # Load adapter config to get base model
        config = PeftConfig.from_pretrained(self.model_dir)
        base_model_name = config.base_model_name_or_path

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Load base model
        model_kwargs = {
            "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            "device_map": "auto" if self.device == "cuda" else None,
        }

        if load_in_8bit:
            model_kwargs["load_in_8bit"] = True
        elif load_in_4bit:
            model_kwargs["load_in_4bit"] = True

        if use_flash_attention and self.device == "cuda":
            model_kwargs["attn_implementation"] = "flash_attention_2"

        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            **model_kwargs
        )

        # Load adapter
        model = PeftModel.from_pretrained(base_model, self.model_dir)

        self.logger.info(
            "adapter_loaded",
            base_model=base_model_name,
            adapter_path=str(self.model_dir)
        )

        return model, tokenizer

    def _load_merged_model(
        self,
        load_in_8bit: bool = False,
        load_in_4bit: bool = False,
        use_flash_attention: bool = False
    ) -> tuple[Any, Any]:
        """Load merged model (no adapter)"""
        self.logger.info("loading_merged_model")

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Load model
        model_kwargs = {
            "torch_dtype": torch.float16 if self.device == "cuda" else torch.float32,
            "device_map": "auto" if self.device == "cuda" else None,
        }

        if load_in_8bit:
            model_kwargs["load_in_8bit"] = True
        elif load_in_4bit:
            model_kwargs["load_in_4bit"] = True

        if use_flash_attention and self.device == "cuda":
            model_kwargs["attn_implementation"] = "flash_attention_2"

        model = AutoModelForCausalLM.from_pretrained(
            self.model_dir,
            **model_kwargs
        )

        self.logger.info("merged_model_loaded", model_path=str(self.model_dir))

        return model, tokenizer

    def load_for_inference(self) -> tuple[Any, Any]:
        """
        Load model optimized for inference.

        Uses:
        - 8-bit quantization on CUDA
        - Float32 on CPU/MPS
        - Flash Attention 2 if available

        Returns:
            (model, tokenizer) tuple
        """
        use_8bit = self.device == "cuda"
        use_flash = self.device == "cuda"

        model, tokenizer = self.load_model_and_tokenizer(
            load_in_8bit=use_8bit,
            use_flash_attention=use_flash
        )

        # Set to eval mode
        model.eval()

        return model, tokenizer

    @staticmethod
    def create_mock_model_for_testing(model_dir: Path) -> None:
        """
        Create mock model files for testing (test mode).

        Args:
            model_dir: Directory to create mock files in
        """
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        # Create mock adapter config
        import json

        adapter_config = {
            "base_model_name_or_path": "Qwen/Qwen2.5-7B",
            "peft_type": "LORA",
            "task_type": "CAUSAL_LM",
            "r": 16,
            "lora_alpha": 32,
            "target_modules": ["q_proj", "v_proj"],
            "lora_dropout": 0.05
        }

        with open(model_dir / "adapter_config.json", "w") as f:
            json.dump(adapter_config, f, indent=2)

        # Create mock adapter weights
        torch.save(
            {"adapter_model": {"mock": "weights"}},
            model_dir / "adapter_model.bin"
        )

        logger.info("mock_model_created", path=str(model_dir))
