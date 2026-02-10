"""
Gradio Interface for MoE Staff Interaction.

Provides a web interface for staff to interact with organizational
unit MoE models, view expert activations, and provide feedback.
"""

import sys
from pathlib import Path
from typing import Any

import gradio as gr

# Import local config BEFORE adding phase-0 to path
from config.settings import InterfaceConfig, Settings

# Add phase-0-infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "phase-0-infrastructure"))
from habitat_logging import get_logger

from .feedback import InterfaceFeedbackCollector
from .mock_inference import ExpertActivation as MockExpertActivation
from .mock_inference import MockInferenceResult, MockMoEInference

# Import model loader and check if torch is available
from .model_loader import (
    ExpertActivation,
    InferenceResult,
    MoEModelLoader,
    TORCH_AVAILABLE as MODEL_LOADER_AVAILABLE,
)

logger = get_logger(__name__)


def format_expert_activations(
    activations: list[ExpertActivation] | list[MockExpertActivation],
) -> str:
    """Format expert activations for display."""
    if not activations:
        return "*No expert activation data available*"

    output = "### Activated Experts\n\n"
    output += "| Expert | Task | Activation Score |\n"
    output += "|--------|------|------------------|\n"

    for act in activations:
        score_bar = "=" * int(act.activation_score * 20)
        output += f"| {act.expert_id} | {act.task_id} | {act.activation_score:.4f} {score_bar} |\n"

    return output


