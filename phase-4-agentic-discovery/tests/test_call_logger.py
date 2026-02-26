"""
Tests for A2A Call Logger
"""

import pytest
import json
import threading
import time
from datetime import datetime
from pathlib import Path

from src.shared.a2a_protocol import (
    A2ARequest,
    A2AResponse,
    A2AMetadata,
    ResponseStatus
)
from src.shared.call_logger import A2ACallLog, A2ACallLogger


class TestA2ACallLog:
    """Test A2ACallLog dataclass"""

    def test_create_call_log(self):
        """Test creating a call log"""
        log = A2ACallLog(
            call_id="test-123",
            timestamp=datetime.now(),
            source_agent="agent-a",
            target_agent="agent-b",
            goal="Test goal",
            call_depth=1,
            max_depth=3,
            status=ResponseStatus.SUCCESS,
            execution_time_ms=100.5
        )

        assert log.call_id == "test-123"
        assert log.call_depth == 1
        assert log.status == ResponseStatus.SUCCESS

    def test_call_log_to_dict(self):
        """Test call log serialization"""
        log = A2ACallLog(
            call_id="test-123",
            timestamp=datetime.now(),
            source_agent="agent-a",
            target_agent="agent-b",
            goal="Test goal",
            call_depth=1,
            max_depth=3,
            status=ResponseStatus.SUCCESS,
            execution_time_ms=100.5,
            cascaded_calls=["agent-c"],
            phase=2
        )

        data = log.to_dict()

        assert data["call_id"] == "test-123"
        assert data["status"] == "success"
        assert data["phase"] == 2
        assert "agent-c" in data["cascaded_calls"]

    def test_call_log_from_dict(self):
        """Test call log deserialization"""
        data = {
            "call_id": "test-123",
            "timestamp": datetime.now().isoformat(),
            "source_agent": "agent-a",
            "target_agent": "agent-b",
            "goal": "Test goal",
            "call_depth": 1,
            "max_depth": 3,
            "status": "success",
            "execution_time_ms": 100.5,
            "cascaded_calls": [],
            "error_message": None,
            "phase": 1,
            "workflow_id": None
        }

        log = A2ACallLog.from_dict(data)

        assert log.call_id == "test-123"
        assert log.status == ResponseStatus.SUCCESS

    def test_call_log_from_request_response(self):
        """Test creating log from request/response pair"""
        metadata = A2AMetadata(
            call_id="test-123",
            timestamp=datetime.now(),
            call_depth=1,
            max_depth=3,
            source_agent="agent-a",
            target_agent="agent-b"
        )

        request = A2ARequest(
            goal="Test goal",
            target="agent-b",
            metadata=metadata
        )

        response = A2AResponse(
            status=ResponseStatus.SUCCESS,
            content="Test response",
            metadata=metadata,
            execution_time_ms=50.0
        )

        log = A2ACallLog.from_request_response(
            request=request,
            response=response,
            phase=3
        )

        assert log.call_id == "test-123"
        assert log.goal == "Test goal"
        assert log.phase == 3

    def test_call_log_from_request_without_metadata(self):
        """Test error when request has no metadata"""
        request = A2ARequest(
            goal="Test goal",
            target="agent-b"
        )

        response = A2AResponse(
            status=ResponseStatus.SUCCESS,
            content="Test response"
        )

        with pytest.raises(ValueError, match="metadata"):
            A2ACallLog.from_request_response(request, response)


