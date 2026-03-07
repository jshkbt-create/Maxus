"""
Base Tool Interface
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    """Result from a tool execution"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseTool(ABC):
    """Abstract base class for all tools"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description"""
        ...

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool"""
        ...

    async def safe_execute(self, **kwargs) -> ToolResult:
        """Execute with error handling"""
        try:
            return await self.execute(**kwargs)
        except Exception as e:
            logger.error(f"Tool {self.name} error: {e}")
            return ToolResult(success=False, error=str(e))
