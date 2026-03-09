"""
Model Evaluator

Evaluates fine-tuned orchestrator models against baselines.
"""

from pathlib import Path
from typing import Any, Optional
import json
import time
import torch
from habitat_logging import get_logger

logger = get_logger(__name__)


class OrchestratorEvaluator:
    """
    Evaluates orchestrator models.

    Metrics:
    - Routing accuracy (correct entry agent)
    - Depth prediction accuracy
    - Inference latency
    - Comparison against baselines
    """

    def __init__(self, model_path: Path, device: Optional[str] = None):
        """
        Initialize evaluator.

        Args:
            model_path: Path to fine-tuned model/adapter
            device: Device to use (cuda/cpu/mps)
        """
        self.model_path = Path(model_path)
        self.device = device or self._auto_detect_device()
        self.logger = logger.bind(component="orchestrator_evaluator")

        self.model = None
        self.tokenizer = None

    def _auto_detect_device(self) -> str:
        """Auto-detect available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def load_model(self) -> None:
        """Load model for evaluation"""
        self.logger.info("loading_model", path=str(self.model_path), device=self.device)

        from ..shared.model_loader import OrchestratorModelLoader

        loader = OrchestratorModelLoader(self.model_path, device=self.device)
        self.model, self.tokenizer = loader.load_for_inference()

        self.logger.info("model_loaded")

    def evaluate(
        self,
        test_dataset_path: Path,
        max_samples: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Evaluate model on test dataset.

        Args:
            test_dataset_path: Path to test dataset (JSONL)
            max_samples: Maximum number of samples to evaluate

        Returns:
            Evaluation metrics
        """
        self.logger.info(
            "evaluating_model",
            test_dataset=str(test_dataset_path),
            max_samples=max_samples
        )

        # Load test examples
        test_examples = []
        with open(test_dataset_path) as f:
            for i, line in enumerate(f):
                if max_samples and i >= max_samples:
                    break
                if line.strip():
                    test_examples.append(json.loads(line))

        # Run evaluation
        results = {
            "total_examples": len(test_examples),
            "correct_agent": 0,
            "correct_depth": 0,
            "correct_both": 0,
            "avg_latency_ms": 0,
            "predictions": []
        }

        total_latency = 0

        for example in test_examples:
            # Get ground truth
            messages = example.get("messages", [])
            metadata = example.get("metadata", {})

            ground_truth_agent = self._extract_agent_from_messages(messages)
            ground_truth_depth = metadata.get("optimal_depth", 2)

            # Get user query
            user_query = self._extract_query_from_messages(messages)

            # Predict
            start_time = time.time()
            prediction = self._predict(user_query)
            latency_ms = (time.time() - start_time) * 1000

            total_latency += latency_ms

            # Evaluate prediction
            pred_agent = self._extract_predicted_agent(prediction)
            pred_depth = self._extract_predicted_depth(prediction)

            correct_agent = pred_agent == ground_truth_agent
            correct_depth = pred_depth == ground_truth_depth
            correct_both = correct_agent and correct_depth

            if correct_agent:
                results["correct_agent"] += 1
            if correct_depth:
                results["correct_depth"] += 1
            if correct_both:
                results["correct_both"] += 1

            # Store prediction
            results["predictions"].append({
                "query": user_query,
                "ground_truth": {
                    "agent": ground_truth_agent,
                    "depth": ground_truth_depth
                },
                "prediction": {
                    "agent": pred_agent,
                    "depth": pred_depth,
                    "raw": prediction
                },
                "correct_agent": correct_agent,
                "correct_depth": correct_depth,
                "latency_ms": latency_ms
            })

        # Compute metrics
        n = len(test_examples)
        results["accuracy_agent"] = results["correct_agent"] / n if n > 0 else 0
        results["accuracy_depth"] = results["correct_depth"] / n if n > 0 else 0
        results["accuracy_both"] = results["correct_both"] / n if n > 0 else 0
        results["avg_latency_ms"] = total_latency / n if n > 0 else 0

        self.logger.info(
            "evaluation_complete",
            accuracy_agent=f"{results['accuracy_agent']:.2%}",
            accuracy_depth=f"{results['accuracy_depth']:.2%}",
            accuracy_both=f"{results['accuracy_both']:.2%}",
            avg_latency_ms=f"{results['avg_latency_ms']:.0f}ms"
        )

        return results

    def _predict(self, query: str) -> str:
        """
        Generate prediction for a query.

        Args:
            query: User query

        Returns:
            Model prediction
        """
        prompt = f"""<|system|>
You are an AI orchestrator that coordinates multiple specialized agents.

Your responsibilities:
1. Analyze user queries and determine which agents to call
2. Decide the optimal cascade depth (how many levels of agent calls)
3. Decompose complex queries into sub-tasks
4. Route sub-tasks to appropriate agents
5. Synthesize responses from multiple agents

Available agents:
- fundraising-agent: Investor profiles, capacity, interests
- business-development-agent: RFP data, competitive landscape
- field-operations-agent: Local capacity, project performance

For each query, output:
1. Entry agent (which agent should handle this)
2. Optimal depth (1-4, how many cascade levels needed)
3. Rationale (why this routing and depth)
<|end|>
<|user|>
Query: {query}<|end|>
<|assistant|>
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.1,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        prediction = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract just the assistant's response
        if "<|assistant|>" in prediction:
            prediction = prediction.split("<|assistant|>")[-1].strip()

        return prediction

    def _extract_agent_from_messages(self, messages: list[dict]) -> str:
        """Extract ground truth agent from messages"""
        for msg in messages:
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                if "Entry agent:" in content:
                    lines = content.split("\n")
                    for line in lines:
                        if "Entry agent:" in line:
                            agent = line.split("Entry agent:")[-1].strip()
                            return agent

        return "unknown"

    def _extract_query_from_messages(self, messages: list[dict]) -> str:
        """Extract user query from messages"""
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if "Query:" in content:
                    return content.split("Query:")[-1].strip()

        return ""

    def _extract_predicted_agent(self, prediction: str) -> str:
        """Extract predicted agent from model output"""
        if "Entry agent:" in prediction:
            lines = prediction.split("\n")
            for line in lines:
                if "Entry agent:" in line:
                    agent = line.split("Entry agent:")[-1].strip()
                    return agent

        return "unknown"

    def _extract_predicted_depth(self, prediction: str) -> int:
        """Extract predicted depth from model output"""
        if "Optimal depth:" in prediction:
            lines = prediction.split("\n")
            for line in lines:
                if "Optimal depth:" in line:
                    depth_str = line.split("Optimal depth:")[-1].strip()
                    try:
                        return int(depth_str.split()[0])
                    except (ValueError, IndexError):
                        return 2

        return 2  # Default

    def export_results(self, results: dict[str, Any], output_path: Path) -> None:
        """
        Export evaluation results.

        Args:
            results: Evaluation results
            output_path: Path to save results
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

        self.logger.info("results_exported", path=str(output_path))

    def compare_with_baseline(
        self,
        results: dict[str, Any],
        baseline_accuracy: float = 0.8,
        baseline_latency_ms: float = 200
    ) -> dict[str, Any]:
        """
        Compare results with baseline.

        Args:
            results: Evaluation results
            baseline_accuracy: Baseline accuracy
            baseline_latency_ms: Baseline latency

        Returns:
            Comparison metrics
        """
        comparison = {
            "model_accuracy": results["accuracy_both"],
            "baseline_accuracy": baseline_accuracy,
            "accuracy_improvement": results["accuracy_both"] - baseline_accuracy,
            "model_latency_ms": results["avg_latency_ms"],
            "baseline_latency_ms": baseline_latency_ms,
            "latency_improvement_ms": baseline_latency_ms - results["avg_latency_ms"],
            "passes_accuracy_target": results["accuracy_both"] >= baseline_accuracy,
            "passes_latency_target": results["avg_latency_ms"] <= baseline_latency_ms
        }

        self.logger.info("baseline_comparison", comparison=comparison)

        return comparison
