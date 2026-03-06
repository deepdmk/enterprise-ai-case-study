# Agno Framework Integration

## Overview

The Agno integration replaces Phase 5's custom routing engine with the Agno framework's `Team` coordination mode. It wraps the three Phase 4 A2A agents (Fundraising, Business Development, Field Operations) as Agno `RemoteAgent` members in a `Team` with a fine-tuned SLM coordinator. The coordinator — trained on 71,000 examples from the 90-day Phase 4 discovery phase — makes routing decisions that were previously handled by a hardcoded `RoutingEngine`.

The integration maintains full backward compatibility with the legacy API through a `LegacyAdapter` that translates Agno Team output into the existing `OrchestratedResponse` format. Clients see identical request/response contracts regardless of which mode is active.

Key capabilities:
- **Dual-mode operation**: Toggle between legacy (`use_agno=False`) and Agno (`use_agno=True`) at startup
- **Learned routing**: Coordinator SLM replaces rule-based routing with patterns learned from discovery data
- **A2A protocol support**: Phase 4 agents are accessed via `RemoteAgent(protocol="a2a")` over REST
- **Training data capture**: All orchestrations are logged in JSONL for continuous fine-tuning
- **Optional AG-UI streaming**: Real-time agent activity visualization via CopilotKit-compatible interface

## Architecture

### Data Flow

```
User Query
    │
    ▼
POST /orchestrate
    │
    ├── use_agno=True ──────────────────────────┐
    │                                           │
    │   LegacyAdapter.orchestrate()             │
    │       │                                   │
    │       ▼                                   │
    │   Team.arun(query)                        │
    │       │                                   │
    │       ▼                                   │
    │   Coordinator SLM (fine-tuned)             │
    │   Analyzes query, selects agent(s)        │
    │       │                                   │
    │       ├── RemoteAgent: fundraising-agent   │  Port 8001
    │       ├── RemoteAgent: business-dev-agent  │  Port 8002
    │       └── RemoteAgent: field-ops-agent     │  Port 8003
    │       │                                   │
    │       ▼                                   │
    │   Team result (content + messages)        │
    │       │                                   │
    │       ▼                                   │
    │   LegacyAdapter extracts:                 │
    │   - RoutingDecision (entry_agent, depth)  │
    │   - AgentResponse[] (per-agent results)   │
    │   - Synthesized response (combined text)  │
    │       │                                   │
    │       ▼                                   │
    │   TrainingLogger.log_orchestration()       │
    │       │                                   │
    │       ▼                                   │
    │   OrchestratedResponse                    │
    │                                           │
    ├── use_agno=False ─────────────────────────┐
    │                                           │
    │   RoutingEngine.route(query)              │
    │       │                                   │
    │       ▼                                   │
    │   AgentClient.call_multiple_agents()      │
    │       │                                   │
    │       ▼                                   │
    │   ResponseSynthesizer.synthesize()        │
    │       │                                   │
    │       ▼                                   │
    │   OrchestratedResponse                    │
    │                                           │
    ▼                                           │
Response to Client ◄────────────────────────────┘
```

### Dual-Mode Switching

The mode is determined at app creation time in `service.py:create_app()`. When `use_agno=True`:

1. `create_orchestrator_team()` builds the Agno `Team` with coordinator model + remote members
2. `LegacyAdapter(team)` wraps the team for API compatibility
3. `TrainingLogger` begins capturing orchestration data
4. Optionally, `create_agui_interface()` mounts AG-UI streaming routes

When `use_agno=False`, the legacy pipeline (`RoutingEngine` → `AgentClient` → `ResponseSynthesizer`) is used instead. Both paths produce the same `OrchestratedResponse` output format.

## Components

### Model Provider (`model_provider.py`)

Provides `create_vllm_model()` which creates a model instance pointing to the fine-tuned orchestrator SLM inference server.

**Two model backends:**

| Backend | Class | URL Format | Use Case |
|---------|-------|-----------|----------|
| Standard vLLM | `agno.models.vllm.VLLM` | `http://host:port/` | Direct vLLM server |
| OpenAI-compatible | `agno.models.openai.like.OpenAILike` | `http://host:port/v1` | vLLM with `--api-key` flag |

**URL normalization:**
- Standard mode: Ensures trailing `/` (e.g., `http://localhost:8100/generate/`)
- OpenAI-compatible mode: Ensures `/v1` suffix (e.g., `http://localhost:8100/v1`)

