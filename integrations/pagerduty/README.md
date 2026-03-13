# PagerDuty Integration

Connect OpenSOAR to PagerDuty for automated incident management and on-call escalation.

## Features

- **Incident Triggering** -- Automatically create PagerDuty incidents from critical alerts.
- **Acknowledgment & Resolution** -- Acknowledge and resolve incidents programmatically from playbooks.
- **Incident Queries** -- List and filter incidents for dashboards and reporting.
- **Notes** -- Add investigation notes to incidents for audit trails.

## Prerequisites

- PagerDuty account with API access
- REST API token (v2) from PagerDuty > Integrations > API Access Keys
- (Optional) Events API v2 integration key from a service's Integrations tab

## Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `api_token` | Yes | PagerDuty REST API v2 token |
| `routing_key` | No | Default Events API v2 routing key for triggering incidents |
| `default_from_email` | No | PagerDuty user email for API actions requiring a `From` header |

## Actions

| Action | Description |
|--------|-------------|
| `pagerduty.trigger_incident` | Trigger a new incident via Events API v2 |
| `pagerduty.acknowledge_incident` | Acknowledge an incident by dedup key |
| `pagerduty.resolve_incident` | Resolve an incident by dedup key |
| `pagerduty.get_incident` | Get incident details by ID |
| `pagerduty.list_incidents` | List incidents with status/urgency filters |
| `pagerduty.create_note` | Add a note to an incident |

## Example Playbook Usage

```python
from opensoar_sdk import playbook

@playbook(name="escalate_critical_alert")
async def escalate_critical(alert, actions):
    if alert.severity == "critical":
        result = await actions.run("pagerduty.trigger_incident",
            summary=f"[CRITICAL] {alert.title}",
            severity="critical",
            source="OpenSOAR",
            custom_details={
                "alert_id": alert.id,
                "source": alert.source,
                "description": alert.description,
            },
        )

        await actions.run("slack.send_message",
            channel="#incidents",
            text=f"PagerDuty incident triggered: {result.get('dedup_key', 'N/A')}",
        )
```
