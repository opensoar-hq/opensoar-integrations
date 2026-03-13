from __future__ import annotations

from opensoar_sdk import action


@action(name="sentinelone.isolate_endpoint", timeout=60, retries=2, retry_backoff=2.0)
async def isolate_endpoint(agent_id: str) -> dict:
    """Disconnect a SentinelOne-managed endpoint from the network."""
    return {
        "agent_id": agent_id,
        "source": "sentinelone",
        "note": "Configure SentinelOne integration for live endpoint isolation",
    }


@action(name="sentinelone.reconnect_endpoint", timeout=60, retries=2, retry_backoff=2.0)
async def reconnect_endpoint(agent_id: str) -> dict:
    """Reconnect a previously isolated SentinelOne-managed endpoint."""
    return {
        "agent_id": agent_id,
        "source": "sentinelone",
        "note": "Configure SentinelOne integration for live endpoint reconnection",
    }


@action(name="sentinelone.get_threats", timeout=30, retries=2, retry_backoff=2.0)
async def get_threats(query: str = "", limit: int = 100, status: str = "") -> dict:
    """Query SentinelOne threats with filters."""
    return {
        "query": query,
        "limit": limit,
        "status": status,
        "source": "sentinelone",
        "note": "Configure SentinelOne integration for live threat queries",
    }


@action(name="sentinelone.get_agent", timeout=30, retries=2, retry_backoff=2.0)
async def get_agent(agent_id: str) -> dict:
    """Get SentinelOne agent details by ID."""
    return {
        "agent_id": agent_id,
        "source": "sentinelone",
        "note": "Configure SentinelOne integration for live agent lookups",
    }


@action(name="sentinelone.mitigate_threat", timeout=60, retries=2, retry_backoff=2.0)
async def mitigate_threat(threat_id: str, action: str = "kill") -> dict:
    """Apply a mitigation action to a SentinelOne threat."""
    return {
        "threat_id": threat_id,
        "action": action,
        "source": "sentinelone",
        "note": "Configure SentinelOne integration for live threat mitigation",
    }


@action(name="sentinelone.initiate_scan", timeout=60, retries=2, retry_backoff=2.0)
async def initiate_scan(agent_id: str) -> dict:
    """Initiate a full disk scan on a SentinelOne agent."""
    return {
        "agent_id": agent_id,
        "source": "sentinelone",
        "note": "Configure SentinelOne integration for live scan initiation",
    }
