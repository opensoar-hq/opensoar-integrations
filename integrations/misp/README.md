# MISP Integration

Connect OpenSOAR to MISP (Malware Information Sharing Platform) for threat intelligence enrichment and IOC management.

## Features

- **Event Search** -- Search MISP events by indicator value, type, or tags for threat context.
- **Event Management** -- Create new events to track incidents and share threat intelligence.
- **IOC Management** -- Add attributes (indicators of compromise) to events for correlation.
- **Attribute Search** -- Search across all events for matching IOCs to check for known threats.
- **Tagging** -- Apply tags to events for classification and workflow automation.

## Prerequisites

- MISP instance (self-hosted or cloud)
- An automation API key from your MISP user profile (Administration > Auth Keys)

## Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `base_url` | Yes | MISP instance URL (e.g. `https://misp.yourorg.com`) |
| `api_key` | Yes | MISP automation API key |
| `verify_ssl` | No | Verify SSL certificates (default: `true`, set `false` for self-signed) |

## Actions

| Action | Description |
|--------|-------------|
| `misp.search_events` | Search events by value, type, or tags |
| `misp.get_event` | Get full event details by ID |
| `misp.create_event` | Create a new event |
| `misp.add_attribute` | Add an IOC attribute to an event |
| `misp.search_attributes` | Search attributes across all events |
| `misp.tag_event` | Add a tag to an event |

### MISP Attribute Types

Common attribute types you can use with `add_attribute`:

| Type | Example |
|------|---------|
| `ip-dst` | `192.168.1.1` |
| `ip-src` | `10.0.0.1` |
| `domain` | `evil.example.com` |
| `md5` | `d41d8cd98f00b204e9800998ecf8427e` |
| `sha256` | `e3b0c44298fc1c149afbf4c8996fb924...` |
| `url` | `https://evil.example.com/payload` |
| `email-src` | `phish@evil.com` |

## Example Playbook Usage

```python
from opensoar_sdk import playbook

@playbook(name="enrich_ioc_from_misp")
async def enrich_from_misp(alert, actions):
    for ioc in alert.iocs:
        results = await actions.run("misp.search_attributes",
            value=ioc["value"],
            type=ioc["type"],
        )

        if results.get("total", 0) > 0:
            await actions.run("slack.send_message",
                channel="#threat-intel",
                text=f"IOC {ioc['value']} found in {results['total']} MISP events",
            )
```
