# SentinelOne Integration

Connect OpenSOAR to SentinelOne for endpoint detection, response, and remediation operations.

## Features

- **Endpoint Isolation** -- Disconnect compromised endpoints and reconnect them after remediation.
- **Threat Management** -- Query, filter, and triage threats detected by SentinelOne agents.
- **Threat Mitigation** -- Kill, quarantine, remediate, or rollback threats programmatically.
- **Agent Management** -- Look up agent details and initiate full disk scans.

## Prerequisites

- SentinelOne management console with API access enabled
- An API token generated from Settings > Users > API Token

## Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `base_url` | Yes | Management console URL (e.g. `https://usea1.sentinelone.net`) |
| `api_token` | Yes | API token from the SentinelOne console |

## Actions

| Action | Description |
|--------|-------------|
| `sentinelone.isolate_endpoint` | Disconnect an endpoint from the network |
| `sentinelone.reconnect_endpoint` | Reconnect a previously isolated endpoint |
| `sentinelone.get_threats` | Query threats with filters |
| `sentinelone.get_agent` | Get agent details by ID |
| `sentinelone.mitigate_threat` | Apply a mitigation action (kill, quarantine, remediate, rollback) |
| `sentinelone.initiate_scan` | Initiate a full disk scan on an agent |

## Example Playbook Usage

```python
from opensoar.core.decorators import playbook

@playbook(name="sentinelone_auto_remediate")
async def auto_remediate(alert, actions):
    threats = await actions.run("sentinelone.get_threats",
        query=alert.source_ref,
        status="active",
    )

    for threat in threats.get("threats", []):
        agent_id = threat["agentId"]
        await actions.run("sentinelone.isolate_endpoint", agent_id=agent_id)
        await actions.run("sentinelone.mitigate_threat",
            threat_id=threat["id"],
            action="remediate",
        )
```