class TestA2ACallLogger:
    """Test A2ACallLogger"""

    @pytest.fixture
    def logger(self, temp_dir):
        """Create a call logger"""
        return A2ACallLogger(temp_dir)

    @pytest.fixture
    def sample_request(self):
        """Create sample request"""
        return A2ARequest(
            goal="Test goal",
            target="agent-b",
            metadata=A2AMetadata(
                call_id="test-123",
                timestamp=datetime.now(),
                call_depth=1,
                max_depth=3,
                source_agent="agent-a",
                target_agent="agent-b"
            )
        )

    @pytest.fixture
    def sample_response(self, sample_request):
        """Create sample response"""
        return A2AResponse(
            status=ResponseStatus.SUCCESS,
            content="Test response",
            metadata=sample_request.metadata,
            execution_time_ms=50.0
        )

    def test_create_logger(self, temp_dir):
        """Test creating a logger"""
        logger = A2ACallLogger(temp_dir)

        assert logger.log_directory == temp_dir
        assert logger._current_phase == 1

    def test_set_phase(self, logger):
        """Test setting phase"""
        logger.set_phase(3)
        assert logger._current_phase == 3

    def test_log_call(self, logger, sample_request, sample_response, temp_dir):
        """Test logging a call"""
        logger.log_call(sample_request, sample_response)

        log_file = temp_dir / "phase_1.jsonl"
        assert log_file.exists()

        with open(log_file) as f:
            line = f.readline()
            data = json.loads(line)

        assert data["call_id"] == "test-123"
        assert data["goal"] == "Test goal"

    def test_log_call_with_workflow_id(self, logger, sample_request, sample_response, temp_dir):
        """Test logging with workflow ID"""
        logger.log_call(sample_request, sample_response, workflow_id="workflow-456")

        log_file = temp_dir / "phase_1.jsonl"
        with open(log_file) as f:
            data = json.loads(f.readline())

        assert data["workflow_id"] == "workflow-456"

    def test_log_multiple_calls(self, logger, temp_dir):
        """Test logging multiple calls"""
        for i in range(5):
            request = A2ARequest(
                goal=f"Test goal {i}",
                target="agent-b",
                metadata=A2AMetadata(
                    call_id=f"test-{i}",
                    timestamp=datetime.now(),
                    call_depth=1,
                    max_depth=3,
                    source_agent="agent-a",
                    target_agent="agent-b"
                )
            )

            response = A2AResponse(
                status=ResponseStatus.SUCCESS,
                content=f"Response {i}",
                metadata=request.metadata,
                execution_time_ms=float(i * 10)
            )

            logger.log_call(request, response)

        logs = logger.load_logs(phase=1)
        assert len(logs) == 5

    def test_load_logs_specific_phase(self, logger, temp_dir):
        """Test loading logs for specific phase"""
        # Log to different phases
        for phase in [1, 2, 3]:
            logger.set_phase(phase)
            request = A2ARequest(
                goal=f"Phase {phase} goal",
                target="agent-b",
                metadata=A2AMetadata(
                    call_id=f"phase-{phase}-call",
                    timestamp=datetime.now(),
                    call_depth=1,
                    max_depth=3,
                    source_agent="agent-a",
                    target_agent="agent-b"
                )
            )

            response = A2AResponse(
                status=ResponseStatus.SUCCESS,
                content=f"Response",
                metadata=request.metadata,
                execution_time_ms=50.0
            )

            logger.log_call(request, response)

        # Load only phase 2
        logs = logger.load_logs(phase=2)
        assert len(logs) == 1
        assert logs[0].phase == 2

    def test_load_all_logs(self, logger, temp_dir):
        """Test loading all logs across phases"""
        for phase in [1, 2, 3]:
            logger.set_phase(phase)
            request = A2ARequest(
                goal=f"Phase {phase} goal",
                target="agent-b",
                metadata=A2AMetadata(
                    call_id=f"phase-{phase}-call",
                    timestamp=datetime.now(),
                    call_depth=1,
                    max_depth=3,
                    source_agent="agent-a",
                    target_agent="agent-b"
                )
            )

            response = A2AResponse(
                status=ResponseStatus.SUCCESS,
                content=f"Response",
                metadata=request.metadata,
                execution_time_ms=50.0
            )

            logger.log_call(request, response)

        # Load all
        logs = logger.load_logs()
        assert len(logs) == 3

    def test_iter_logs(self, logger, temp_dir):
        """Test streaming logs with iter_logs"""
        # Create many logs
        for i in range(10):
            request = A2ARequest(
                goal=f"Goal {i}",
                target="agent-b",
                metadata=A2AMetadata(
                    call_id=f"call-{i}",
                    timestamp=datetime.now(),
                    call_depth=1,
                    max_depth=3,
                    source_agent="agent-a",
                    target_agent="agent-b"
                )
            )

            response = A2AResponse(
                status=ResponseStatus.SUCCESS,
                content=f"Response",
                metadata=request.metadata,
                execution_time_ms=50.0
            )

            logger.log_call(request, response)

        # Iterate and count
        count = 0
        for log in logger.iter_logs():
            count += 1
            assert isinstance(log, A2ACallLog)

        assert count == 10

    def test_get_phase_stats(self, logger, sample_request, sample_response):
        """Test getting phase statistics"""
        # Log some calls
        logger.log_call(sample_request, sample_response)

        # Create error response
        error_request = A2ARequest(
            goal="Error goal",
            target="agent-b",
            metadata=A2AMetadata(
                call_id="error-call",
                timestamp=datetime.now(),
                call_depth=2,
                max_depth=3,
                source_agent="agent-a",
                target_agent="agent-b"
            )
        )

        error_response = A2AResponse(
            status=ResponseStatus.ERROR,
            content=None,
            metadata=error_request.metadata,
            error_message="Test error",
            execution_time_ms=100.0
        )

        logger.log_call(error_request, error_response)

        stats = logger.get_phase_stats(1)

        assert stats["phase"] == 1
        assert stats["total_calls"] == 2
        assert stats["success_rate"] == 0.5

    def test_get_phase_stats_empty(self, logger):
        """Test stats for empty phase"""
        stats = logger.get_phase_stats(5)

        assert stats["total_calls"] == 0
        assert stats["success_rate"] == 0.0

    def test_export_for_analysis(self, logger, sample_request, sample_response, temp_dir):
        """Test exporting logs for analysis"""
        logger.log_call(sample_request, sample_response)

        output_file = temp_dir / "export.json"
        logger.export_for_analysis(output_file)

        assert output_file.exists()

        with open(output_file) as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["call_id"] == "test-123"

    def test_concurrent_writes(self, temp_dir):
        """Test concurrent writes to logger (file locking)"""
        logger = A2ACallLogger(temp_dir)
        errors = []

        def write_logs(thread_id):
            try:
                for i in range(10):
                    request = A2ARequest(
                        goal=f"Thread {thread_id} goal {i}",
                        target="agent-b",
                        metadata=A2AMetadata(
                            call_id=f"thread-{thread_id}-call-{i}",
                            timestamp=datetime.now(),
                            call_depth=1,
                            max_depth=3,
                            source_agent="agent-a",
                            target_agent="agent-b"
                        )
                    )

                    response = A2AResponse(
                        status=ResponseStatus.SUCCESS,
                        content=f"Response",
                        metadata=request.metadata,
                        execution_time_ms=50.0
                    )

                    logger.log_call(request, response)
            except Exception as e:
                errors.append(e)

        # Start multiple threads
        threads = []
        for t_id in range(5):
            t = threading.Thread(target=write_logs, args=(t_id,))
            threads.append(t)
            t.start()

        # Wait for all threads
        for t in threads:
            t.join()

        # Check no errors
        assert len(errors) == 0

        # Verify all logs were written
        logs = logger.load_logs()
        assert len(logs) == 50  # 5 threads * 10 logs each

    def test_log_file_path(self, logger, temp_dir):
        """Test log file path generation"""
        path = logger._get_log_file(3)

        assert path == temp_dir / "phase_3.jsonl"

    def test_status_breakdown(self, logger):
        """Test status breakdown calculation"""
        logs = [
            A2ACallLog(
                call_id="1",
                timestamp=datetime.now(),
                source_agent="a",
                target_agent="b",
                goal="g",
                call_depth=1,
                max_depth=3,
                status=ResponseStatus.SUCCESS,
                execution_time_ms=50.0
            ),
            A2ACallLog(
                call_id="2",
                timestamp=datetime.now(),
                source_agent="a",
                target_agent="b",
                goal="g",
                call_depth=1,
                max_depth=3,
                status=ResponseStatus.SUCCESS,
                execution_time_ms=50.0
            ),
            A2ACallLog(
                call_id="3",
                timestamp=datetime.now(),
                source_agent="a",
                target_agent="b",
                goal="g",
                call_depth=1,
                max_depth=3,
                status=ResponseStatus.ERROR,
                execution_time_ms=50.0
            ),
        ]

        breakdown = logger._get_status_breakdown(logs)

        assert breakdown["success"] == 2
        assert breakdown["error"] == 1
