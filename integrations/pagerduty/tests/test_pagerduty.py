from __future__ import annotations

import pytest

from integrations.pagerduty.connector import PagerDutyIntegration
from integrations.pagerduty.actions import (
    trigger_incident,
    acknowledge_incident,
    resolve_incident,
)


class TestPagerDutyConfig:
    def test_missing_api_token_raises(self):
        with pytest.raises(ValueError, match="api_token"):
            PagerDutyIntegration(config={})

    def test_valid_config(self):
        integration = PagerDutyIntegration(config={"api_token": "test-token"})
        assert integration.integration_type == "pagerduty"
        assert integration.display_name == "PagerDuty"

    def test_optional_routing_key(self):
        integration = PagerDutyIntegration(
            config={"api_token": "test-token", "routing_key": "R123"}
        )
        assert integration._config["routing_key"] == "R123"


class TestPagerDutyActions:
    def test_get_actions_returns_all(self):
        integration = PagerDutyIntegration(config={"api_token": "test-token"})
        actions = integration.get_actions()
        action_names = [a.name for a in actions]
        assert "trigger_incident" in action_names
        assert "acknowledge_incident" in action_names
        assert "resolve_incident" in action_names
        assert "get_incident" in action_names
        assert "list_incidents" in action_names
        assert "create_note" in action_names


class TestPagerDutyActionFunctions:
    @pytest.mark.asyncio
    async def test_trigger_incident_fallback(self):
        result = await trigger_incident(summary="Test alert", severity="critical")
        assert result["summary"] == "Test alert"
        assert result["severity"] == "critical"

    @pytest.mark.asyncio
    async def test_acknowledge_incident_fallback(self):
        result = await acknowledge_incident(dedup_key="dedup-123")
        assert result["dedup_key"] == "dedup-123"
        assert result["source"] == "pagerduty"

    @pytest.mark.asyncio
    async def test_resolve_incident_fallback(self):
        result = await resolve_incident(dedup_key="dedup-123")
        assert result["dedup_key"] == "dedup-123"
        assert result["source"] == "pagerduty"