class MoEInterfaceApp:
    """
    Gradio-based MoE interface application.

    Provides:
    - Unit selection dropdown
    - Prompt input
    - Generation parameter controls
    - Response display with expert activations
    - Feedback collection for RLHF
    """

    def __init__(
        self,
        inference_engine: MoEModelLoader | MockMoEInference,
        config: InterfaceConfig,
        feedback_collector: InterfaceFeedbackCollector | None = None,
        test_mode: bool = False,
    ):
        """
        Initialize the interface app.

        Args:
            inference_engine: MoE model loader or mock inference engine.
            config: Interface configuration.
            feedback_collector: Optional feedback collector for RLHF.
            test_mode: Whether running in test mode.
        """
        self.inference_engine = inference_engine
        self.config = config
        self.feedback_collector = feedback_collector
        self.test_mode = test_mode
        self._app: gr.Blocks | None = None

        # Session tracking
        self._current_session_id: str | None = None
        self._current_feedback_id: str | None = None
        self._current_result: InferenceResult | MockInferenceResult | None = None

        if self.feedback_collector:
            self._current_session_id = self.feedback_collector.create_session()

        logger.info(
            "moe_interface_app_initialized",
            test_mode=test_mode,
            feedback_enabled=feedback_collector is not None,
        )

    def generate_response(
        self,
        unit_id: str,
        prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> tuple[str, str]:
        """
        Generate response from selected unit's MoE model.

        Args:
            unit_id: Selected unit.
            prompt: User prompt.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.

        Returns:
            Tuple of (response_markdown, expert_activation_markdown).
        """
        if not prompt.strip():
            return "Please enter a prompt.", "*No generation performed*"

        if not unit_id:
            return "Please select a unit.", "*No generation performed*"

        logger.info(
            "generation_requested",
            unit_id=unit_id,
            prompt_length=len(prompt),
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Generate response
        result = self.inference_engine.generate(
            unit_id=unit_id,
            prompt=prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=self.config.generation.top_p,
        )

        self._current_result = result

        # Record for feedback
        if self.feedback_collector and self._current_session_id:
            activations_dict = [
                {
                    "expert_id": a.expert_id,
                    "task_id": a.task_id,
                    "model_id": a.model_id,
                    "activation_score": a.activation_score,
                }
                for a in result.activations
            ]
            self._current_feedback_id = self.feedback_collector.record_interaction(
                session_id=self._current_session_id,
                unit_id=unit_id,
                prompt=prompt,
                response=result.response,
                activated_experts=activations_dict,
                generation_params={
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": self.config.generation.top_p,
                },
            )

        # Format response
        response_md = f"## Response\n\n{result.response}"

        if hasattr(result, "tokens_generated") and result.tokens_generated > 0:
            response_md += f"\n\n---\n*Tokens generated: {result.tokens_generated}*"
            if hasattr(result, "generation_time_ms") and result.generation_time_ms > 0:
                response_md += f" | *Time: {result.generation_time_ms:.0f}ms*"

        # Format expert activations
        activations_md = format_expert_activations(result.activations)

        return response_md, activations_md

    def submit_thumbs_up(self) -> str:
        """Handle thumbs up feedback."""
        if not self.feedback_collector or not self._current_feedback_id:
            return "No active generation to provide feedback on."

        self.feedback_collector.submit_feedback(
            feedback_id=self._current_feedback_id,
            thumbs_up=True,
        )
        self._current_feedback_id = None
        return "Thank you for your positive feedback!"

    def submit_thumbs_down(self) -> str:
        """Handle thumbs down feedback."""
        if not self.feedback_collector or not self._current_feedback_id:
            return "No active generation to provide feedback on."

        self.feedback_collector.submit_feedback(
            feedback_id=self._current_feedback_id,
            thumbs_up=False,
        )
        self._current_feedback_id = None
        return "Thank you for your feedback. We'll work on improving!"

    def submit_detailed_feedback(self, rating: float, comment: str) -> str:
        """Handle detailed feedback submission."""
        if not self.feedback_collector or not self._current_feedback_id:
            return "No active generation to provide feedback on."

        self.feedback_collector.submit_feedback(
            feedback_id=self._current_feedback_id,
            rating=int(rating),
            comment=comment,
        )
        self._current_feedback_id = None
        return "Thank you for your detailed feedback!"

    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface.

        Returns:
            Gradio Blocks interface.
        """
        # Get available units
        available_units = self.inference_engine.get_available_units()

        # Unit display names
        unit_display_names = {
            "fundraising": "Fundraising",
            "business_development": "Business Development",
            "field_operations": "Field Operations",
        }

        unit_choices = [
            (unit_display_names.get(u, u), u) for u in available_units
        ]

        with gr.Blocks(
            title=self.config.gradio.title,
        ) as app:
            gr.Markdown(f"# {self.config.gradio.title}")
            gr.Markdown(self.config.gradio.description)

            if self.test_mode:
                gr.Markdown("**[TEST MODE]** Using mock responses - no GPU required.")

            with gr.Row():
                with gr.Column(scale=3):
                    unit_dropdown = gr.Dropdown(
                        choices=unit_choices,
                        label="Select Unit",
                        value=available_units[0] if available_units else None,
                        interactive=True,
                    )

                    prompt_input = gr.Textbox(
                        label="Prompt",
                        placeholder="Enter your prompt here...\n\nExamples:\n- Analyze investor profile for Gates Foundation\n- Summarize RFP requirements for health systems project\n- Assess project performance for Kenya initiative",
                        lines=5,
                    )

                with gr.Column(scale=1):
                    max_tokens_slider = gr.Slider(
                        minimum=50,
                        maximum=512,
                        value=self.config.generation.max_new_tokens,
                        step=10,
                        label="Max Tokens",
                    )

                    temperature_slider = gr.Slider(
                        minimum=0.1,
                        maximum=1.5,
                        value=self.config.generation.temperature,
                        step=0.1,
                        label="Temperature",
                    )

            generate_btn = gr.Button("Generate", variant="primary", size="lg")

            with gr.Row():
                with gr.Column(scale=2):
                    response_output = gr.Markdown(
                        label="Response",
                        value="Select a unit and enter a prompt to generate a response.",
                    )

                with gr.Column(scale=1):
                    activations_output = gr.Markdown(
                        label="Expert Activations",
                        value="*Expert activation data will appear here after generation*",
                    )

            # Feedback UI
            feedback_status = None
            if self.feedback_collector and self.config.feedback.enabled:
                with gr.Group():
                    gr.Markdown("### Was this response helpful?")
                    with gr.Row():
                        thumbs_up_btn = gr.Button(
                            "Helpful", variant="secondary", size="sm"
                        )
                        thumbs_down_btn = gr.Button(
                            "Not Helpful", variant="secondary", size="sm"
                        )

                    with gr.Accordion("Optional: Detailed Feedback", open=False):
                        rating_slider = gr.Slider(
                            minimum=1,
                            maximum=5,
                            value=3,
                            step=1,
                            label="Rating (1-5)",
                        )
                        feedback_text = gr.Textbox(
                            label="Comments",
                            placeholder="What could we improve? Was the response accurate?",
                            lines=2,
                        )
                        submit_feedback_btn = gr.Button(
                            "Submit Detailed Feedback", variant="primary"
                        )

                    feedback_status = gr.Markdown("")

                    # Connect feedback handlers
                    thumbs_up_btn.click(
                        fn=self.submit_thumbs_up,
                        outputs=feedback_status,
                    )
                    thumbs_down_btn.click(
                        fn=self.submit_thumbs_down,
                        outputs=feedback_status,
                    )
                    submit_feedback_btn.click(
                        fn=self.submit_detailed_feedback,
                        inputs=[rating_slider, feedback_text],
                        outputs=feedback_status,
                    )

            # Connect generation handler
            generate_btn.click(
                fn=self.generate_response,
                inputs=[unit_dropdown, prompt_input, max_tokens_slider, temperature_slider],
                outputs=[response_output, activations_output],
            )

            # Also generate on Ctrl+Enter
            prompt_input.submit(
                fn=self.generate_response,
                inputs=[unit_dropdown, prompt_input, max_tokens_slider, temperature_slider],
                outputs=[response_output, activations_output],
            )

            gr.Markdown(
                """
                ---
                **About:** This interface allows staff to interact with organizational
                unit MoE (Mixture of Experts) models. Each unit has specialized experts
                trained for specific tasks. The expert activation display shows which
                experts were consulted to generate the response.
                """
            )

        self._app = app
        return app

    def launch(
        self,
        host: str | None = None,
        port: int | None = None,
        share: bool | None = None,
    ) -> None:
        """
        Launch the Gradio app.

        Args:
            host: Server host (uses config default if None).
            port: Server port (uses config default if None).
            share: Whether to create public link (uses config default if None).
        """
        if self._app is None:
            self.create_interface()

        self._app.launch(
            server_name=host or self.config.gradio.host,
            server_port=port or self.config.gradio.port,
            share=share if share is not None else self.config.gradio.share,
        )


def create_moe_interface_app(
    settings: Settings,
    test_mode: bool = False,
) -> MoEInterfaceApp:
    """
    Create an MoE interface app from settings.

    Args:
        settings: Application settings.
        test_mode: If True, use mock inference engine.

    Returns:
        Configured MoEInterfaceApp instance.
    """
    base_path = Path(__file__).parent.parent.parent

    # Determine exports directory
    if test_mode:
        exports_dir = base_path / settings.paths.exports_dir / "phase4_test"
    else:
        exports_dir = base_path / settings.paths.exports_dir / "phase4"

    # Initialize inference engine
    if test_mode:
        inference_engine = MockMoEInference(
            exports_dir=exports_dir,
            experts_per_token=settings.moe.experts_per_token,
        )
    else:
        if not MODEL_LOADER_AVAILABLE:
            raise RuntimeError(
                "Production mode requires PyTorch. Install with: pip install torch transformers\n"
                "Or use --test-mode for testing without GPU dependencies."
            )
        inference_engine = MoEModelLoader(
            exports_dir=exports_dir,
            device="auto",
        )

    # Initialize feedback collector if enabled
    feedback_collector = None
    if settings.interface.feedback.enabled:
        feedback_dir = base_path / settings.interface.feedback.feedback_dir
        feedback_collector = InterfaceFeedbackCollector(
            feedback_dir=feedback_dir,
            test_mode=test_mode,
        )

    return MoEInterfaceApp(
        inference_engine=inference_engine,
        config=settings.interface,
        feedback_collector=feedback_collector,
        test_mode=test_mode,
    )
