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
        # TODO: Implement PagerDuty event trigger
        # POST https://events.pagerduty.com/v2/enqueue
        # Body: {
        #   "routing_key": routing_key or self._config.get("routing_key"),
        #   "event_action": "trigger",
        #   "payload": {
        #     "summary": summary,
        #     "severity": severity,  # critical, error, warning, info
        #     "source": source,
        #     "custom_details": custom_details or {},
        #   },
        # }
        raise NotImplementedError("TODO: implement PagerDuty trigger_incident")

    async def acknowledge_incident(self, dedup_key: str, routing_key: str = "") -> dict:
        """Acknowledge incident via POST https://events.pagerduty.com/v2/enqueue."""
        # TODO: Implement PagerDuty event acknowledgment
        # POST https://events.pagerduty.com/v2/enqueue
        # Body: {
        #   "routing_key": routing_key or self._config.get("routing_key"),
        #   "event_action": "acknowledge",
        #   "dedup_key": dedup_key,
        # }
        raise NotImplementedError("TODO: implement PagerDuty acknowledge_incident")

    async def resolve_incident(self, dedup_key: str, routing_key: str = "") -> dict:
        """Resolve incident via POST https://events.pagerduty.com/v2/enqueue."""
        # TODO: Implement PagerDuty event resolution
        # POST https://events.pagerduty.com/v2/enqueue
        # Body: {
        #   "routing_key": routing_key or self._config.get("routing_key"),
        #   "event_action": "resolve",
        #   "dedup_key": dedup_key,
        # }
        raise NotImplementedError("TODO: implement PagerDuty resolve_incident")

    async def get_incident(self, incident_id: str) -> dict:
        """Get incident via GET /incidents/{id}."""
        # TODO: Implement PagerDuty incident lookup
        # GET /incidents/{incident_id}
        raise NotImplementedError("TODO: implement PagerDuty get_incident")

    async def list_incidents(
        self,
        statuses: list[str] | None = None,
        urgencies: list[str] | None = None,
        since: str = "",
        until: str = "",
    ) -> dict:
        """List incidents via GET /incidents."""
        # TODO: Implement PagerDuty incident listing
        # GET /incidents?statuses[]={status}&urgencies[]={urgency}&since={since}&until={until}
        raise NotImplementedError("TODO: implement PagerDuty list_incidents")

    async def create_note(self, incident_id: str, content: str) -> dict:
        """Add note via POST /incidents/{id}/notes."""
        # TODO: Implement PagerDuty note creation
        # POST /incidents/{incident_id}/notes
        # Headers: {"From": self._config.get("default_from_email")}
        # Body: {"note": {"content": content}}
        raise NotImplementedError("TODO: implement PagerDuty create_note")

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
        if self._events_client:
            await self._events_client.close()
