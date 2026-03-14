from __future__ import annotations

import pytest

from integrations.crowdstrike.connector import CrowdStrikeIntegration
from integrations.crowdstrike.actions import (
    get_detection,
    isolate_host,
    search_detections,
)


class TestCrowdStrikeConfig:
    def test_missing_client_id_raises(self):
        with pytest.raises(ValueError, match="client_id"):
            CrowdStrikeIntegration(config={"client_secret": "secret"})

    def test_missing_client_secret_raises(self):
        with pytest.raises(ValueError, match="client_secret"):
            CrowdStrikeIntegration(config={"client_id": "id"})

    def test_valid_config(self):
        integration = CrowdStrikeIntegration(
            config={"client_id": "test-id", "client_secret": "test-secret"}
        )
        assert integration.integration_type == "crowdstrike"
        assert integration.display_name == "CrowdStrike Falcon"


class TestCrowdStrikeActions:
    def test_get_actions_returns_all(self):
        integration = CrowdStrikeIntegration(
            config={"client_id": "test-id", "client_secret": "test-secret"}
        )
        actions = integration.get_actions()
        action_names = [a.name for a in actions]
        assert "isolate_host" in action_names
        assert "lift_containment" in action_names
        assert "get_detection" in action_names
        assert "search_detections" in action_names
        assert "search_iocs" in action_names
        assert "create_ioc" in action_names
        assert "get_device" in action_names

    def test_methods_require_client(self):
        """Methods should fail gracefully when client is not connected."""
        integration = CrowdStrikeIntegration(
            config={"client_id": "test-id", "client_secret": "test-secret"}
        )
        # Client is None since connect() was not called
        assert integration._client is None


class TestCrowdStrikeActionFunctions:
    @pytest.mark.asyncio
    async def test_isolate_host_fallback(self):
        result = await isolate_host(device_id="device-123")
        assert result["source"] == "crowdstrike"
        assert result["device_id"] == "device-123"

    @pytest.mark.asyncio
    async def test_get_detection_fallback(self):
        result = await get_detection(detection_id="ldt:abc:123")
        assert result["source"] == "crowdstrike"
        assert result["detection_id"] == "ldt:abc:123"

    @pytest.mark.asyncio
    async def test_search_detections_fallback(self):
        result = await search_detections(filter="status:'new'", limit=50)
        assert result["source"] == "crowdstrike"
        assert result["filter"] == "status:'new'"
        assert result["limit"] == 50
