from __future__ import annotations

from opensoar_sdk import action


@action(name="misp.search_events", timeout=30, retries=2, retry_backoff=2.0)
async def search_events(
    value: str = "",
    type: str = "",
    tags: list[str] | None = None,
    limit: int = 50,
) -> dict:
    """Search MISP events by value, type, or tags."""
    return {
        "value": value,
        "type": type,
        "tags": tags,
        "limit": limit,
        "source": "misp",
        "note": "Configure MISP integration for live event search",
    }


@action(name="misp.get_event", timeout=30, retries=2, retry_backoff=2.0)
async def get_event(event_id: str) -> dict:
    """Get MISP event details by ID."""
    return {
        "event_id": event_id,
        "source": "misp",
        "note": "Configure MISP integration for live event lookups",
    }


@action(name="misp.create_event", timeout=30, retries=2, retry_backoff=2.0)
async def create_event(
    info: str,
    distribution: int = 0,
    threat_level: int = 2,
    analysis: int = 0,
) -> dict:
    """Create a new MISP event."""
    return {
        "info": info,
        "distribution": distribution,
        "threat_level": threat_level,
        "source": "misp",
        "note": "Configure MISP integration for live event creation",
    }


@action(name="misp.add_attribute", timeout=30, retries=2, retry_backoff=2.0)
async def add_attribute(
    event_id: str,
    type: str,
    value: str,
    category: str = "",
    to_ids: bool = True,
    comment: str = "",
) -> dict:
    """Add an attribute (IOC) to a MISP event."""
    return {
        "event_id": event_id,
        "type": type,
        "value": value,
        "category": category,
        "source": "misp",
        "note": "Configure MISP integration for live attribute creation",
    }


@action(name="misp.search_attributes", timeout=30, retries=2, retry_backoff=2.0)
async def search_attributes(
    value: str = "",
    type: str = "",
    category: str = "",
    tags: list[str] | None = None,
) -> dict:
    """Search MISP attributes across all events."""
    return {
        "value": value,
        "type": type,
        "category": category,
        "source": "misp",
        "note": "Configure MISP integration for live attribute search",
    }


@action(name="misp.tag_event", timeout=30, retries=2, retry_backoff=2.0)
async def tag_event(event_id: str, tag: str) -> dict:
    """Add a tag to a MISP event."""
    return {
        "event_id": event_id,
        "tag": tag,
        "source": "misp",
        "note": "Configure MISP integration for live event tagging",
    }
