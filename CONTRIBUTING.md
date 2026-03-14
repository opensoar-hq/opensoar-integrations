# Contributing to OpenSOAR Integrations

Thank you for your interest in building integrations for OpenSOAR! This guide walks you through creating a new community integration pack.

## Quick Start

1. Fork this repository
2. Copy the template: `cp -r templates/integration-template integrations/your-tool`
3. Implement your integration (see below)
4. Add tests
5. Open a pull request

## Integration Structure

Every integration lives in its own directory under `integrations/` and contains:

```
integrations/your-tool/
├── manifest.yaml      # Metadata, config schema, action definitions
├── connector.py       # Integration class that manages the API connection
├── actions.py         # @action decorated functions for use in playbooks
├── README.md          # Documentation for users of this integration
└── tests/
    └── test_your_tool.py
```

## manifest.yaml

The manifest describes your integration to OpenSOAR's loader. Required fields:

```yaml
name: your-tool              # Unique identifier (lowercase, hyphens OK)
display_name: Your Tool      # Human-readable name
version: 0.1.0               # SemVer
author: Your Name            # Or "OpenSOAR Community"
description: Short summary
category: edr|siem|soar|itsm|alerting|threat_intel|email|chat|cloud|identity
min_sdk_version: "0.1.0"

config:
  api_key:
    type: string
    required: true
    secret: true              # Secrets are encrypted at rest and masked in logs
    description: API key for authentication
  base_url:
    type: string
    required: false
    default: "https://api.example.com"
    description: API base URL

actions:
  - name: action_name
    description: What this action does
    inputs: [param1, param2]
    outputs: [result_field1, result_field2]
```

### Config Field Types

- `string` -- plain text or secret
- `integer` -- whole numbers
- `boolean` -- true/false
- `choice` -- use with `choices: [a, b, c]`

Mark any credentials with `secret: true` so OpenSOAR encrypts them at rest and redacts them from logs.

## connector.py

Your connector must subclass `Integration` from `opensoar_sdk`:

```python
from __future__ import annotations

from typing import Any

import aiohttp

from opensoar_sdk import (
    ActionDefinition,
    HealthCheckResult,
    Integration,
)


class YourToolIntegration(Integration):
    integration_type = "your-tool"
    display_name = "Your Tool"
    description = "What it does"

    def __init__(self, config: dict[str, Any]):
        self._client: aiohttp.ClientSession | None = None
        super().__init__(config)

    def _validate_config(self, config: dict[str, Any]) -> None:
        if "api_key" not in config:
            raise ValueError("your-tool requires 'api_key' in config")

    async def connect(self) -> None:
        self._client = aiohttp.ClientSession(
            base_url=config["base_url"],
            headers={"Authorization": f"Bearer {self._config['api_key']}"},
        )

    async def health_check(self) -> HealthCheckResult:
        # Make a lightweight API call to verify credentials
        ...

    def get_actions(self) -> list[ActionDefinition]:
        return [
            ActionDefinition(
                name="do_something",
                description="Does something useful",
                parameters={"target": {"type": "string"}},
            ),
        ]

    async def do_something(self, target: str) -> dict:
        # Implement the actual API call
        ...

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
```

### Key Requirements

- All I/O must be **async** (use `aiohttp`, not `requests`).
- `_validate_config` should raise `ValueError` for missing required config.
- `connect()` sets up the HTTP session.
- `health_check()` makes a real (lightweight) API call.
- `disconnect()` cleans up the session.
- Action methods must match the names in `get_actions()`.

## actions.py

Actions are standalone decorated functions that playbooks can call. They should work even without a configured connector (returning a placeholder if needed):

```python
from opensoar_sdk import action


@action(name="your-tool.do_something", timeout=30, retries=2, retry_backoff=2.0)
async def do_something(target: str) -> dict:
    """Does something useful."""
    # When the integration is connected, OpenSOAR routes this to the connector.
    # This fallback runs if no connector is configured.
    return {
        "target": target,
        "note": "Configure your-tool integration for live results",
    }
```

### Action Decorator Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `name` | required | Namespaced action name (`integration.action`) |
| `timeout` | `60` | Seconds before the action times out |
| `retries` | `0` | Number of retry attempts on failure |
| `retry_backoff` | `1.0` | Multiplier for exponential backoff |

## Tests

Write tests in `tests/test_your_tool.py`. At minimum, test:

1. Config validation (missing required fields raise `ValueError`)
2. Action definitions are returned correctly
3. Action functions return the expected structure

```python
import pytest

from integrations.your_tool.connector import YourToolIntegration


def test_validate_config_missing_key():
    with pytest.raises(ValueError):
        YourToolIntegration(config={})


def test_get_actions():
    integration = YourToolIntegration(config={"api_key": "test"})
    actions = integration.get_actions()
    assert len(actions) > 0
    assert all(a.name for a in actions)
```

Run tests with:

```bash
pip install -e ".[dev]"
pytest integrations/your-tool/tests/
```

## Code Style

- Type hints on all public functions
- Docstrings on action functions
- `from __future__ import annotations` at the top of every module
- Follow the patterns in existing integrations

## Pull Request Checklist

- [ ] `manifest.yaml` is complete with config schema and actions
- [ ] `connector.py` subclasses `Integration` with all abstract methods
- [ ] `actions.py` has `@action` decorated functions for each action
- [ ] `README.md` documents setup and usage
- [ ] Tests pass: `pytest integrations/your-tool/tests/`
- [ ] No secrets or credentials in the code
- [ ] Optional dependency added to `pyproject.toml`

## Questions?

Open an issue on the [main OpenSOAR repo](https://github.com/opensoar-hq/opensoar-core) or start a discussion.
