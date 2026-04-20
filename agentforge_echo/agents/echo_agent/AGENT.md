---
name: echo-agent
namespace: project.echo.echo-agent
description: Deterministic string-reversal agent. Used as the canonical test fixture for AgentForge's plugin system — no LLM, no network, no flake.
keywords: [echo, reverse, test, smoke]
utterances:
  - reverse this string
  - echo back
  - flip the text
model: sonnet
memory_profile: none
runner: agentforge_echo.agents.echo_agent.runner:EchoRunner
---

# Echo Agent

Deterministic test fixture. Input string → reversed string. That's it.

Exists to exercise `AgentLoader.load_external()`, namespace registration under `project.echo`, and the `GET /api/plugins/echo/agents` surface without pulling in any LLM provider or external service.
