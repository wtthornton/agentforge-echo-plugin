"""AgentForge plugin entry point for agentforge-echo-plugin.

`register(app)` is called by `PluginRegistry.register_plugin()`:
1. Mounts the echo router onto the host FastAPI app.
2. Loads the echo-agent into the host's AgentLoader (if present), using an
   absolute path derived from this file's location so load never depends on
   CWD at registration time.
"""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI

logger = logging.getLogger(__name__)

_AGENT_DIR = Path(__file__).parent / "agents" / "echo_agent"
_NAMESPACE = "project.echo"


def register(app: FastAPI) -> None:
    from agentforge_echo.routes import router

    app.include_router(router)

    agent_loader = getattr(app.state, "agent_loader", None)
    if agent_loader is None:
        logger.debug("echo plugin: no agent_loader on app.state — skipping agent load")
        return

    try:
        newly_loaded = agent_loader.load_external(_AGENT_DIR.parent, _NAMESPACE)
        logger.info(
            "echo plugin: loaded %d agent(s) from %s", len(newly_loaded), _AGENT_DIR
        )
    except Exception:
        logger.exception("echo plugin: agent load failed")
