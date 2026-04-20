# agentforge-echo-plugin

The canonical **test rig** for AgentForge's plugin system. Filed as [TAP-753](https://linear.app/tappscodingagents/issue/TAP-753).

This plugin does nothing useful in production. Its only job is to exercise every plugin-system hook point — entry-point discovery, `register(app)` callback, route mounting, agent discovery, event bus — **deterministically, with zero external dependencies**. When this plugin's smoke test breaks, the plugin system broke.

## What it proves works

| Hook | How |
|------|-----|
| `[project.entry-points."agentforge.plugins"]` discovery | `pyproject.toml` declares `echo = "agentforge_echo"` |
| `register(app)` entry-point | `agentforge_echo.plugin:register` mounts the router |
| Route mounting | `GET /api/echo/status`, `POST /api/echo/echo` |
| `plugin.json` manifest | served back via `GET /api/plugins` on the host |
| Agent discovery via `AgentLoader.load_external()` | `echo-agent` under `project.echo` namespace |
| Namespace enforcement | agent namespace `project.echo.echo-agent` validated on load |
| TopicBus event publish | `POST /api/echo/echo` emits `EchoEvent` on `project.echo.echoed` |
| Deterministic runner | `EchoRunner.run(s) == s[::-1]` — no LLM, no network |

## Install

```bash
uv pip install -e /path/to/agentforge-echo-plugin
```

Then, against a running AgentForge:

```bash
curl -XPOST http://127.0.0.1:8001/api/plugins/register \
  -H 'content-type: application/json' \
  -d '{"package_name":"agentforge-echo-plugin"}'
```

## Verify

```bash
curl http://127.0.0.1:8001/api/echo/status
# → {"status":"ok","plugin":"echo","version":"1.0.0"}

curl -XPOST http://127.0.0.1:8001/api/echo/echo \
  -H 'content-type: application/json' \
  -d '{"msg":"hello"}'
# → {"echoed":"hello","reversed":"olleh"}

curl http://127.0.0.1:8001/api/plugins/echo/agents
# → { "plugin_id":"echo", "agents":[{"name":"echo-agent", ...}] }
```

## Run plugin-side tests

```bash
cd /path/to/agentforge-echo-plugin
uv sync
uv run pytest
```

## Guarantee

**This plugin will pass in any dev environment with no network access.** If it doesn't, the plugin system regressed — not your environment.

## Not covered (intentionally)

- Frontend module federation (`remote_url` is empty — manifest is served, but no JS bundle exists to load)
- Credential-vault integration (echo has no credentials)
- LLM-in-loop behaviours (would break determinism)

These belong in dedicated rigs when their smoke becomes worth writing.
