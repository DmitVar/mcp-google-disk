"""Response models for MCP tools."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ToolResponse(BaseModel):
    success: bool
    data: Any | None = None
    error: str | None = None

    @classmethod
    def ok(cls, data: Any | None = None) -> "ToolResponse":
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, error: str) -> "ToolResponse":
        return cls(success=False, data=None, error=error)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()