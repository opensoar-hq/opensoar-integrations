from __future__ import annotations

import pytest

from integrations.sentinelone.connector import SentinelOneIntegration
from integrations.sentinelone.actions import (
    get_threats,
    isolate_endpoint,
    mitigate_threat,
)


class TestSentinelOneConfig:
    def test_missing_base_url_raises(self):
        with pytest.raises(ValueError, match="base_url"):
            SentinelOneIntegration(config={"api_token": "token"})

    def test_missing_api_token_raises(self):
        with pytest.raises(ValueError, match="api_token"):
            SentinelOneIntegration(config={"base_url": "https://example.sentinelone.net"})

    def test_valid_config(self):
        integration = SentinelOneIntegration(
            config={"base_url": "https://usea1.sentinelone.net", "api_token": "test"}
        )
        assert integration.integration_type == "sentinelone"


class TestSentinelOneActions:
    def test_get_actions_returns_all(self):
        integration = SentinelOneIntegration(
            config={"base_url": "https://usea1.sentinelone.net", "api_token": "test"}
        )
        actions = integration.get_actions()
        action_names = [a.name for a in actions]
        assert "isolate_endpoint" in action_names
        assert "reconnect_endpoint" in action_names
        assert "get_threats" in action_names
        assert "get_agent" in action_names
        assert "mitigate_threat" in action_names
        assert "initiate_scan" in action_names


class TestSentinelOneActionFunctions:
    @pytest.mark.asyncio
    async def test_isolate_endpoint_fallback(self):
        result = await isolate_endpoint(agent_id="agent-123")
        assert result["source"] == "sentinelone"
        assert result["agent_id"] == "agent-123"

    @pytest.mark.asyncio
    async def test_get_threats_fallback(self):
        result = await get_threats(query="malware", limit=50)
        assert result["source"] == "sentinelone"
        assert result["query"] == "malware"

    @pytest.mark.asyncio
    async def test_mitigate_threat_fallback(self):
        result = await mitigate_threat(threat_id="threat-456", action="quarantine")
        assert result["source"] == "sentinelone"
        assert result["action"] == "quarantine"
