from __future__ import annotations

from typing import Any

import aiohttp

from opensoar.integrations.base import ActionDefinition, HealthCheckResult, IntegrationBase


class YourToolIntegration(IntegrationBase):
    """Your Tool integration.

    Replace this docstring with a description of how this integration
    authenticates and what API version it targets.
    """

    integration_type = "your-tool"
    display_name = "Your Tool Name"
    description = "Brief description of what this integration does"

    def __init__(self, config: dict[str, Any]):
        self._client: aiohttp.ClientSession | None = None
        super().__init__(config)

    def _validate_config(self, config: dict[str, Any]) -> None:
        for key in ("api_key", "base_url"):
            if key not in config:
                raise ValueError(f"Your Tool requires '{key}' in config")

    async def connect(self) -> None:
        self._client = aiohttp.ClientSession(
            base_url=self._config["base_url"],
            headers={
                "Authorization": f"Bearer {self._config['api_key']}",
                "Content-Type": "application/json",
            },
        )

    async def health_check(self) -> HealthCheckResult:
        if not self._client:
            return HealthCheckResult(healthy=False, message="Not connected")

        try:
            # TODO: Replace with a lightweight API endpoint for health checking
            async with self._client.get("/health") as resp:
                if resp.status == 200:
                    return HealthCheckResult(healthy=True, message="OK")
                return HealthCheckResult(healthy=False, message=f"HTTP {resp.status}")
        except Exception as e:
            return HealthCheckResult(healthy=False, message=str(e))

    def get_actions(self) -> list[ActionDefinition]:
        return [
            ActionDefinition(
                name="example_action",
                description="Describe what this action does",
                parameters={
                    "param1": {"type": "string"},
                    "param2": {"type": "string"},
                },
            ),
        ]

    async def example_action(self, param1: str, param2: str = "") -> dict:
        """Execute the example action."""
        # TODO: Implement the actual API call
        # Example:
        # async with self._client.post("/api/endpoint", json={"key": param1}) as resp:
        #     return await resp.json()
        raise NotImplementedError("TODO: implement example_action")

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
