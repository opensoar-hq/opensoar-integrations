from __future__ import annotations

import pytest

from integrations.jira.connector import JiraIntegration
from integrations.jira.actions import create_issue, search_issues, transition_issue


class TestJiraConfig:
    def test_missing_base_url_raises(self):
        with pytest.raises(ValueError, match="base_url"):
            JiraIntegration(config={"email": "a@b.com", "api_token": "tok"})

    def test_missing_email_raises(self):
        with pytest.raises(ValueError, match="email"):
            JiraIntegration(config={"base_url": "https://x.atlassian.net", "api_token": "tok"})

    def test_missing_api_token_raises(self):
        with pytest.raises(ValueError, match="api_token"):
            JiraIntegration(config={"base_url": "https://x.atlassian.net", "email": "a@b.com"})

    def test_valid_config(self):
        integration = JiraIntegration(
            config={"base_url": "https://x.atlassian.net", "email": "a@b.com", "api_token": "tok"}
        )
        assert integration.integration_type == "jira"


class TestJiraActions:
    def test_get_actions_returns_all(self):
        integration = JiraIntegration(
            config={"base_url": "https://x.atlassian.net", "email": "a@b.com", "api_token": "tok"}
        )
        actions = integration.get_actions()
        action_names = [a.name for a in actions]
        assert "create_issue" in action_names
        assert "get_issue" in action_names
        assert "update_issue" in action_names
        assert "transition_issue" in action_names
        assert "add_comment" in action_names
        assert "search_issues" in action_names


class TestJiraActionFunctions:
    @pytest.mark.asyncio
    async def test_create_issue_fallback(self):
        result = await create_issue(project_key="SEC", summary="Test alert")
        assert result["source"] == "jira"
        assert result["project_key"] == "SEC"
        assert result["summary"] == "Test alert"

    @pytest.mark.asyncio
    async def test_search_issues_fallback(self):
        result = await search_issues(jql="project = SEC ORDER BY created DESC")
        assert result["source"] == "jira"
        assert "SEC" in result["jql"]

    @pytest.mark.asyncio
    async def test_transition_issue_fallback(self):
        result = await transition_issue(issue_key="SEC-42", transition_name="In Progress")
        assert result["source"] == "jira"
        assert result["issue_key"] == "SEC-42"
