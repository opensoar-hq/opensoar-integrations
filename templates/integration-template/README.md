# Your Tool Name Integration

Connect OpenSOAR to Your Tool Name for [describe use case].

## Features

- **Feature 1** -- Describe what this feature does.
- **Feature 2** -- Describe what this feature does.

## Prerequisites

- List prerequisites here (account, API access, permissions, etc.)

## Configuration

| Field | Required | Description |
|-------|----------|-------------|
| `api_key` | Yes | API key for authentication |
| `base_url` | Yes | API base URL |

## Actions

| Action | Description |
|--------|-------------|
| `your-tool.example_action` | Describe what this action does |

## Example Playbook Usage

```python
from opensoar.core.decorators import playbook

@playbook(name="your_playbook")
async def your_playbook(alert, actions):
    result = await actions.run("your-tool.example_action",
        param1="value1",
        param2="value2",
    )
```
