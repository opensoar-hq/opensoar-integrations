from __future__ import annotations

import time
from typing import Any

import aiohttp

from opensoar_sdk import Integration, ActionDefinition, HealthCheckResult


class CrowdStrikeIntegration(Integration):
    """CrowdStrike Falcon integration using OAuth2 client credentials.

    Authenticates via the /oauth2/token endpoint and uses the bearer token
    for all subsequent API calls. The token is refreshed automatically when
    it expires.
    """

    integration_type = "crowdstrike"
    display_name = "CrowdStrike Falcon"
    description = "Host isolation, detection management, and IOC operations via CrowdStrike Falcon"

    def __init__(self, config: dict[str, Any]):
        self._client: aiohttp.ClientSession | None = None
        self._token: str | None = None
        self._token_expiry: float = 0
        super().__init__(config)

    def _validate_config(self, config: dict[str, Any]) -> None:
        for key in ("client_id", "client_secret"):
            if key not in config:
                raise ValueError(f"CrowdStrike requires '{key}' in config")

    @property
    def _base_url(self) -> str:
        return self._config.get("base_url", "https://api.crowdstrike.com")

    async def _authenticate(self) -> None:
        """Obtain or refresh an OAuth2 bearer token."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._base_url}/oauth2/token",
                data={
                    "client_id": self._config["client_id"],
                    "client_secret": self._config["client_secret"],
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                self._token = data["access_token"]
                self._token_expiry = time.time() + data.get("expires_in", 1799)

    async def _ensure_token(self) -> str:
        """Return a valid bearer token, refreshing if necessary."""
        if not self._token or time.time() >= self._token_expiry - 60:
            await self._authenticate()
        assert self._token is not None
        return self._token

    async def connect(self) -> None:
        await self._authenticate()
        self._client = aiohttp.ClientSession(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
        )

    async def health_check(self) -> HealthCheckResult:
        if not self._client:
            return HealthCheckResult(healthy=False, message="Not connected")

        try:
            token = await self._ensure_token()
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            async with self._client.get("/sensors/queries/sensors/v1?limit=1") as resp:
                if resp.status == 200:
                    return HealthCheckResult(healthy=True, message="OK")
                return HealthCheckResult(
                    healthy=False,
                    message=f"HTTP {resp.status}",
                    details={"body": await resp.text()},
                )
        except Exception as e:
            return HealthCheckResult(healthy=False, message=str(e))

    def get_actions(self) -> list[ActionDefinition]:
        return [
            ActionDefinition(
                name="isolate_host",
                description="Network-isolate a host by device ID",
                parameters={"device_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="lift_containment",
                description="Remove network isolation from a host",
                parameters={"device_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="get_detection",
                description="Get detection details by ID",
                parameters={"detection_id": {"type": "string"}},
            ),
            ActionDefinition(
                name="search_detections",
                description="Search detections with FQL filter",
                parameters={
                    "filter": {"type": "string"},
                    "limit": {"type": "integer"},
                },
            ),
            ActionDefinition(
                name="search_iocs",
                description="Search custom IOC indicators",
                parameters={
                    "type": {"type": "string"},
                    "value": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="create_ioc",
                description="Create a custom IOC indicator",
                parameters={
                    "type": {"type": "string"},
                    "value": {"type": "string"},
                    "action": {"type": "string"},
                    "severity": {"type": "string"},
                    "description": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="get_device",
                description="Get host details by device ID",
                parameters={"device_id": {"type": "string"}},
            ),
        ]

    async def isolate_host(self, device_id: str) -> dict:
        """Network-contain a host via POST /devices/entities/devices-actions/v2."""
        try:
            token = await self._ensure_token()
            assert self._client is not None
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            async with self._client.post(
                "/devices/entities/devices-actions/v2?action_name=contain",
                json={"ids": [device_id]},
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def lift_containment(self, device_id: str) -> dict:
        """Lift containment via POST /devices/entities/devices-actions/v2."""
        try:
            token = await self._ensure_token()
            assert self._client is not None
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            async with self._client.post(
                "/devices/entities/devices-actions/v2?action_name=lift_containment",
                json={"ids": [device_id]},
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_detection(self, detection_id: str) -> dict:
        """Get detection details via POST /detects/entities/summaries/GET/v1."""
        try:
            token = await self._ensure_token()
            assert self._client is not None
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            async with self._client.post(
                "/detects/entities/summaries/GET/v1",
                json={"ids": [detection_id]},
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def search_detections(self, filter: str = "", limit: int = 100) -> dict:
        """Search detections via GET /detects/queries/detects/v1."""
        try:
            token = await self._ensure_token()
            assert self._client is not None
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            params: dict[str, Any] = {"limit": limit}
            if filter:
                params["filter"] = filter
            async with self._client.get(
                "/detects/queries/detects/v1",
                params=params,
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def search_iocs(self, type: str = "", value: str = "") -> dict:
        """Search IOC indicators via GET /iocs/queries/indicators/v1."""
        try:
            token = await self._ensure_token()
            assert self._client is not None
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            filter_parts = []
            if type:
                filter_parts.append(f"type:'{type}'")
            if value:
                filter_parts.append(f"value:'{value}'")
            params: dict[str, str] = {}
            if filter_parts:
                params["filter"] = "+".join(filter_parts)
            async with self._client.get(
                "/iocs/queries/indicators/v1",
                params=params,
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def create_ioc(
        self,
        type: str,
        value: str,
        action: str = "detect",
        severity: str = "medium",
        description: str = "",
    ) -> dict:
        """Create a custom IOC via POST /iocs/entities/indicators/v1."""
        try:
            token = await self._ensure_token()
            assert self._client is not None
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            indicator: dict[str, Any] = {
                "type": type,
                "value": value,
                "action": action,
                "severity": severity,
            }
            if description:
                indicator["description"] = description
            async with self._client.post(
                "/iocs/entities/indicators/v1",
                json={"indicators": [indicator]},
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_device(self, device_id: str) -> dict:
        """Get host details via POST /devices/entities/devices/v2."""
        try:
            token = await self._ensure_token()
            assert self._client is not None
            self._client.headers.update({"Authorization": f"Bearer {token}"})
            async with self._client.post(
                "/devices/entities/devices/v2",
                json={"ids": [device_id]},
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
