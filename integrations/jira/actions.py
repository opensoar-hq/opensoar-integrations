from __future__ import annotations

from typing import Any

from opensoar_sdk import action


@action(name="jira.create_issue", timeout=30, retries=2, retry_backoff=2.0)
async def create_issue(
    project_key: str,
    summary: str,
    description: str = "",
    issue_type: str = "Task",
    priority: str = "Medium",
) -> dict:
    """Create a new Jira issue."""
    return {
        "project_key": project_key,
        "summary": summary,
        "issue_type": issue_type,
        "source": "jira",
        "note": "Configure Jira integration for live issue creation",
    }


@action(name="jira.get_issue", timeout=30, retries=2, retry_backoff=2.0)
async def get_issue(issue_key: str) -> dict:
    """Get Jira issue details by key."""
    return {
        "issue_key": issue_key,
        "source": "jira",
        "note": "Configure Jira integration for live issue lookups",
    }


@action(name="jira.update_issue", timeout=30, retries=2, retry_backoff=2.0)
async def update_issue(issue_key: str, fields: dict[str, Any] | None = None) -> dict:
    """Update fields on an existing Jira issue."""
    return {
        "issue_key": issue_key,
        "fields": fields,
        "source": "jira",
        "note": "Configure Jira integration for live issue updates",
    }


@action(name="jira.transition_issue", timeout=30, retries=2, retry_backoff=2.0)
async def transition_issue(issue_key: str, transition_name: str) -> dict:
    """Transition a Jira issue to a new status."""
    return {
        "issue_key": issue_key,
        "transition_name": transition_name,
        "source": "jira",
        "note": "Configure Jira integration for live issue transitions",
    }


@action(name="jira.add_comment", timeout=30, retries=2, retry_backoff=2.0)
async def add_comment(issue_key: str, body: str) -> dict:
    """Add a comment to a Jira issue."""
    return {
        "issue_key": issue_key,
        "body": body,
        "source": "jira",
        "note": "Configure Jira integration for live comments",
    }


@action(name="jira.search_issues", timeout=30, retries=2, retry_backoff=2.0)
async def search_issues(jql: str, max_results: int = 50) -> dict:
    """Search Jira issues with JQL."""
    return {
        "jql": jql,
        "max_results": max_results,
        "source": "jira",
        "note": "Configure Jira integration for live JQL search",
    }
