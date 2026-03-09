"""
MoE Model Loader
Loads Phase 3 Mixture-of-Experts models for use in A2A agents.
"""

import sys
from pathlib import Path
from typing import Optional, Any, TYPE_CHECKING

from src.shared.path_config import configure_paths, PHASE3_ROOT

if TYPE_CHECKING:
    pass


class MoEModelLoader:
    """
    Loads MoE models from Phase 3 for use in agent services.

    Supports loading base models and applying A2A LoRA adapters.
    """

    def __init__(
        self,
        phase3_path: Optional[Path] = None,
        device: Optional[str] = None
    ):
        """
        Initialize MoE model loader.

        Args:
            phase3_path: Path to phase-3-moe-experts directory
            device: Device to load models on (cuda/cpu/mps)
        """
        self.phase3_path = phase3_path or self._find_phase3_path()
        self.device = device or self._get_default_device()

        # Configure paths for cross-phase imports (Phase 3 for MoE utilities)
        configure_paths()
        if self.phase3_path:
            phase3_src = str(self.phase3_path / "src")
            if phase3_src not in sys.path:
                sys.path.insert(0, phase3_src)
        elif PHASE3_ROOT.exists():
            phase3_src = str(PHASE3_ROOT / "src")
            if phase3_src not in sys.path:
                sys.path.insert(0, phase3_src)

    def load_unit_model(
        self,
        unit_name: str,
        with_a2a_adapter: bool = False,
        adapter_path: Optional[Path] = None
    ) -> Any:
        """
        Load a unit-specific MoE model.

        Args:
            unit_name: Unit name (e.g., "fundraising")
            with_a2a_adapter: Whether to load A2A LoRA adapter
            adapter_path: Custom path to A2A adapter

        Returns:
            Loaded model (transformers model or PEFT model)
        """
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from peft import PeftModel
        except ImportError:
            raise ImportError(
                "transformers and peft required. Install with: "
                "pip install transformers peft"
            )

        # Determine model path
        model_path = self._get_model_path(unit_name)

        # Load base model
        import torch
        print(f"Loading MoE model for {unit_name} from {model_path}")
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )

        if self.device != "cuda":
            model = model.to(self.device)

        # Load A2A adapter if requested
        if with_a2a_adapter:
            adapter_path = adapter_path or self._get_a2a_adapter_path(unit_name)
            if adapter_path and adapter_path.exists():
                print(f"Loading A2A adapter from {adapter_path}")
                model = PeftModel.from_pretrained(
                    model,
                    str(adapter_path),
                    is_trainable=False
                )
            else:
                print(f"Warning: A2A adapter not found at {adapter_path}, using base model")

        return model

    def load_tokenizer(self, unit_name: str) -> Any:
        """
        Load tokenizer for a unit model.

        Args:
            unit_name: Unit name

        Returns:
            Tokenizer
        """
        try:
            from transformers import AutoTokenizer
        except ImportError:
            raise ImportError("transformers required")

        model_path = self._get_model_path(unit_name)
        tokenizer = AutoTokenizer.from_pretrained(str(model_path))

        # Ensure pad token is set
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        return tokenizer

    def get_model_info(self, unit_name: str) -> dict[str, Any]:
        """
        Get information about a model without loading it.

        Args:
            unit_name: Unit name

        Returns:
            Dictionary with model info
        """
        model_path = self._get_model_path(unit_name)
        a2a_adapter_path = self._get_a2a_adapter_path(unit_name)

        return {
            "unit_name": unit_name,
            "model_path": str(model_path),
            "model_exists": model_path.exists(),
            "a2a_adapter_path": str(a2a_adapter_path),
            "a2a_adapter_exists": a2a_adapter_path.exists(),
            "device": self.device
        }

    def _find_phase3_path(self) -> Optional[Path]:
        """Try to find phase-3-moe-experts directory"""
        # Look in common locations
        possible_paths = [
            Path.cwd().parent / "phase-3-moe-experts",
            Path.cwd() / ".." / "phase-3-moe-experts",
            Path.cwd() / "phase-3-moe-experts"
        ]

        for path in possible_paths:
            if path.exists():
                return path.resolve()

        return None

    def _get_model_path(self, unit_name: str) -> Path:
        """Get path to unit model"""
        if self.phase3_path:
            # Try phase4 export directory first
            phase4_export = self.phase3_path / "data" / "exports" / "phase4" / unit_name
            if phase4_export.exists():
                return phase4_export

            # Fall back to models directory
            return self.phase3_path / "data" / "models" / unit_name

        # Default to local path if Phase 3 not found
        return Path.cwd() / "data" / "models" / unit_name

    def _get_a2a_adapter_path(self, unit_name: str) -> Path:
        """Get path to A2A LoRA adapter"""
        return Path.cwd() / "data" / "models" / "a2a_adapters" / unit_name

    def _get_default_device(self) -> str:
        """Determine default device"""
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
        except ImportError:
            pass
        return "cpu"


class MockMoEModel:
    """
    Mock MoE model for testing without loading actual models.

    Simulates model behavior for integration testing.
    """

    def __init__(self, unit_name: str):
        self.unit_name = unit_name
        self.config = type('Config', (), {'max_length': 512})()

    def generate(self, input_ids, **kwargs):
        """Mock generate method"""
        # Return dummy output
        return input_ids

    def __call__(self, *args, **kwargs):
        """Mock forward pass"""
        import torch
        batch_size = args[0].shape[0] if args else 1
        seq_len = args[0].shape[1] if args else 10
        vocab_size = 32000

        return type('Output', (), {
            'logits': torch.randn(batch_size, seq_len, vocab_size)
        })()


class MockTokenizer:
    """Mock tokenizer for testing"""

    def __init__(self):
        self.pad_token = "[PAD]"
        self.eos_token = "[EOS]"
        self.pad_token_id = 0
        self.eos_token_id = 1

    def __call__(self, text, **kwargs):
        """Mock tokenization"""
        import torch
        return {
            'input_ids': torch.randint(0, 1000, (1, 10)),
            'attention_mask': torch.ones(1, 10)
        }

    def decode(self, token_ids, **kwargs):
        """Mock decoding"""
        return f"Mock response from model"

    def batch_decode(self, token_ids, **kwargs):
        """Mock batch decoding"""
        return [self.decode(ids) for ids in token_ids]
