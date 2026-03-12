from __future__ import annotations

import base64
from typing import Any

import aiohttp

from opensoar.integrations.base import ActionDefinition, HealthCheckResult, IntegrationBase


class JiraIntegration(IntegrationBase):
    """Jira Cloud / Data Center integration using REST API v3.

    Authenticates with email + API token (Cloud) using Basic Auth.
    All endpoints are under /rest/api/3/.
    """

    integration_type = "jira"
    display_name = "Jira"
    description = "Issue creation, updates, transitions, and JQL search for incident tracking"

    def __init__(self, config: dict[str, Any]):
        self._client: aiohttp.ClientSession | None = None
        super().__init__(config)

    def _validate_config(self, config: dict[str, Any]) -> None:
        for key in ("base_url", "email", "api_token"):
            if key not in config:
                raise ValueError(f"Jira requires '{key}' in config")

    @property
    def _api_base(self) -> str:
        return self._config["base_url"].rstrip("/")

    def _auth_header(self) -> str:
        credentials = f"{self._config['email']}:{self._config['api_token']}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    async def connect(self) -> None:
        self._client = aiohttp.ClientSession(
            base_url=self._api_base,
            headers={
                "Authorization": self._auth_header(),
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

    async def health_check(self) -> HealthCheckResult:
        if not self._client:
            return HealthCheckResult(healthy=False, message="Not connected")

        try:
            async with self._client.get("/rest/api/3/myself") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return HealthCheckResult(
                        healthy=True,
                        message="OK",
                        details={"user": data.get("displayName")},
                    )
                return HealthCheckResult(healthy=False, message=f"HTTP {resp.status}")
        except Exception as e:
            return HealthCheckResult(healthy=False, message=str(e))

    def get_actions(self) -> list[ActionDefinition]:
        return [
            ActionDefinition(
                name="create_issue",
                description="Create a new Jira issue",
                parameters={
                    "project_key": {"type": "string"},
                    "summary": {"type": "string"},
                    "description": {"type": "string"},
                    "issue_type": {"type": "string"},
                    "priority": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="get_issue",
                description="Get issue details by key",
                parameters={"issue_key": {"type": "string"}},
            ),
            ActionDefinition(
                name="update_issue",
                description="Update fields on an existing issue",
                parameters={
                    "issue_key": {"type": "string"},
                    "fields": {"type": "object"},
                },
            ),
            ActionDefinition(
                name="transition_issue",
                description="Transition an issue to a new status",
                parameters={
                    "issue_key": {"type": "string"},
                    "transition_name": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="add_comment",
                description="Add a comment to an issue",
                parameters={
                    "issue_key": {"type": "string"},
                    "body": {"type": "string"},
                },
            ),
            ActionDefinition(
                name="search_issues",
                description="Search issues with JQL",
                parameters={
                    "jql": {"type": "string"},
                    "max_results": {"type": "integer"},
                },
            ),
        ]

    async def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str = "",
        issue_type: str = "Task",
        priority: str = "Medium",
    ) -> dict:
        """Create issue via POST /rest/api/3/issue."""
        # TODO: Implement Jira issue creation
        # POST /rest/api/3/issue
        # Body: {
        #   "fields": {
        #     "project": {"key": project_key},
        #     "summary": summary,
        #     "description": {"type": "doc", "version": 1, "content": [...]},
        #     "issuetype": {"name": issue_type},
        #     "priority": {"name": priority},
        #   }
        # }
        raise NotImplementedError("TODO: implement Jira create_issue")

    async def get_issue(self, issue_key: str) -> dict:
        """Get issue via GET /rest/api/3/issue/{issueKey}."""
        # TODO: Implement Jira issue lookup
        # GET /rest/api/3/issue/{issue_key}
        raise NotImplementedError("TODO: implement Jira get_issue")

    async def update_issue(self, issue_key: str, fields: dict[str, Any] | None = None) -> dict:
        """Update issue via PUT /rest/api/3/issue/{issueKey}."""
        # TODO: Implement Jira issue update
        # PUT /rest/api/3/issue/{issue_key}
        # Body: {"fields": fields}
        raise NotImplementedError("TODO: implement Jira update_issue")

    async def transition_issue(self, issue_key: str, transition_name: str) -> dict:
        """Transition issue via POST /rest/api/3/issue/{issueKey}/transitions."""
        # TODO: Implement Jira issue transition
        # Step 1: GET /rest/api/3/issue/{issue_key}/transitions to find transition ID
        # Step 2: POST /rest/api/3/issue/{issue_key}/transitions
        # Body: {"transition": {"id": transition_id}}
        raise NotImplementedError("TODO: implement Jira transition_issue")

    async def add_comment(self, issue_key: str, body: str) -> dict:
        """Add comment via POST /rest/api/3/issue/{issueKey}/comment."""
        # TODO: Implement Jira add comment
        # POST /rest/api/3/issue/{issue_key}/comment
        # Body: {
        #   "body": {
        #     "type": "doc", "version": 1,
        #     "content": [{"type": "paragraph", "content": [{"type": "text", "text": body}]}]
        #   }
        # }
        raise NotImplementedError("TODO: implement Jira add_comment")

    async def search_issues(self, jql: str, max_results: int = 50) -> dict:
        """Search issues via POST /rest/api/3/search."""
        # TODO: Implement Jira JQL search
        # POST /rest/api/3/search
        # Body: {"jql": jql, "maxResults": max_results}
        raise NotImplementedError("TODO: implement Jira search_issues")

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
