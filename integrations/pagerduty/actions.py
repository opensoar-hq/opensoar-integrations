from __future__ import annotations

from typing import Any

from opensoar.core.decorators import action


@action(name="pagerduty.trigger_incident", timeout=30, retries=2, retry_backoff=2.0)
async def trigger_incident(
    summary: str,
    severity: str = "error",
    source: str = "OpenSOAR",
    routing_key: str = "",
    custom_details: dict[str, Any] | None = None,
) -> dict:
    """Trigger a new PagerDuty incident via Events API v2."""
    return {
        "summary": summary,
        "severity": severity,
        "source": source,
        "note": "Configure PagerDuty integration for live incident triggering",
    }


@action(name="pagerduty.acknowledge_incident", timeout=30, retries=2, retry_backoff=2.0)
async def acknowledge_incident(dedup_key: str, routing_key: str = "") -> dict:
    """Acknowledge a PagerDuty incident by dedup key."""
    return {
        "dedup_key": dedup_key,
        "source": "pagerduty",
        "note": "Configure PagerDuty integration for live incident acknowledgment",
    }


@action(name="pagerduty.resolve_incident", timeout=30, retries=2, retry_backoff=2.0)
async def resolve_incident(dedup_key: str, routing_key: str = "") -> dict:
    """Resolve a PagerDuty incident by dedup key."""
    return {
        "dedup_key": dedup_key,
        "source": "pagerduty",
        "note": "Configure PagerDuty integration for live incident resolution",
    }


@action(name="pagerduty.get_incident", timeout=30, retries=2, retry_backoff=2.0)
async def get_incident(incident_id: str) -> dict:
    """Get PagerDuty incident details by ID."""
    return {
        "incident_id": incident_id,
        "source": "pagerduty",
        "note": "Configure PagerDuty integration for live incident lookups",
    }


@action(name="pagerduty.list_incidents", timeout=30, retries=2, retry_backoff=2.0)
async def list_incidents(
    statuses: list[str] | None = None,
    urgencies: list[str] | None = None,
    since: str = "",
    until: str = "",
) -> dict:
    """List PagerDuty incidents with filters."""
    return {
        "statuses": statuses,
        "urgencies": urgencies,
        "source": "pagerduty",
        "note": "Configure PagerDuty integration for live incident listing",
    }


@action(name="pagerduty.create_note", timeout=30, retries=2, retry_backoff=2.0)
async def create_note(incident_id: str, content: str) -> dict:
    """Add a note to a PagerDuty incident."""
    return {
        "incident_id": incident_id,
        "content": content,
        "source": "pagerduty",
        "note": "Configure PagerDuty integration for live note creation",
    }
