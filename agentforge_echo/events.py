"""Typed events emitted by the echo plugin onto AgentForge's TopicBus."""

from __future__ import annotations

from pydantic import BaseModel


class EchoEvent(BaseModel):
    """Emitted on topic `project.echo.echoed` whenever POST /api/echo/echo fires."""

    msg: str
    reversed_msg: str
