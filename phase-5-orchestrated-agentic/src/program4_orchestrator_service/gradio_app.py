"""
Gradio Interface for Phase 5 Orchestrator.

Provides a web interface for testing orchestrator routing and
agent coordination without requiring the full service stack.
"""

from typing import Optional, Tuple, Union
import httpx
import structlog

import gradio as gr

from config.settings import GradioConfig
from ..shared.routing_schema import (
    RoutingDecision,
    OrchestratedResponse,
    AgentResponse,
    AgentType,
)
from .mock_orchestrator import MockOrchestratorClient

logger = structlog.get_logger()


class OrchestratorHttpClient:
    """
    HTTP client for connecting to running orchestrator service.
    """

    def __init__(self, base_url: str, timeout_ms: int = 10000):
        """
        Initialize HTTP client.

        Args:
            base_url: Base URL of orchestrator service
            timeout_ms: Request timeout in milliseconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout_ms = timeout_ms
        self.logger = logger.bind(component="orchestrator_http_client")

    def route(self, query: str) -> RoutingDecision:
        """
        Get routing decision from orchestrator service.

        Args:
            query: User query

        Returns:
            RoutingDecision from service
        """
        with httpx.Client(timeout=self.timeout_ms / 1000) as client:
            response = client.post(
                f"{self.base_url}/route",
                json={"query": query},
            )
            response.raise_for_status()
            data = response.json()
            return RoutingDecision(**data["routing_decision"])

    def orchestrate(self, query: str) -> OrchestratedResponse:
        """
        Get full orchestration from service.

        Args:
            query: User query

        Returns:
            OrchestratedResponse from service
        """
        with httpx.Client(timeout=self.timeout_ms / 1000) as client:
            response = client.post(
                f"{self.base_url}/orchestrate",
                json={"query": query, "execute": True},
            )
            response.raise_for_status()
            data = response.json()
            return OrchestratedResponse(**data["orchestrated_response"])

    def get_stats(self) -> dict:
        """Get orchestrator statistics."""
        with httpx.Client(timeout=self.timeout_ms / 1000) as client:
            response = client.get(f"{self.base_url}/stats")
            response.raise_for_status()
            return response.json()

    def health_check(self) -> bool:
        """Check if orchestrator service is healthy."""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception:
            return False


def format_routing_decision(routing: RoutingDecision) -> str:
    """Format routing decision as markdown."""
    agent_display = routing.entry_agent.replace("-", " ").title()

    output = "### Routing Decision\n\n"
    output += f"**Entry Agent:** {agent_display}\n\n"
    output += f"**Optimal Depth:** {routing.optimal_depth}\n\n"
    output += f"**Workflow:** {routing.workflow.replace('_', ' ').title()}\n\n"
    output += f"**Reasoning:** {routing.reasoning}\n\n"

    if routing.agent_calls:
        output += "**Agent Call Sequence:**\n"
        for call in routing.agent_calls:
            agent_name = call.agent.replace("-", " ").title()
            output += f"- Step {call.step}: {agent_name} → {call.operation}\n"

    output += f"\n*Estimated latency: {routing.estimated_latency_ms}ms | "
    output += f"Success probability: {routing.success_probability:.0%}*"

    return output


def format_agent_responses(responses: list[AgentResponse]) -> dict[str, str]:
    """Format agent responses for tabbed display."""
    formatted = {}

    for resp in responses:
        agent_name = resp.agent.replace("-", " ").title()
        status = "✓" if resp.success else "✗"

        content = f"### {agent_name}\n\n"
        content += resp.response
        content += f"\n\n---\n"
        content += f"*Latency: {resp.latency_ms}ms | Status: {status}*"

        if resp.cascaded_calls:
            content += f"\n*Cascaded to: {', '.join(resp.cascaded_calls)}*"

        formatted[agent_name] = content

    return formatted


def format_performance_metrics(response: OrchestratedResponse) -> str:
    """Format performance metrics as markdown."""
    status = "✓ Success" if response.success else "✗ Failed"
    agents_called = len(response.agent_responses)
    successful = sum(1 for r in response.agent_responses if r.success)

    output = "### Performance Metrics\n\n"
    output += f"| Metric | Value |\n"
    output += f"|--------|-------|\n"
    output += f"| Total Latency | {response.total_latency_ms}ms |\n"
    output += f"| Agents Called | {agents_called} |\n"
    output += f"| Successful Calls | {successful}/{agents_called} |\n"
    output += f"| Overall Status | {status} |\n"

    return output


class OrchestratorInterfaceApp:
    """
    Gradio-based orchestrator interface application.

    Provides:
    - Query input for orchestration requests
    - Routing decision display
    - Agent response tabs
    - Synthesized response output
    - Performance metrics
    """

    def __init__(
        self,
        client: Union[MockOrchestratorClient, OrchestratorHttpClient],
        config: GradioConfig,
        test_mode: bool = False,
    ):
        """
        Initialize the interface app.

        Args:
            client: Orchestrator client (mock or HTTP)
            config: Gradio configuration
            test_mode: Whether running in test mode
        """
        self.client = client
        self.config = config
        self.test_mode = test_mode
        self._app: Optional[gr.Blocks] = None

        logger.info(
            "orchestrator_interface_initialized",
            test_mode=test_mode,
            client_type=type(client).__name__,
        )

    def route_query(self, query: str) -> Tuple[str, str]:
        """
        Get routing decision only (no agent execution).

        Args:
            query: User query

        Returns:
            Tuple of (routing_markdown, stats_markdown)
        """
        if not query.strip():
            return "Please enter a query.", ""

        try:
            routing = self.client.route(query)
            routing_md = format_routing_decision(routing)

            stats = self.client.get_stats()
            stats_md = f"*Total routes: {stats.get('total_routes', 0)}*"

            return routing_md, stats_md

        except Exception as e:
            logger.error("route_query_failed", error=str(e))
            return f"**Error:** {str(e)}", ""

    def orchestrate_query(
        self, query: str
    ) -> Tuple[str, str, str, str, str, str]:
        """
        Execute full orchestration.

        Args:
            query: User query

        Returns:
            Tuple of (routing_md, fundraising_md, bizdev_md, fieldops_md, response_md, perf_md)
        """
        if not query.strip():
            empty = "Please enter a query."
            return empty, "", "", "", "", ""

        try:
            response = self.client.orchestrate(query)

            # Format routing decision
            routing_md = format_routing_decision(response.routing_decision)

            # Format agent responses by type
            agent_tabs = {
                "Fundraising": "",
                "Business Development": "",
                "Field Operations": "",
            }

            for agent_resp in response.agent_responses:
                agent_name = agent_resp.agent.replace("-", " ").title()
                status = "✓" if agent_resp.success else "✗"

                content = f"{agent_resp.response}\n\n"
                content += f"---\n*Latency: {agent_resp.latency_ms}ms | Status: {status}*"
                if agent_resp.cascaded_calls:
                    content += f"\n*Cascaded to: {', '.join(agent_resp.cascaded_calls)}*"

                if "Fundraising" in agent_name:
                    agent_tabs["Fundraising"] = content
                elif "Business" in agent_name:
                    agent_tabs["Business Development"] = content
                elif "Field" in agent_name:
                    agent_tabs["Field Operations"] = content

            # Format synthesized response
            response_md = f"## Final Response\n\n{response.synthesized_response}"

            # Format performance metrics
            perf_md = format_performance_metrics(response)

            return (
                routing_md,
                agent_tabs["Fundraising"] or "*Agent not called*",
                agent_tabs["Business Development"] or "*Agent not called*",
                agent_tabs["Field Operations"] or "*Agent not called*",
                response_md,
                perf_md,
            )

        except Exception as e:
            logger.error("orchestrate_query_failed", error=str(e))
            error_msg = f"**Error:** {str(e)}"
            return error_msg, "", "", "", "", ""

    def get_stats(self) -> str:
        """Get orchestrator statistics as markdown."""
        try:
            stats = self.client.get_stats()

            output = "### Orchestrator Statistics\n\n"
            output += f"**Mode:** {stats.get('mode', 'unknown')}\n\n"

            if "total_routes" in stats:
                output += f"**Total Routes:** {stats['total_routes']}\n\n"

            if "total_orchestrations" in stats:
                output += f"**Total Orchestrations:** {stats['total_orchestrations']}\n\n"

            if "routes_by_agent" in stats:
                output += "**Routes by Agent:**\n"
                for agent, count in stats["routes_by_agent"].items():
                    agent_name = agent.replace("-", " ").title()
                    output += f"- {agent_name}: {count}\n"

            if "routing" in stats:
                routing = stats["routing"]
                output += f"\n**Routing Stats:**\n"
                output += f"- Success rate: {routing.get('successful_routes', 0)}/{routing.get('total_requests', 0)}\n"
                output += f"- Avg latency: {routing.get('avg_latency_ms', 0):.0f}ms\n"

            return output

        except Exception as e:
            return f"**Error fetching stats:** {str(e)}"

    def create_interface(self) -> gr.Blocks:
        """
        Create the Gradio interface.

        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(title=self.config.title) as app:
            gr.Markdown(f"# {self.config.title}")
            gr.Markdown(self.config.description)

            if self.test_mode:
                gr.Markdown(
                    "**[TEST MODE]** Using mock responses - no service required."
                )

            # Input section
            with gr.Row():
                with gr.Column(scale=3):
                    query_input = gr.Textbox(
                        label="Query",
                        placeholder="Enter your query...\n\nExamples:\n- Analyze investor Gates Foundation capacity\n- Review RFP for Kenya health project\n- Assess regional operations in East Africa",
                        lines=4,
                    )

                with gr.Column(scale=1):
                    gr.Markdown("### Options")
                    mode_info = gr.Markdown(
                        f"*Mode: {'Test' if self.test_mode else 'Production'}*"
                    )

            # Action buttons
            with gr.Row():
                route_btn = gr.Button("Route Only", variant="secondary")
                orchestrate_btn = gr.Button(
                    "Full Orchestration", variant="primary", size="lg"
                )
                stats_btn = gr.Button("View Stats", variant="secondary")

            # Routing Decision section
            gr.Markdown("---")
            routing_output = gr.Markdown(
                value="*Submit a query to see routing decision*",
                label="Routing Decision",
            )

            # Agent Responses section
            gr.Markdown("---")
            gr.Markdown("### Agent Responses")
            with gr.Tabs():
                with gr.TabItem("Fundraising"):
                    fundraising_output = gr.Markdown(
                        value="*Agent response will appear here*"
                    )
                with gr.TabItem("Business Development"):
                    bizdev_output = gr.Markdown(
                        value="*Agent response will appear here*"
                    )
                with gr.TabItem("Field Operations"):
                    fieldops_output = gr.Markdown(
                        value="*Agent response will appear here*"
                    )

            # Synthesized Response section
            gr.Markdown("---")
            response_output = gr.Markdown(
                value="*Synthesized response will appear here*",
                label="Synthesized Response",
            )

            # Performance Metrics section
            gr.Markdown("---")
            perf_output = gr.Markdown(
                value="*Performance metrics will appear here*",
                label="Performance",
            )

            # Stats modal (shown when stats button clicked)
            stats_output = gr.Markdown(visible=False)

            # Connect handlers
            route_btn.click(
                fn=self.route_query,
                inputs=[query_input],
                outputs=[routing_output, stats_output],
            )

            orchestrate_btn.click(
                fn=self.orchestrate_query,
                inputs=[query_input],
                outputs=[
                    routing_output,
                    fundraising_output,
                    bizdev_output,
                    fieldops_output,
                    response_output,
                    perf_output,
                ],
            )

            # Enter key triggers orchestration
            query_input.submit(
                fn=self.orchestrate_query,
                inputs=[query_input],
                outputs=[
                    routing_output,
                    fundraising_output,
                    bizdev_output,
                    fieldops_output,
                    response_output,
                    perf_output,
                ],
            )

            stats_btn.click(
                fn=lambda: (self.get_stats(), gr.update(visible=True)),
                outputs=[stats_output, stats_output],
            )

            gr.Markdown(
                """
                ---
                **About:** This interface allows testing of the Phase 5 Orchestrator,
                which routes queries to specialized agents (Fundraising, Business Development,
                Field Operations) and synthesizes their responses. The orchestrator uses
                a fine-tuned SLM to make routing decisions based on query analysis.
                """
            )

        self._app = app
        return app

    def launch(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        share: Optional[bool] = None,
    ) -> None:
        """
        Launch the Gradio app.

        Args:
            host: Server host (uses config default if None)
            port: Server port (uses config default if None)
            share: Whether to create public link (uses config default if None)
        """
        if self._app is None:
            self.create_interface()

        self._app.launch(
            server_name=host or self.config.host,
            server_port=port or self.config.port,
            share=share if share is not None else self.config.share,
        )


def create_orchestrator_interface(
    test_mode: bool = False,
    service_url: Optional[str] = None,
    config: Optional[GradioConfig] = None,
) -> OrchestratorInterfaceApp:
    """
    Create an orchestrator interface app.

    Args:
        test_mode: If True, use mock client (no service required)
        service_url: URL of orchestrator service (for production mode)
        config: Gradio configuration

    Returns:
        Configured OrchestratorInterfaceApp instance
    """
    if config is None:
        config = GradioConfig()

    if test_mode:
        client = MockOrchestratorClient()
    else:
        if service_url is None:
            service_url = "http://localhost:8000"
        client = OrchestratorHttpClient(service_url)

    return OrchestratorInterfaceApp(
        client=client,
        config=config,
        test_mode=test_mode,
    )
