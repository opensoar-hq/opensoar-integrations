from __future__ import annotations

import pytest

from integrations.misp.connector import MISPIntegration
from integrations.misp.actions import (
    add_attribute,
    search_attributes,
    search_events,
)


class TestMISPConfig:
    def test_missing_base_url_raises(self):
        with pytest.raises(ValueError, match="base_url"):
            MISPIntegration(config={"api_key": "key"})

    def test_missing_api_key_raises(self):
        with pytest.raises(ValueError, match="api_key"):
            MISPIntegration(config={"base_url": "https://misp.example.com"})

    def test_valid_config(self):
        integration = MISPIntegration(
            config={"base_url": "https://misp.example.com", "api_key": "test-key"}
        )
        assert integration.integration_type == "misp"
        assert integration.display_name == "MISP"

    def test_verify_ssl_default(self):
        integration = MISPIntegration(
            config={"base_url": "https://misp.example.com", "api_key": "test-key"}
        )
        assert integration._config.get("verify_ssl", True) is True


class TestMISPActions:
    def test_get_actions_returns_all(self):
        integration = MISPIntegration(
            config={"base_url": "https://misp.example.com", "api_key": "test-key"}
        )
        actions = integration.get_actions()
        action_names = [a.name for a in actions]
        assert "search_events" in action_names
        assert "get_event" in action_names
        assert "create_event" in action_names
        assert "add_attribute" in action_names
        assert "search_attributes" in action_names
        assert "tag_event" in action_names


class TestMISPActionFunctions:
    @pytest.mark.asyncio
    async def test_search_events_fallback(self):
        result = await search_events(value="192.168.1.1", type="ip-dst")
        assert result["source"] == "misp"
        assert result["value"] == "192.168.1.1"

    @pytest.mark.asyncio
    async def test_add_attribute_fallback(self):
        result = await add_attribute(
            event_id="1234", type="domain", value="evil.example.com"
        )
        assert result["source"] == "misp"
        assert result["type"] == "domain"
        assert result["value"] == "evil.example.com"

    @pytest.mark.asyncio
    async def test_search_attributes_fallback(self):
        result = await search_attributes(value="evil.example.com", type="domain")
        assert result["source"] == "misp"
        assert result["value"] == "evil.example.com"
