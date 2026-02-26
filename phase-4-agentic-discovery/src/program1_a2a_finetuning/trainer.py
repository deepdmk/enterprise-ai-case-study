"""
A2A Fine-Tuning Trainer

Fine-tunes Phase 3 MoE models with LoRA to add A2A protocol capabilities.
"""

from pathlib import Path
from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import torch

from ..shared.phase0_integration import get_phase0_integration


class A2AFineTuner:
    """
    Fine-tunes MoE models to understand and generate A2A protocol calls.

    Uses LoRA (Low-Rank Adaptation) to add A2A capabilities on top of
    existing Phase 3 MoE models without catastrophic forgetting.
    """

    def __init__(
        self,
        unit_name: str,
        base_model_path: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        device: Optional[str] = None,
        test_mode: bool = False
    ):
        """
        Initialize A2A fine-tuner.

        Args:
            unit_name: Unit name to fine-tune
            base_model_path: Path to base MoE model (from Phase 3)
            output_dir: Where to save the fine-tuned adapter
            device: Device to train on (cuda/cpu/mps)
            test_mode: If True, use test mode
        """
        self.unit_name = unit_name
        self.base_model_path = base_model_path
        self.output_dir = output_dir or Path.cwd() / "data" / "models" / "a2a_adapters" / unit_name
        self.device = device or self._get_default_device()
        self.test_mode = test_mode

        # Training config
        self.lora_config = {
            "r": 16,  # LoRA rank
            "lora_alpha": 32,
            "target_modules": ["q_proj", "v_proj"],  # Attention layers
            "lora_dropout": 0.05,
            "bias": "none",
            "task_type": "CAUSAL_LM"
        }

        self.training_config = {
            "num_train_epochs": 3,
            "per_device_train_batch_size": 4,
            "gradient_accumulation_steps": 4,
            "learning_rate": 2e-4,
            "warmup_steps": 100,
            "logging_steps": 10,
            "save_steps": 500,
            "max_seq_length": 512,
            "fp16": self.device == "cuda",
            "optim": "adamw_torch"
        }

    def train(
        self,
        dataset_path: Path,
        test_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Train A2A adapter on the dataset.

        Args:
            dataset_path: Path to training dataset (JSONL)
            test_mode: If True, use mock model for testing

        Returns:
            Training results including metrics and paths
        """
        # Initialize Phase 0 integration
        phase0 = get_phase0_integration(Path.cwd() / "data", test_mode=test_mode)
        experiment_id = f"phase-4/{self.unit_name}/a2a-finetuning/v1"

        # Start experiment tracking
        if phase0["available"]:
            phase0["experiment_tracker"].log_a2a_finetuning_experiment(
                experiment_id=experiment_id,
                unit_name=self.unit_name,
                config={
                    "base_model_path": str(self.base_model_path),
                    "lora_config": self.lora_config,
                    "training_config": self.training_config,
                    "dataset_path": str(dataset_path)
                }
            )

        if test_mode:
            result = self._train_mock(dataset_path)

            # Complete experiment and register model
            model_id = f"phase-4/{self.unit_name}/a2a-adapter/v1"
            if phase0["available"]:
                phase0["model_registry"].register_a2a_adapter(
                    model_id=model_id,
                    unit_name=self.unit_name,
                    adapter_path=self.output_dir,
                    base_model=str(self.base_model_path) if self.base_model_path else f"{self.unit_name}_moe",
                    source_dataset_id=f"phase-4/{self.unit_name}/a2a-training/v1",
                    lora_config=self.lora_config,
                    tags=["a2a", "protocol", "lora", "mock"]
                )

                phase0["experiment_tracker"].complete_experiment(
                    experiment_id=experiment_id,
                    model_id=model_id
                )

            return result

        try:
            import torch
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                TrainingArguments,
                Trainer
            )
            from peft import (
                get_peft_model,
                LoraConfig,
                TaskType,
                prepare_model_for_kbit_training
            )
            from datasets import load_dataset
            from trl import SFTTrainer
        except ImportError:
            raise ImportError(
                "Required packages not installed. Install with: "
                "pip install transformers peft trl datasets"
            )

        print(f"\n{'='*60}")
        print(f"A2A Fine-Tuning for {self.unit_name}")
        print(f"{'='*60}\n")

        # Load base model
        print(f"Loading base model from {self.base_model_path}")
        model = AutoModelForCausalLM.from_pretrained(
            str(self.base_model_path),
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )

        tokenizer = AutoTokenizer.from_pretrained(str(self.base_model_path))
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Prepare model for training
        if self.device == "cuda":
            model = prepare_model_for_kbit_training(model)

        # Configure LoRA
        print("\nConfiguring LoRA adapter...")
        lora_config = LoraConfig(
            r=self.lora_config["r"],
            lora_alpha=self.lora_config["lora_alpha"],
            target_modules=self.lora_config["target_modules"],
            lora_dropout=self.lora_config["lora_dropout"],
            bias=self.lora_config["bias"],
            task_type=TaskType.CAUSAL_LM
        )

        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

        # Load dataset
        print(f"\nLoading dataset from {dataset_path}")
        dataset = load_dataset("json", data_files=str(dataset_path), split="train")
        print(f"Dataset size: {len(dataset)} examples")

        # Split train/eval
        split_dataset = dataset.train_test_split(test_size=0.1)
        train_dataset = split_dataset["train"]
        eval_dataset = split_dataset["test"]

        # Training arguments
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=self.training_config["num_train_epochs"],
            per_device_train_batch_size=self.training_config["per_device_train_batch_size"],
            gradient_accumulation_steps=self.training_config["gradient_accumulation_steps"],
            learning_rate=self.training_config["learning_rate"],
            warmup_steps=self.training_config["warmup_steps"],
            logging_steps=self.training_config["logging_steps"],
            save_steps=self.training_config["save_steps"],
            fp16=self.training_config["fp16"],
            optim=self.training_config["optim"],
            evaluation_strategy="steps",
            eval_steps=self.training_config["save_steps"],
            save_total_limit=3,
            load_best_model_at_end=True,
            report_to="none"  # Disable wandb/tensorboard
        )

        # Initialize trainer
        print("\nInitializing trainer...")
        trainer = SFTTrainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=tokenizer,
            max_seq_length=self.training_config["max_seq_length"],
            dataset_text_field="messages",
            packing=False
        )

        # Train
        print("\nStarting training...")
        trainer.train()

        # Save final adapter
        print(f"\nSaving adapter to {self.output_dir}")
        model.save_pretrained(str(self.output_dir))
        tokenizer.save_pretrained(str(self.output_dir))

        print("\n✓ Training complete!")

        # Get final metrics
        final_metrics = {
            "final_train_loss": trainer.state.log_history[-1].get("loss", 0.0) if trainer.state.log_history else 0.0,
            "total_steps": trainer.state.global_step,
            "adapter_path": str(self.output_dir)
        }

        # Complete experiment and register model
        model_id = f"phase-4/{self.unit_name}/a2a-adapter/v1"
        if phase0["available"]:
            phase0["model_registry"].register_a2a_adapter(
                model_id=model_id,
                unit_name=self.unit_name,
                adapter_path=self.output_dir,
                base_model=str(self.base_model_path) if self.base_model_path else f"{self.unit_name}_moe",
                source_dataset_id=f"phase-4/{self.unit_name}/a2a-training/v1",
                lora_config=self.lora_config,
                tags=["a2a", "protocol", "lora"]
            )

            phase0["experiment_tracker"].complete_experiment(
                experiment_id=experiment_id,
                model_id=model_id
            )

        return final_metrics

    def _train_mock(self, dataset_path: Path) -> Dict[str, Any]:
        """Mock training for testing"""
        print(f"\n{'='*60}")
        print(f"MOCK A2A Fine-Tuning for {self.unit_name}")
        print(f"{'='*60}\n")

        print(f"Loading dataset from {dataset_path}")
        import json
        with open(dataset_path) as f:
            examples = [json.loads(line) for line in f if line.strip()]
        print(f"Dataset size: {len(examples)} examples")

        print("\nConfiguring mock LoRA adapter...")
        print(f"  Rank: {self.lora_config['r']}")
        print(f"  Alpha: {self.lora_config['lora_alpha']}")
        print(f"  Target modules: {self.lora_config['target_modules']}")

        print("\nRunning mock training...")
        final_loss = 0.0
        for epoch in range(1, 4):
            loss = 1.5 / epoch
            final_loss = loss
            print(f"Epoch {epoch}/3 - Loss: {loss:.4f}")

        # Create mock output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save mock config
        import json
        config_file = self.output_dir / "adapter_config.json"
        with open(config_file, "w") as f:
            json.dump({
                "base_model_name_or_path": str(self.base_model_path),
                "unit_name": self.unit_name,
                "lora_config": self.lora_config,
                "mock_model": True
            }, f, indent=2)

        print(f"\n✓ Mock adapter saved to {self.output_dir}")

        return {
            "adapter_path": str(self.output_dir),
            "metrics": {
                "final_train_loss": final_loss,
                "total_steps": len(examples) * 3,
                "mock_training": True
            }
        }

    def validate(self, test_queries: Optional[list] = None) -> Dict[str, Any]:
        """
        Validate the fine-tuned model on test queries.

        Args:
            test_queries: List of test queries, or None for default

        Returns:
            Validation results
        """
        if test_queries is None:
            test_queries = self._get_default_test_queries()

        print(f"\nValidating A2A adapter for {self.unit_name}")
        print(f"{'='*60}\n")

        results = {
            "unit_name": self.unit_name,
            "adapter_path": str(self.output_dir),
            "test_cases": []
        }

        # Check if adapter exists
        if not (self.output_dir / "adapter_config.json").exists():
            print("⚠ Adapter not found - run training first")
            return results

        # Load mock config to check if it's a mock model
        import json
        with open(self.output_dir / "adapter_config.json") as f:
            config = json.load(f)

        if config.get("mock_model"):
            print("Running mock validation...\n")
            for i, query in enumerate(test_queries, 1):
                print(f"Test {i}: {query}")
                print(f"  → Mock A2A response generated ✓\n")
                results["test_cases"].append({
                    "query": query,
                    "status": "success",
                    "mock": True
                })
        else:
            # Real validation would load model and run inference
            print("Real model validation not implemented in test mode")

        print("✓ Validation complete")
        return results

    def _get_default_test_queries(self) -> list:
        """Get default test queries for validation"""
        queries_by_unit = {
            "fundraising": [
                "What is the investment capacity of INV-123?",
                "Compare investor INV-456 with competitive funders",
                "I need information about investor INV-789's local presence"
            ],
            "business_development": [
                "What RFPs are available in health sector?",
                "Which angel investors might be interested in RFP-2024-001?",
                "Analyze RFP-2024-002 including potential investors"
            ],
            "field_operations": [
                "What is the capacity of Kenya office?",
                "Which investors are active in Ghana?",
                "Create regional analysis for Tanzania"
            ]
        }
        return queries_by_unit.get(self.unit_name, ["Test query"])

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
