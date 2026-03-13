# CrowdStrike Falcon Integration

Connect OpenSOAR to CrowdStrike Falcon for endpoint detection and response operations.

## Features

- **Host Isolation** -- Network-contain compromised hosts and lift containment when remediation is complete.
- **Detection Management** -- Search and retrieve detection details for triage and investigation.
- **IOC Management** -- Search, create, and manage custom IOC indicators for threat hunting.
- **Device Lookup** -- Query host details for enrichment during incident response.

## Prerequisites

- CrowdStrike Falcon subscription with API access
- An OAuth2 API client with the following scopes:
  - `Hosts: Read, Write` (for device queries and containment)
  - `Detections: Read` (for detection queries)
  - `IOC Management: Read, Write` (for IOC operations)

## Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `base_url` | Yes | API base URL (default: `https://api.crowdstrike.com`) |
| `client_id` | Yes | OAuth2 API client ID |
| `client_secret` | Yes | OAuth2 API client secret |

### Cloud Regions

| Cloud | Base URL |
|-------|----------|
| US-1 | `https://api.crowdstrike.com` |
| US-2 | `https://api.us-2.crowdstrike.com` |
| EU-1 | `https://api.eu-1.crowdstrike.com` |
| GOV | `https://api.laggar.gcw.crowdstrike.com` |

## Actions

| Action | Description |
|--------|-------------|
| `crowdstrike.isolate_host` | Network-isolate a host by device ID |
| `crowdstrike.lift_containment` | Remove network isolation from a host |
| `crowdstrike.get_detection` | Get detection details by ID |
| `crowdstrike.search_detections` | Search detections with FQL filter |
| `crowdstrike.search_iocs` | Search custom IOC indicators |
| `crowdstrike.create_ioc` | Create a custom IOC indicator |
| `crowdstrike.get_device` | Get host details by device ID |

## Example Playbook Usage

```python
from opensoar_sdk import playbook

@playbook(name="crowdstrike_isolate_on_critical")
async def isolate_on_critical(alert, actions):
    detection = await actions.run("crowdstrike.get_detection", detection_id=alert.source_ref)

    if detection.get("max_severity_displayname") == "Critical":
        device_id = detection["device"]["device_id"]
        await actions.run("crowdstrike.isolate_host", device_id=device_id)
        await actions.run("slack.send_message",
            channel="#incidents",
            text=f"Isolated host {device_id} due to critical detection",
        )
```
