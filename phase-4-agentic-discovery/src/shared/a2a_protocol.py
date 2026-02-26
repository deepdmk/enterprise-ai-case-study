"""
A2A (Agent-to-Agent) Protocol
Defines core data structures for agent communication and discovery.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MessageType(str, Enum):
    """Types of A2A messages"""
    QUERY = "query"
    RESPONSE = "response"
    ERROR = "error"
    CAPABILITY_DISCOVERY = "capability_discovery"


class ResponseStatus(str, Enum):
    """Status codes for A2A responses"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    NOT_FOUND = "not_found"
    TIMEOUT = "timeout"
    DEPTH_EXCEEDED = "depth_exceeded"
    ERROR = "error"


@dataclass
class A2AMetadata:
    """Metadata for A2A protocol communication"""
    call_id: str
    timestamp: datetime
    call_depth: int
    max_depth: int
    source_agent: str
    target_agent: str
    timeout_ms: int = 5000
    retry_count: int = 0
    trace_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "call_id": self.call_id,
            "timestamp": self.timestamp.isoformat(),
            "call_depth": self.call_depth,
            "max_depth": self.max_depth,
            "source_agent": self.source_agent,
            "target_agent": self.target_agent,
            "timeout_ms": self.timeout_ms,
            "retry_count": self.retry_count,
            "trace_id": self.trace_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2AMetadata":
        """Create from dictionary"""
        required_fields = ["call_id", "timestamp", "call_depth", "max_depth",
                           "source_agent", "target_agent"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"A2AMetadata missing required fields: {missing}")

        data = data.copy()
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


@dataclass
class A2ARequest:
    """
    Request structure for A2A protocol.

    Attributes:
        goal: Natural language description of what the agent needs
        target: Target agent identifier (e.g., "fundraising-agent")
        parameters: Additional structured parameters for the request
        metadata: Protocol metadata (depth, timeouts, etc.)
        message_type: Type of message (default: QUERY)
    """
    goal: str
    target: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Optional[A2AMetadata] = None
    message_type: MessageType = MessageType.QUERY

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "goal": self.goal,
            "target": self.target,
            "parameters": self.parameters,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "message_type": self.message_type.value
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2ARequest":
        """Create from dictionary"""
        required_fields = ["goal", "target"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"A2ARequest missing required fields: {missing}")

        data = data.copy()
        if data.get("metadata"):
            data["metadata"] = A2AMetadata.from_dict(data["metadata"])
        if data.get("message_type"):
            data["message_type"] = MessageType(data["message_type"])
        return cls(**data)


@dataclass
class A2AResponse:
    """
    Response structure for A2A protocol.

    Attributes:
        status: Response status code
        content: The actual response content
        metadata: Protocol metadata from the request
        error_message: Error details if status indicates failure
        cascaded_calls: List of sub-agent calls made to fulfill this request
        execution_time_ms: How long the request took to process
    """
    status: ResponseStatus
    content: Any
    metadata: Optional[A2AMetadata] = None
    error_message: Optional[str] = None
    cascaded_calls: List[str] = field(default_factory=list)
    execution_time_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "status": self.status.value,
            "content": self.content,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "error_message": self.error_message,
            "cascaded_calls": self.cascaded_calls,
            "execution_time_ms": self.execution_time_ms
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2AResponse":
        """Create from dictionary"""
        required_fields = ["status", "content"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"A2AResponse missing required fields: {missing}")

        data = data.copy()
        data["status"] = ResponseStatus(data["status"])
        if data.get("metadata"):
            data["metadata"] = A2AMetadata.from_dict(data["metadata"])
        return cls(**data)


@dataclass
class A2ACapability:
    """
    Describes an agent's capabilities for discovery.

    Attributes:
        agent_id: Unique identifier for the agent
        name: Human-readable name
        description: What this agent can do
        domains: Domain expertise areas
        example_queries: Example queries this agent can handle
        dependencies: Other agents this agent may call
        max_cascade_depth: Maximum depth for cascading calls
    """
    agent_id: str
    name: str
    description: str
    domains: List[str]
    example_queries: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    max_cascade_depth: int = 3

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "domains": self.domains,
            "example_queries": self.example_queries,
            "dependencies": self.dependencies,
            "max_cascade_depth": self.max_cascade_depth
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "A2ACapability":
        """Create from dictionary"""
        required_fields = ["agent_id", "name", "description", "domains"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"A2ACapability missing required fields: {missing}")

        return cls(**data)