**Parameters passed through `**kwargs`:**
- `max_tokens`: Maximum generation tokens (default: 512)
- `temperature`: Sampling temperature (default: 0.1)

```python
model = create_vllm_model(
    inference_url="http://localhost:8100/generate",
    model_id="phase5-orchestrator",
    use_openai_compatible=False,
    max_tokens=512,
    temperature=0.1
)
```

### Remote Agent Members (`members.py`)

Factory functions that wrap each Phase 4 A2A agent as an Agno `RemoteAgent`. Each agent runs as an independent FastAPI service serving the A2A protocol.

**Three members:**

| Member | Factory Function | Default URL | MoE Experts | Expert Capabilities |
|--------|-----------------|-------------|-------------|---------------------|
| Fundraising | `create_fundraising_member()` | `http://localhost:8001` | 5 | Investor profiling, portfolio analysis, funding capacity, interest matching, historical giving |
| Business Development | `create_business_dev_member()` | `http://localhost:8002` | 4 | RFP tracking, competitive landscape, funding opportunities, market positioning |
| Field Operations | `create_field_ops_member()` | `http://localhost:8003` | 5 | Regional capacity, local intelligence, project performance, partner relationships, logistics |

**RemoteAgent configuration:**
```python
RemoteAgent(
    base_url=base_url,
    agent_id="fundraising-agent",
    protocol="a2a",
    a2a_protocol="rest"  # Phase 4 agents use REST-based A2A
)
```

The `create_all_members()` function dynamically creates members from the agent registry dictionary, only instantiating agents that are registered. This allows partial deployment (e.g., running with only 2 of 3 agents available).

### Coordinator (`coordinator.py`)

Defines the system prompt, instructions, and description for the coordinator — the fine-tuned SLM that makes routing decisions within the Agno Team.

**Three exported functions:**

1. **`create_coordinator_instructions()`** — Returns a list of instruction strings covering:
   - Core responsibilities (analyze, delegate, synthesize)
   - Agent capabilities (what each member can do)
   - Routing strategy (keyword-based agent selection rules learned from discovery)
   - Cascade depth optimization (depth 1-4 guidelines)
   - Response synthesis rules (combine, highlight, resolve conflicts)
   - Error handling (fallback strategies, partial answers)

2. **`create_coordinator_system_prompt()`** — Full system prompt sent to the SLM, including:
   - Role definition as AI orchestrator
   - Available agents and their capabilities
   - Routing strategy learned from 90 days of discovery data
   - Cascade depth optimization guidelines (depth 1 = simple lookups, depth 2 = standard, depth 3+ = complex)
   - Expected output format (agent selection, depth, rationale)
   - Reference to 71,000 training examples informing decisions

3. **`create_coordinator_description()`** — Short description string used as the Team's description field.

**Routing rules (from Phase 4 discovery):**
- Investor/funder queries → Fundraising Agent
- RFP/competitive/market queries → Business Development Agent
- Regional/country/local queries → Field Operations Agent
- Complex multi-faceted queries → Multiple agents (sequential or parallel)

**Cascade depth guidelines (from adaptive depth testing):**
- Depth 1: Simple lookup queries, no cascading needed
- Depth 2: Queries requiring context from one related domain (standard workflow)
- Depth 3+: Complex cross-functional queries requiring multiple cascades (use sparingly)
- Depth 4: Maximum depth, reserved for the most complex multi-agent coordination

### Team (`team.py`)

Central orchestration assembly point. `create_orchestrator_team()` combines the model, members, and instructions into an Agno `Team`.

**Team configuration:**
```python
Team(
    name="Phase5Orchestrator",
    mode=TeamMode.route,
    model=model,              # Fine-tuned SLM via VLLM/OpenAILike
    members=members,          # List of RemoteAgent instances
    description=description,  # From coordinator.create_coordinator_description()
    instructions=instructions,# From coordinator.create_coordinator_instructions()
    show_members_responses=True,
    markdown=True
)
```

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `inference_server_url` | required | URL of vLLM/TGI inference server |
| `agent_registry` | required | Dict mapping agent names to URLs |
| `show_members_responses` | `True` | Include member responses in team output |
| `respond_directly` | `True` | Members respond directly vs coordinator synthesizing |
| `model_timeout` | `30.0` | Inference timeout in seconds |
| `model_max_tokens` | `512` | Maximum tokens for coordinator generation |
| `model_temperature` | `0.1` | Sampling temperature (low = deterministic routing) |
| `test_mode` | `False` | Use mock model (no real inference server needed) |
| `use_openai_compatible` | `False` | Use OpenAI-compatible endpoint format |

