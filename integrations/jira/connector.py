from __future__ import annotations

import base64
from typing import Any

import aiohttp

from opensoar_sdk import Integration, ActionDefinition, HealthCheckResult


class JiraIntegration(Integration):
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
        try:
            assert self._client is not None
            adf_description = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description or ""}],
                    }
                ],
            }
            body = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": summary,
                    "description": adf_description,
                    "issuetype": {"name": issue_type},
                    "priority": {"name": priority},
                }
            }
            async with self._client.post(
                "/rest/api/3/issue", json=body
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_issue(self, issue_key: str) -> dict:
        """Get issue via GET /rest/api/3/issue/{issueKey}."""
        try:
            assert self._client is not None
            async with self._client.get(
                f"/rest/api/3/issue/{issue_key}"
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def update_issue(self, issue_key: str, fields: dict[str, Any] | None = None) -> dict:
        """Update issue via PUT /rest/api/3/issue/{issueKey}."""
        try:
            assert self._client is not None
            async with self._client.put(
                f"/rest/api/3/issue/{issue_key}",
                json={"fields": fields or {}},
            ) as resp:
                if resp.status == 204:
                    return {"status": "ok"}
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def transition_issue(self, issue_key: str, transition_name: str) -> dict:
        """Transition issue via POST /rest/api/3/issue/{issueKey}/transitions."""
        try:
            assert self._client is not None
            # Step 1: Get available transitions
            async with self._client.get(
                f"/rest/api/3/issue/{issue_key}/transitions"
            ) as resp:
                data = await resp.json()
            transitions = data.get("transitions", [])
            transition_id = None
            for t in transitions:
                if t.get("name", "").lower() == transition_name.lower():
                    transition_id = t["id"]
                    break
            if not transition_id:
                return {
                    "error": f"Transition '{transition_name}' not found",
                    "available": [t.get("name") for t in transitions],
                }
            # Step 2: Perform the transition
            async with self._client.post(
                f"/rest/api/3/issue/{issue_key}/transitions",
                json={"transition": {"id": transition_id}},
            ) as resp:
                if resp.status == 204:
                    return {"status": "ok"}
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def add_comment(self, issue_key: str, body: str) -> dict:
        """Add comment via POST /rest/api/3/issue/{issueKey}/comment."""
        try:
            assert self._client is not None
            adf_body = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": body}],
                    }
                ],
            }
            async with self._client.post(
                f"/rest/api/3/issue/{issue_key}/comment",
                json={"body": adf_body},
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def search_issues(self, jql: str, max_results: int = 50) -> dict:
        """Search issues via POST /rest/api/3/search."""
        try:
            assert self._client is not None
            async with self._client.post(
                "/rest/api/3/search",
                json={"jql": jql, "maxResults": max_results},
            ) as resp:
                return await resp.json()
        except Exception as e:
            return {"error": str(e)}

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
