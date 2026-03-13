from __future__ import annotations

from opensoar_sdk import action


@action(name="crowdstrike.isolate_host", timeout=60, retries=2, retry_backoff=2.0)
async def isolate_host(device_id: str, hostname: str = "") -> dict:
    """Network-isolate a CrowdStrike-managed host."""
    return {
        "device_id": device_id,
        "hostname": hostname,
        "source": "crowdstrike",
        "note": "Configure CrowdStrike integration for live host isolation",
    }


@action(name="crowdstrike.lift_containment", timeout=60, retries=2, retry_backoff=2.0)
async def lift_containment(device_id: str) -> dict:
    """Remove network isolation from a CrowdStrike-managed host."""
    return {
        "device_id": device_id,
        "source": "crowdstrike",
        "note": "Configure CrowdStrike integration for live containment lift",
    }


@action(name="crowdstrike.get_detection", timeout=30, retries=2, retry_backoff=2.0)
async def get_detection(detection_id: str) -> dict:
    """Look up a CrowdStrike detection by ID."""
    return {
        "detection_id": detection_id,
        "source": "crowdstrike",
        "note": "Configure CrowdStrike integration for live detection lookups",
    }


@action(name="crowdstrike.search_detections", timeout=30, retries=2, retry_backoff=2.0)
async def search_detections(filter: str = "", limit: int = 100) -> dict:
    """Search CrowdStrike detections with an FQL filter."""
    return {
        "filter": filter,
        "limit": limit,
        "source": "crowdstrike",
        "note": "Configure CrowdStrike integration for live detection search",
    }


@action(name="crowdstrike.search_iocs", timeout=30, retries=2, retry_backoff=2.0)
async def search_iocs(type: str = "", value: str = "") -> dict:
    """Search CrowdStrike custom IOC indicators."""
    return {
        "type": type,
        "value": value,
        "source": "crowdstrike",
        "note": "Configure CrowdStrike integration for live IOC search",
    }


@action(name="crowdstrike.create_ioc", timeout=30, retries=2, retry_backoff=2.0)
async def create_ioc(
    type: str,
    value: str,
    action: str = "detect",
    severity: str = "medium",
    description: str = "",
) -> dict:
    """Create a custom IOC indicator in CrowdStrike."""
    return {
        "type": type,
        "value": value,
        "action": action,
        "source": "crowdstrike",
        "note": "Configure CrowdStrike integration for live IOC creation",
    }


@action(name="crowdstrike.get_device", timeout=30, retries=2, retry_backoff=2.0)
async def get_device(device_id: str) -> dict:
    """Get CrowdStrike host details by device ID."""
    return {
        "device_id": device_id,
        "source": "crowdstrike",
        "note": "Configure CrowdStrike integration for live device lookups",
    }
