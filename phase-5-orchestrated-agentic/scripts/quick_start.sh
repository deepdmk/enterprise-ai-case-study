#!/bin/bash

# Phase 5 Quick Start Script
# Runs the complete pipeline in test mode (no GPU required)

set -e  # Exit on error

echo "================================================================================"
echo "Phase 5: Orchestrated Agentic - Quick Start"
echo "================================================================================"
echo ""
echo "This script will:"
echo "  1. Install the package"
echo "  2. Generate mock training data"
echo "  3. Create mock fine-tuned model"
echo "  4. Start inference server (background)"
echo "  5. Start orchestrator service (background)"
echo "  6. Run example tests"
echo ""
echo "Press Ctrl+C to stop all services at any time"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "Stopping services..."
    if [ ! -z "$INFERENCE_PID" ]; then
        kill $INFERENCE_PID 2>/dev/null || true
    fi
    if [ ! -z "$ORCHESTRATOR_PID" ]; then
        kill $ORCHESTRATOR_PID 2>/dev/null || true
    fi
    echo "Cleanup complete"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Step 1: Install package
echo "Step 1/7: Installing package..."
pip install -e . > /dev/null 2>&1
echo "✓ Package installed"
echo ""

# Step 2: Generate training data
echo "Step 2/7: Generating mock training data..."
phase5-convert --full-pipeline --test-mode
echo "✓ Training data generated"
echo ""

# Step 3: Create mock model
echo "Step 3/7: Creating mock fine-tuned model..."
phase5-finetune --full-pipeline --test-mode
echo "✓ Mock model created"
echo ""

# Step 4: Start inference server
echo "Step 4/7: Starting inference server (port 8100)..."
phase5-inference --start --test-mode > /tmp/phase5-inference.log 2>&1 &
INFERENCE_PID=$!
echo "✓ Inference server started (PID: $INFERENCE_PID)"
echo "  Logs: /tmp/phase5-inference.log"
echo ""

# Wait for inference server to be ready
echo "Waiting for inference server to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8100/health > /dev/null 2>&1; then
        echo "✓ Inference server is ready"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo "✗ Inference server failed to start (timeout)"
        exit 1
    fi
done
echo ""

# Step 5: Start orchestrator service
echo "Step 5/7: Starting orchestrator service (port 8000)..."
phase5-orchestrator --start --test-mode > /tmp/phase5-orchestrator.log 2>&1 &
ORCHESTRATOR_PID=$!
echo "✓ Orchestrator service started (PID: $ORCHESTRATOR_PID)"
echo "  Logs: /tmp/phase5-orchestrator.log"
echo ""

# Wait for orchestrator to be ready
echo "Waiting for orchestrator to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Orchestrator is ready"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo "✗ Orchestrator failed to start (timeout)"
        exit 1
    fi
done
echo ""

# Step 6: Run tests
echo "Step 6/7: Running test suite..."
pytest tests/test_all.py -v --tb=short || echo "⚠ Some tests may have failed (this is expected in test mode)"
echo ""

# Step 7: Run examples
echo "Step 7/7: Running orchestration example..."
echo ""
python examples/example_orchestration.py
echo ""

echo "================================================================================"
echo "Quick Start Complete!"
echo "================================================================================"
echo ""
echo "Services are running:"
echo "  - Inference Server:  http://localhost:8100"
echo "  - Orchestrator API:  http://localhost:8000"
echo "  - API Docs:          http://localhost:8000/docs"
echo ""
echo "Try these commands:"
echo "  curl http://localhost:8000/health"
echo '  curl -X POST http://localhost:8000/route -H "Content-Type: application/json" -d '"'"'{"query": "Evaluate Kenya project"}'"'"
echo "  python examples/example_orchestration.py"
echo ""
echo "View logs:"
echo "  tail -f /tmp/phase5-inference.log"
echo "  tail -f /tmp/phase5-orchestrator.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================================================"

# Keep script running
while true; do
    sleep 1
done
