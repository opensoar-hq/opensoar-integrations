from __future__ import annotations

from opensoar.core.decorators import action


@action(name="your-tool.example_action", timeout=30, retries=2, retry_backoff=2.0)
async def example_action(param1: str, param2: str = "") -> dict:
    """Execute the example action.

    This fallback runs when no connector is configured. Replace with
    a meaningful placeholder response.
    """
    return {
        "param1": param1,
        "param2": param2,
        "source": "your-tool",
        "note": "Configure your-tool integration for live results",
    }
