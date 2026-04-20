"""Echo plugin HTTP routes — GET /api/echo/status, POST /api/echo/echo."""

from __future__ import annotations

from fastapi import APIRouter, Request
from pydantic import BaseModel

from agentforge_echo import __version__
from agentforge_echo.events import EchoEvent

router = APIRouter(prefix="/api/echo", tags=["echo"])


class EchoRequest(BaseModel):
    msg: str


class EchoResponse(BaseModel):
    echoed: str
    reversed: str


@router.get("/status")
async def status() -> dict[str, str]:
    return {"status": "ok", "plugin": "echo", "version": __version__}


@router.post("/echo", response_model=EchoResponse)
async def echo(body: EchoRequest, request: Request) -> EchoResponse:
    reversed_msg = body.msg[::-1]

    bus = getattr(request.app.state, "topic_bus", None)
    if bus is not None:
        event = EchoEvent(msg=body.msg, reversed_msg=reversed_msg)
        await bus.emit("project.echo", "echoed", event.model_dump())

    return EchoResponse(echoed=body.msg, reversed=reversed_msg)
