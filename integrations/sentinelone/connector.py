from __future__ import annotations

from typing import Any

import aiohttp

from opensoar.integrations.base import ActionDefinition, HealthCheckResult, IntegrationBase


class SentinelOneIntegration(IntegrationBase):
    """SentinelOne integration using API token authentication.

    Authenticates via the APIToken header against the SentinelOne management
    console REST API v2.1.
    """

    integration_type = "sentinelone"
    display_name = "SentinelOne"
    description = "Endpoint isolation, threat management, and remediation via SentinelOne"

    def __init__(self, config: dict[str, Any]):
        self._client: aiohttp.ClientSession | None = None
        super().__init__(config)

    def _validate_config(self, config: dict[str, Any]) -> None:
        for key in ("base_url", "api_token"):
            if key not in config:
                raise ValueError(f"SentinelOne requires '{key}' in config")

    @property
    def _api_base(self) -> str:
        return self._config["base_url"].rstrip("/") + "/web/api/v2.1"

    async def connect(self) -> None:
        self._client = aiohttp.ClientSession(
            base_url=self._api_base,
            headers={
                "Authorization": f"APIToken {self._config['api_token']}",
                "Content-Type": "application/json",
            },
        )

    async def health_check(self) -> HealthCheckResult:
        if not self._client:
            return HealthCheckResult(healthy=False, message="Not connected")

        try:
            async with self._client.get("/system/status") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return HealthCheckResult(
                        healthy=True,
                        message="OK",
                        details={"health": data.get("data", {}).get("health")},
                    )
                return HealthCheckResult(healthy=False, message=f"HTTP {resp.status}")
        except Exception as e:
            return HealthCheckResult(healthy=False, message=str(e))

    def get_actions(self) -> list[ActionDefinition]:
        return [
            ActionDefinition(
                name="isolate_endpoint",
                description="Disconnect an endpoint from the network",
                parameters={"agent_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="reconnect_endpoint",
                description="Reconnect a previously isolated endpoint",
                parameters={"agent_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="get_threats",
                description="Query threats with filters",
                parameters={
                    "query": {"type": "string"},
                    "limit": {"type": "integer"},
                    "status": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="get_agent",
                description="Get agent details by ID",
                parameters={"agent_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="mitigate_threat",
                description="Apply a mitigation action to a threat",
                parameters={
                    "threat_id": {"type": "string"},
                    "action": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="initiate_scan",
                description="Initiate a full disk scan on an agent",
                parameters={"agent_id": {"type": "string"}},
            ),
        ]

    async def isolate_endpoint(self, agent_id: str) -> dict:
        """Disconnect agent from network via POST /agents/actions/disconnect."""
        # TODO: Implement SentinelOne endpoint isolation
        # POST /agents/actions/disconnect
        # Body: {"filter": {"ids": [agent_id]}}
        raise NotImplementedError("TODO: implement SentinelOne isolate_endpoint")

    async def reconnect_endpoint(self, agent_id: str) -> dict:
        """Reconnect agent via POST /agents/actions/connect."""
        # TODO: Implement SentinelOne endpoint reconnection
        # POST /agents/actions/connect
        # Body: {"filter": {"ids": [agent_id]}}
        raise NotImplementedError("TODO: implement SentinelOne reconnect_endpoint")

    async def get_threats(
        self, query: str = "", limit: int = 100, status: str = ""
    ) -> dict:
        """Query threats via GET /threats."""
        # TODO: Implement SentinelOne threat query
        # GET /threats?query={query}&limit={limit}&statuses={status}
        raise NotImplementedError("TODO: implement SentinelOne get_threats")

    async def get_agent(self, agent_id: str) -> dict:
        """Get agent details via GET /agents."""
        # TODO: Implement SentinelOne agent lookup
        # GET /agents?ids={agent_id}
        raise NotImplementedError("TODO: implement SentinelOne get_agent")

    async def mitigate_threat(self, threat_id: str, action: str = "kill") -> dict:
        """Apply mitigation action via POST /threats/mitigate/{action}."""
        # TODO: Implement SentinelOne threat mitigation
        # POST /threats/mitigate/{action}
        # Body: {"filter": {"ids": [threat_id]}}
        # Valid actions: kill, quarantine, un-quarantine, remediate, rollback-remediation
        raise NotImplementedError("TODO: implement SentinelOne mitigate_threat")

    async def initiate_scan(self, agent_id: str) -> dict:
        """Initiate full disk scan via POST /agents/actions/initiate-scan."""
        # TODO: Implement SentinelOne scan initiation
        # POST /agents/actions/initiate-scan
        # Body: {"filter": {"ids": [agent_id]}}
        raise NotImplementedError("TODO: implement SentinelOne initiate_scan")

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
