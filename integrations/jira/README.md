# Jira Integration

Connect OpenSOAR to Jira Cloud or Data Center for incident tracking and ticket management.

## Features

- **Issue Creation** -- Automatically create Jira tickets when alerts fire or incidents are declared.
- **Issue Updates** -- Update fields, add comments, and transition issue status from playbooks.
- **JQL Search** -- Query existing issues to check for duplicates or related incidents.
- **Workflow Transitions** -- Move tickets through your workflow (e.g. Open -> In Progress -> Done).

## Prerequisites

- Jira Cloud or Data Center instance
- An Atlassian account with appropriate project permissions
- An API token (Cloud) generated at https://id.atlassian.com/manage-profile/security/api-tokens

## Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `base_url` | Yes | Jira instance URL (e.g. `https://yourcompany.atlassian.net`) |
| `email` | Yes | Atlassian account email |
| `api_token` | Yes | Atlassian API token |

## Actions

| Action | Description |
|--------|-------------|
| `jira.create_issue` | Create a new issue in a project |
| `jira.get_issue` | Get issue details by key (e.g. `SEC-123`) |
| `jira.update_issue` | Update fields on an existing issue |
| `jira.transition_issue` | Transition an issue to a new status |
| `jira.add_comment` | Add a comment to an issue |
| `jira.search_issues` | Search issues with JQL |

## Example Playbook Usage

```python
from opensoar_sdk import playbook

@playbook(name="create_incident_ticket")
async def create_incident_ticket(alert, actions):
    issue = await actions.run("jira.create_issue",
        project_key="SEC",
        summary=f"[{alert.severity.upper()}] {alert.title}",
        description=f"Alert ID: {alert.id}\nSource: {alert.source}\n\n{alert.description}",
        issue_type="Bug",
        priority="High" if alert.severity == "critical" else "Medium",
    )

    await actions.run("slack.send_message",
        channel="#incidents",
        text=f"Created Jira ticket {issue['issue_key']} for alert {alert.id}",
    )
```
