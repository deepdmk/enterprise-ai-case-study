#!/bin/bash
# Quick Start Script for Phase 4: Agentic Discovery
# Runs the complete pipeline in test mode

set -e  # Exit on error

echo "=========================================="
echo "Phase 4: Agentic Discovery - Quick Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -e .

echo ""
echo "=========================================="
echo "Step 1: A2A Fine-Tuning (Test Mode)"
echo "=========================================="
echo ""

# Fine-tune all three units
for unit in fundraising business_development field_operations; do
    echo "Fine-tuning $unit..."
    python -m src.program1_a2a_finetuning.main \
        --full-pipeline \
        --unit $unit \
        --test-mode \
        --num-examples 100
    echo ""
done

echo ""
echo "=========================================="
echo "Step 2: Starting Agent Services"
echo "=========================================="
echo ""
echo "Starting agent services in background..."
echo "(Services will run on ports 8001-8003)"
echo ""

# Start agent services in background
python -m src.program2_agent_services.main \
    --start fundraising-agent \
    --port 8001 \
    --test-mode &
AGENT1_PID=$!

sleep 2

python -m src.program2_agent_services.main \
    --start business-development-agent \
    --port 8002 \
    --test-mode &
AGENT2_PID=$!

sleep 2

python -m src.program2_agent_services.main \
    --start field-operations-agent \
    --port 8003 \
    --test-mode &
AGENT3_PID=$!

sleep 3

echo "Agent services started (PIDs: $AGENT1_PID, $AGENT2_PID, $AGENT3_PID)"
echo ""

# Test agent health
echo "Testing agent health..."
for port in 8001 8002 8003; do
    if curl -s http://localhost:$port/health > /dev/null; then
        echo "  ✓ Agent on port $port is healthy"
    else
        echo "  ✗ Agent on port $port is not responding"
    fi
done

echo ""
echo "=========================================="
echo "Step 3: Discovery Pipeline (Test Mode)"
echo "=========================================="
echo ""

# Run discovery pipeline
python -m src.program3_discovery_pipeline.main \
    --run \
    --test-mode \
    --queries-per-day 5

echo ""
echo "=========================================="
echo "Step 4: Adaptive Analysis & Phase 5 Export"
echo "=========================================="
echo ""

# Analyze and export
python -m src.program4_adaptive_analyzer.main --full-pipeline

echo ""
echo "=========================================="
echo "Quick Start Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  - A2A adapters: data/models/a2a_adapters/"
echo "  - Discovery logs: data/logs/discovery/"
echo "  - Analysis: data/exports/analysis_results.json"
echo "  - Phase 5 data: data/exports/orchestrator_chat.jsonl"
echo ""
echo "Cleaning up agent services..."
kill $AGENT1_PID $AGENT2_PID $AGENT3_PID 2>/dev/null || true

echo ""
echo "Done! Check the README.md for more detailed usage."