**Test mode:** When `test_mode=True`, `create_mock_model()` returns a `VLLM` instance pointing to `http://localhost:9999/mock/`. The test environment is expected to mock the HTTP calls.

**`run_orchestration()`** — Async helper for running team orchestration:
- Non-streaming: `team.arun(query)` returns result with `.content`, `.messages`, `.metrics`
- Streaming: `team.arun_stream(query)` returns an async generator for real-time output

### Legacy Adapter (`legacy_adapter.py`)

Bridges the gap between Agno's `Team` API and the existing Phase 5 API contracts. This is the critical compatibility layer that allows the Agno integration to be a drop-in replacement.

**`LegacyAdapter` class:**

```python
adapter = LegacyAdapter(team)
response = await adapter.orchestrate(query)  # Returns OrchestratedResponse
decision = await adapter.route(query)         # Returns RoutingDecision
```

**`orchestrate()` method flow:**
1. Calls `team.arun(query)` to run the Agno Team
2. Extracts `RoutingDecision` by parsing coordinator output (`_extract_routing_decision`)
3. Extracts `AgentResponse[]` from team messages (`_extract_agent_responses`)
4. Extracts synthesized response from result content (`_extract_synthesized_response`)
5. Wraps everything in `OrchestratedResponse` with metadata `{"agno_mode": True}`
6. On error, returns a fallback `OrchestratedResponse` with `success=False`

**Routing decision extraction:**
- Entry agent: Detected by keyword matching in coordinator output (`"fundraising"`, `"business development"`, `"field operations"`)
- Optimal depth: Extracted via regex `depth[:\s]+(\d+)`, clamped to range [1, 4]
- Workflow type: Detected from query keywords (e.g., `"regional"` → `EVALUATE_REGIONAL_PROJECT`)
- Default: `AgentType.FIELD_OPERATIONS` with `depth=2` if parsing fails

