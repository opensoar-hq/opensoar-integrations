from __future__ import annotations

from typing import Any

import aiohttp

from opensoar_sdk import Integration, ActionDefinition, HealthCheckResult

# PagerDuty API endpoints
_EVENTS_API_V2 = "https://events.pagerduty.com/v2/enqueue"
_REST_API_BASE = "https://api.pagerduty.com"


class PagerDutyIntegration(Integration):
    """PagerDuty integration using Events API v2 and REST API v2.

    Uses two authentication mechanisms:
    - Events API v2: routing key (integration key) for triggering/ack/resolve
    - REST API v2: API token for querying incidents and adding notes
    """

    integration_type = "pagerduty"
    display_name = "PagerDuty"
    description = "Incident triggering, acknowledgment, and resolution via PagerDuty"

    def __init__(self, config: dict[str, Any]):
        self._client: aiohttp.ClientSession | None = None
        self._events_client: aiohttp.ClientSession | None = None
        super().__init__(config)

    def _validate_config(self, config: dict[str, Any]) -> None:
        if "api_token" not in config:
            raise ValueError("PagerDuty requires 'api_token' in config")

    async def connect(self) -> None:
        self._client = aiohttp.ClientSession(
            base_url=_REST_API_BASE,
            headers={
                "Authorization": f"Token token={self._config['api_token']}",
                "Content-Type": "application/json",
                "Accept": "application/vnd.pagerduty+json;version=2",
            },
        )
        self._events_client = aiohttp.ClientSession(
            headers={"Content-Type": "application/json"},
        )

    async def health_check(self) -> HealthCheckResult:
        if not self._client:
            return HealthCheckResult(healthy=False, message="Not connected")

        try:
            async with self._client.get("/abilities") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return HealthCheckResult(
                        healthy=True,
                        message="OK",
                        details={"abilities": data.get("abilities", [])},
                    )
                return HealthCheckResult(healthy=False, message=f"HTTP {resp.status}")
        except Exception as e:
            return HealthCheckResult(healthy=False, message=str(e))

    def get_actions(self) -> list[ActionDefinition]:
        return [
            ActionDefinition(
                name="trigger_incident",
                description="Trigger a new incident via Events API v2",
                parameters={
                    "summary": {"type": "string"},
                    "severity": {"type": "string"},
                    "source": {"type": "string"},
                    "routing_key": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="acknowledge_incident",
                description="Acknowledge an incident by dedup key",
                parameters={
                    "dedup_key": {"type": "string"},
                    "routing_key": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="resolve_incident",
                description="Resolve an incident by dedup key",
                parameters={
                    "dedup_key": {"type": "string"},
                    "routing_key": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="get_incident",
                description="Get incident details by ID",
                parameters={"incident_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="list_incidents",
                description="List incidents with filters",
                parameters={
                    "statuses": {"type": "array"},
                    "urgencies": {"type": "array"},
                    "since": {"type": "string"},
                    "until": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="create_note",
                description="Add a note to an incident",
                parameters={
                    "incident_id": {"type": "string"},
                    "content": {"type": "string"},
                },
            ),
        ]

    async def trigger_incident(
        self,
        summary: str,
        severity: str = "error",
        source: str = "OpenSOAR",
        routing_key: str = "",
        custom_details: dict[str, Any] | None = None,
    ) -> dict:
        """Trigger incident via POST https://events.pagerduty.com/v2/enqueue."""
        try:
            assert self._events_client is not None
            body = {
                "routing_key": routing_key or self._config.get("routing_key", ""),
                "event_action": "trigger",
                "payload": {
                    "summary": summary,
                    "severity": severity,
                    "source": source,
                    "custom_details": custom_details or {},
                },
            }
            async with self._events_client.post(
                _EVENTS_API_V2, json=body
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def acknowledge_incident(self, dedup_key: str, routing_key: str = "") -> dict:
        """Acknowledge incident via POST https://events.pagerduty.com/v2/enqueue."""
        try:
            assert self._events_client is not None
            body = {
                "routing_key": routing_key or self._config.get("routing_key", ""),
                "event_action": "acknowledge",
                "dedup_key": dedup_key,
            }
            async with self._events_client.post(
                _EVENTS_API_V2, json=body
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def resolve_incident(self, dedup_key: str, routing_key: str = "") -> dict:
        """Resolve incident via POST https://events.pagerduty.com/v2/enqueue."""
        try:
            assert self._events_client is not None
            body = {
                "routing_key": routing_key or self._config.get("routing_key", ""),
                "event_action": "resolve",
                "dedup_key": dedup_key,
            }
            async with self._events_client.post(
                _EVENTS_API_V2, json=body
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_incident(self, incident_id: str) -> dict:
        """Get incident via GET /incidents/{id}."""
        try:
            assert self._client is not None
            async with self._client.get(
                f"/incidents/{incident_id}"
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def list_incidents(
        self,
        statuses: list[str] | None = None,
        urgencies: list[str] | None = None,
        since: str = "",
        until: str = "",
    ) -> dict:
        """List incidents via GET /incidents."""
        try:
            assert self._client is not None
            params: list[tuple[str, str]] = []
            if statuses:
                for s in statuses:
                    params.append(("statuses[]", s))
            if urgencies:
                for u in urgencies:
                    params.append(("urgencies[]", u))
            if since:
                params.append(("since", since))
            if until:
                params.append(("until", until))
            async with self._client.get("/incidents", params=params) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def create_note(self, incident_id: str, content: str) -> dict:
        """Add note via POST /incidents/{id}/notes."""
        try:
            assert self._client is not None
            headers: dict[str, str] = {}
            from_email = self._config.get("default_from_email")
            if from_email:
                headers["From"] = from_email
            async with self._client.post(
                f"/incidents/{incident_id}/notes",
                json={"note": {"content": content}},
                headers=headers,
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
        if self._events_client:
            await self._events_client.close()
