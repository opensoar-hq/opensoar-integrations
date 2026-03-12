from __future__ import annotations

from typing import Any

import aiohttp
import ssl

from opensoar.integrations.base import ActionDefinition, HealthCheckResult, IntegrationBase


class MISPIntegration(IntegrationBase):
    """MISP (Malware Information Sharing Platform) integration.

    Authenticates via the Authorization header with an automation API key.
    All endpoints accept and return JSON via the /events, /attributes,
    and /tags REST endpoints.
    """

    integration_type = "misp"
    display_name = "MISP"
    description = "Threat intelligence event and IOC management via MISP"

    def __init__(self, config: dict[str, Any]):
        self._client: aiohttp.ClientSession | None = None
        super().__init__(config)

    def _validate_config(self, config: dict[str, Any]) -> None:
        for key in ("base_url", "api_key"):
            if key not in config:
                raise ValueError(f"MISP requires '{key}' in config")

    @property
    def _api_base(self) -> str:
        return self._config["base_url"].rstrip("/")

    async def connect(self) -> None:
        ssl_context: ssl.SSLContext | bool = True
        if not self._config.get("verify_ssl", True):
            ssl_context = False

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self._client = aiohttp.ClientSession(
            base_url=self._api_base,
            headers={
                "Authorization": self._config["api_key"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            connector=connector,
        )

    async def health_check(self) -> HealthCheckResult:
        if not self._client:
            return HealthCheckResult(healthy=False, message="Not connected")

        try:
            async with self._client.get("/servers/getVersion.json") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return HealthCheckResult(
                        healthy=True,
                        message="OK",
                        details={"version": data.get("version")},
                    )
                return HealthCheckResult(healthy=False, message=f"HTTP {resp.status}")
        except Exception as e:
            return HealthCheckResult(healthy=False, message=str(e))

    def get_actions(self) -> list[ActionDefinition]:
        return [
            ActionDefinition(
                name="search_events",
                description="Search MISP events",
                parameters={
                    "value": {"type": "string"},
                    "type": {"type": "string"},
                    "tags": {"type": "array"},
                    "limit": {"type": "integer"},
                },
            ),
            ActionDefinition(
                name="get_event",
                description="Get full event details by ID",
                parameters={"event_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="create_event",
                description="Create a new MISP event",
                parameters={
                    "info": {"type": "string"},
                    "distribution": {"type": "integer"},
                    "threat_level": {"type": "integer"},
                    "analysis": {"type": "integer"},
                },
            ),
            ActionDefinition(
                name="add_attribute",
                description="Add an attribute (IOC) to an event",
                parameters={
                    "event_id": {"type": "string"},
                    "type": {"type": "string"},
                    "value": {"type": "string"},
                    "category": {"type": "string"},
                    "to_ids": {"type": "boolean"},
                    "comment": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="search_attributes",
                description="Search attributes across all events",
                parameters={
                    "value": {"type": "string"},
                    "type": {"type": "string"},
                    "category": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="tag_event",
                description="Add a tag to an event",
                parameters={
                    "event_id": {"type": "string"},
                    "tag": {"type": "string"},
                },
            ),
        ]

    async def search_events(
        self,
        value: str = "",
        type: str = "",
        tags: list[str] | None = None,
        limit: int = 50,
    ) -> dict:
        """Search events via POST /events/restSearch."""
        # TODO: Implement MISP event search
        # POST /events/restSearch
        # Body: {
        #   "returnFormat": "json",
        #   "value": value,
        #   "type": type,
        #   "tags": tags,
        #   "limit": limit,
        # }
        raise NotImplementedError("TODO: implement MISP search_events")

    async def get_event(self, event_id: str) -> dict:
        """Get event via GET /events/view/{eventId}."""
        # TODO: Implement MISP event lookup
        # GET /events/view/{event_id}
        raise NotImplementedError("TODO: implement MISP get_event")

    async def create_event(
        self,
        info: str,
        distribution: int = 0,
        threat_level: int = 2,
        analysis: int = 0,
    ) -> dict:
        """Create event via POST /events/add."""
        # TODO: Implement MISP event creation
        # POST /events/add
        # Body: {
        #   "Event": {
        #     "info": info,
        #     "distribution": distribution,  # 0=org, 1=community, 2=connected, 3=all
        #     "threat_level_id": threat_level,  # 1=high, 2=medium, 3=low, 4=undefined
        #     "analysis": analysis,  # 0=initial, 1=ongoing, 2=complete
        #   }
        # }
        raise NotImplementedError("TODO: implement MISP create_event")

    async def add_attribute(
        self,
        event_id: str,
        type: str,
        value: str,
        category: str = "",
        to_ids: bool = True,
        comment: str = "",
    ) -> dict:
        """Add attribute via POST /attributes/add/{eventId}."""
        # TODO: Implement MISP attribute creation
        # POST /attributes/add/{event_id}
        # Body: {
        #   "type": type,  # e.g. ip-dst, domain, md5, sha256, url
        #   "value": value,
        #   "category": category,  # e.g. Network activity, Payload delivery
        #   "to_ids": to_ids,
        #   "comment": comment,
        # }
        raise NotImplementedError("TODO: implement MISP add_attribute")

    async def search_attributes(
        self,
        value: str = "",
        type: str = "",
        category: str = "",
        tags: list[str] | None = None,
    ) -> dict:
        """Search attributes via POST /attributes/restSearch."""
        # TODO: Implement MISP attribute search
        # POST /attributes/restSearch
        # Body: {
        #   "returnFormat": "json",
        #   "value": value,
        #   "type": type,
        #   "category": category,
        #   "tags": tags,
        # }
        raise NotImplementedError("TODO: implement MISP search_attributes")

    async def tag_event(self, event_id: str, tag: str) -> dict:
        """Tag event via POST /tags/attachTagToObject."""
        # TODO: Implement MISP event tagging
        # POST /tags/attachTagToObject
        # Body: {"uuid": event_uuid, "tag": tag}
        # Note: need to resolve event_id to UUID first via get_event
        raise NotImplementedError("TODO: implement MISP tag_event")

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