**Agent response extraction:**
- Scans `result.messages` for entries with `role="assistant"` and agent name in the `name` field
- Maps names to `AgentType` enum values via keyword matching
- Individual latency is not tracked (Agno doesn't expose per-member timing)

**`route()` method:** Runs a full orchestration internally and returns only the `RoutingDecision`. In Agno mode, routing cannot be separated from execution because the coordinator makes decisions during the team run.

**Fallback routing:** On any exception, `_create_fallback_routing()` returns a safe default:
```python
RoutingDecision(
    workflow=WorkflowType.UNKNOWN,
    entry_agent=AgentType.FIELD_OPERATIONS,
    optimal_depth=2,
    agent_calls=[],
    reasoning="Fallback routing due to error",
    success_probability=0.0
)
```

### Training Logger (`training_logger.py`)

Captures all orchestration interactions in JSONL format for continuous fine-tuning of the orchestrator SLM. This enables the system to improve over time by learning from real-world usage patterns.

**`TrainingLogger` class:**

```python
logger = TrainingLogger(
    log_dir="data/training/agno_logs",
    enabled=True
)
```

**Methods:**

| Method | Purpose | Output |
|--------|---------|--------|
| `log_orchestration(response, feedback)` | Log full orchestration with optional user feedback | Appends to JSONL |
| `log_routing_only(query, entry_agent, depth, reasoning)` | Log lightweight routing decision only | Appends to JSONL |
| `export_training_data(output_file, filter_successful)` | Convert logs to ChatML training format | New JSONL file |
| `get_stats()` | Return logging statistics | Dict with counts and rates |

**Log entry structure (full orchestration):**
```json
{
  "timestamp": 1709740800.0,
  "query": "What is USAID's funding capacity?",
  "routing_decision": {
    "entry_agent": "fundraising",
    "optimal_depth": 2,
    "workflow": "assess_investor_capacity",
    "reasoning": "Investor capacity query routes to fundraising agent"
  },
  "agent_responses": [
    {
      "agent": "fundraising",
      "operation": "process_query",
      "success": true,
      "latency_ms": 150,
      "cascaded_calls": []
    }
  ],
  "synthesized_response": "USAID's current funding capacity...",
  "total_latency_ms": 320,
  "success": true,
  "feedback": {},
  "metadata": {"agno_mode": true}
}
```

**Training data export:** `export_training_data()` reads the JSONL log, filters for successful orchestrations (by default), and converts each entry to ChatML format via `TrainingExample.to_chat_format()`. This produces training data compatible with the Phase 5 fine-tuning pipeline.

**Statistics:** `get_stats()` scans the log file and returns:
- `total_logs`: Total orchestration count
- `successful`: Count of successful orchestrations
- `failed`: Count of failed orchestrations
- `success_rate`: Ratio of successful to total
- `log_file`: Path to current log file

### AG-UI Interface (`agui_interface.py`)

Optional real-time streaming interface using Agno's AG-UI protocol. Enables CopilotKit-compatible frontend integration for visualizing agent activity as it happens.

**Three exported functions:**

1. **`create_agui_interface(team, path, name, description, enabled)`**
   - Creates an `AGUI` instance from `agno.interfaces.agui`
   - Default path: `/agui`
   - Default name: "Phase 5 Orchestrator"
   - Returns `None` if disabled, if `agno.interfaces.agui` is not importable, or on any error
   - Requires `agno>=2.4.0` with interfaces support

2. **`mount_agui_routes(app, agui)`**
   - Mounts the AGUI router to the FastAPI application
   - Adds endpoints:
     - `POST /agui/stream` — SSE stream for real-time events
     - `GET /agui/events` — Event stream for tool activity
   - No-op if `agui` is `None`

3. **`create_streaming_response(agui, query)`**
   - Helper for custom streaming endpoints
   - Returns an async generator via `agui.stream_response(query)`
   - Raises `ValueError` if AG-UI is not available

**Graceful degradation:** The AG-UI interface is fully optional. If the `agno.interfaces.agui` module is not available (older Agno version), the integration logs a warning and continues without streaming support. No functionality is lost — only the real-time visualization is unavailable.

## Configuration

The Agno integration is configured under the `orchestrator_service.agno` key in `config/config.yaml`:

```yaml
orchestrator_service:
  # Agent registry (Phase 4 agent URLs)
  agent_registry:
    fundraising-agent: "http://localhost:8001"
    business-development-agent: "http://localhost:8002"
    field-operations-agent: "http://localhost:8003"

  # Inference server connection
  inference_server_url: "http://localhost:8100/generate"

  # Agno Framework Integration (Agno 2.4.1)
  agno:
    enabled: false              # Set to true to use Agno Team mode
    show_members_responses: true # Show member responses in final output
    respond_directly: true       # Members respond directly

    # Model configuration
    model_timeout: 30.0          # Inference timeout in seconds
    model_max_tokens: 512        # Maximum tokens for coordinator
    model_temperature: 0.1       # Sampling temperature
    use_openai_compatible: false  # Use OpenAI-compatible endpoint

    # AG-UI Configuration (optional streaming interface)
    agui:
      enabled: false             # Set to true to enable AG-UI streaming
      path: "/agui"              # AG-UI endpoint path

    # Training logger (capture data for future fine-tuning)
    training_logger:
      enabled: true              # Log orchestration interactions
      log_dir: "data/training/agno_logs"
```

**Configuration keys:**

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `agno.enabled` | bool | `false` | Master switch for Agno mode |
| `agno.show_members_responses` | bool | `true` | Include member responses in team output |
| `agno.model_timeout` | float | `30.0` | Inference server timeout in seconds |
| `agno.model_max_tokens` | int | `512` | Max tokens for coordinator generation |
| `agno.model_temperature` | float | `0.1` | Sampling temperature (low = deterministic) |
| `agno.use_openai_compatible` | bool | `false` | Use OpenAI-compatible endpoint format |
| `agno.agui.enabled` | bool | `false` | Enable AG-UI streaming interface |
| `agno.agui.path` | str | `"/agui"` | URL path for AG-UI endpoints |
| `agno.training_logger.enabled` | bool | `true` | Enable training data capture |
| `agno.training_logger.log_dir` | str | `"data/training/agno_logs"` | Directory for JSONL logs |

## Usage

### Starting the Service

**Legacy mode (default):**
```bash
# Test mode (mock routing, no inference server needed)
python -m src.program4_orchestrator_service.main --start --test-mode

# Production mode (requires inference server + Phase 4 agents)
python -m src.program4_orchestrator_service.main --start
```

**Agno mode:**
```bash
# Test mode (mock model, no inference server needed)
python -m src.program4_orchestrator_service.main --start --use-agno --test-mode

# Production mode (requires inference server + Phase 4 agents)
python -m src.program4_orchestrator_service.main --start --use-agno
```

### API Endpoints

All endpoints work identically in both modes:

```bash
# Health check
curl http://localhost:8000/health

# Routing decision only
curl -X POST http://localhost:8000/route \
  -H "Content-Type: application/json" \
  -d '{"query": "What is USAID funding capacity for East Africa?"}'

# Full orchestration (routing + agent execution + synthesis)
curl -X POST http://localhost:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"query": "What is USAID funding capacity for East Africa?", "execute": true}'

# Statistics
curl http://localhost:8000/stats
```

**Agno-mode health check response:**
```json
{
  "status": "healthy",
  "mode": "agno",
  "test_mode": false,
  "team_members": 3,
  "agents_available": 3,
  "agents_total": 3,
  "agent_health": {
    "fundraising-agent": true,
    "business-development-agent": true,
    "field-operations-agent": true
  }
}
```

### Gradio UI

```bash
# Launch with Agno mode
python -m src.program4_orchestrator_service.main --ui --use-agno --test-mode
```

## Testing

### Test Files

| Test File | Coverage |
|-----------|----------|
| `tests/test_agno_orchestrator.py` | Core Agno integration: team creation, legacy adapter, model provider, members, coordinator, training logger |
| `tests/test_agno_implementation.py` | File structure validation, documentation existence, module imports, configuration completeness |
| `tests/test_service_endpoints.py` | FastAPI endpoint tests for both legacy and Agno modes |
| `tests/test_all.py` | Full test suite aggregation |

### Running Tests

```bash
cd phase-5-orchestrated-agentic

# Run all Agno tests
python -m pytest tests/test_agno_orchestrator.py -v

# Run implementation validation
python -m pytest tests/test_agno_implementation.py -v

# Run specific test class
python -m pytest tests/test_agno_orchestrator.py::TestLegacyAdapter -v

# Run all tests
python -m pytest tests/ -v
```

## Design Decisions

### Why `TeamMode.route`

The team uses `TeamMode.route` rather than `TeamMode.coordinate` or `TeamMode.collaborate`. In route mode, the coordinator SLM selects which member(s) to delegate to based on the query — this maps directly to the routing decisions the fine-tuned SLM was trained on. The 71,000 training examples from Phase 4 discovery are fundamentally routing decisions (query → agent selection + depth), making `route` the natural fit.

### Why LegacyAdapter Exists

The existing Phase 5 API contract uses `OrchestratedResponse` with fields like `RoutingDecision`, `AgentResponse[]`, and `synthesized_response`. Agno's Team returns a different structure (content + messages). Rather than breaking the API contract and forcing all consumers to update, the `LegacyAdapter` translates between formats. This allows:
- Zero-downtime migration: switch between modes without client changes
- A/B testing: run both modes in parallel to compare routing quality
- Gradual rollout: start with legacy mode, switch to Agno after validation

### Why the Training Logger Captures Data

The orchestrator SLM improves through continuous fine-tuning cycles. Phase 4 provided the initial 71,000 training examples, but real-world usage patterns may differ from the 90-day discovery phase. The training logger captures every orchestration so that:
- New routing patterns can be learned from production traffic
- Routing accuracy can be measured over time
- User feedback (thumbs up/down) can be incorporated into training
- The export-to-ChatML pipeline enables periodic retraining

### Phase 4 A2A Adapter for RemoteAgent Compatibility

Phase 4 agents implement a custom A2A protocol over REST. Agno's `RemoteAgent` supports `protocol="a2a"` with `a2a_protocol="rest"`, which maps to this protocol. The `a2a_adapter.py` module in Phase 4 ensures the FastAPI endpoints conform to the A2A protocol specification that Agno expects, specifically:
- Task submission and status polling endpoints
- Standardized request/response format
- Agent card metadata for discovery

This avoids modifying the Phase 4 agents while making them fully compatible with Agno's remote agent protocol.

### Low Temperature (0.1) for Coordinator

The coordinator uses `temperature=0.1` by default because routing decisions should be deterministic. Given the same query, the coordinator should consistently select the same agent(s) and depth. Higher temperatures would introduce unnecessary randomness in routing, potentially degrading latency and accuracy. The low temperature also aligns with how the model was fine-tuned — the training examples have single correct routing decisions per query.
