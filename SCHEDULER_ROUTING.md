# Scheduler and Multi-Agent Routing

This document explains how the scheduler routes to different source agents (RSS, API) in the LangGraph workflow.

## Architecture Overview

```
Scheduler Agent
    ↓
    ├─→ RSS Agent (if trigger_type == "rss")
    │       ↓
    │   Classification Agent
    │       ↓
    │   Storage Agent
    │
    └─→ API Agent (if trigger_type == "api")
            ↓
        Classification Agent
            ↓
        Storage Agent
```

## How It Works

### 1. Scheduler Agent (`agents/scheduler/agent.py`)

The scheduler is the **entry point** of the workflow. It:
- Reads `trigger_type` from state
- Routes to appropriate source agent:
  - `"rss"` → RSS Agent
  - `"api"` → API Agent (CourtListener)
  - `"proquest"` → (future)
  - `"websearch"` → (future)
- Sets `workflow_step` in state to indicate which agent to route to

### 2. Conditional Routing (`workflow.py`)

The workflow uses **conditional edges** to route from scheduler:

```python
workflow.add_conditional_edges(
    "scheduler",
    route_to_source_agent,  # Routing function
    {
        "rss_agent": "rss_agent",
        "api_agent": "api_agent"
    }
)
```

The `route_to_source_agent()` function checks `workflow_step` set by scheduler and returns the appropriate agent name.

### 3. Source Agents

Both RSS and API agents:
- Process their respective sources
- Update state with content, metadata, etc.
- Route to **Classification Agent** (same for both)
- Classification routes to **Storage Agent**

## Usage

### Running RSS Flow

```bash
cd langraph
python run_demo.py --agent rss
```

Or in code:
```python
initial_state = create_initial_state(trigger_type="rss")
```

### Running API Flow

```bash
cd langraph
python run_demo.py --agent api
```

Or in code:
```python
initial_state = create_initial_state(trigger_type="api")
```

### Running All Flows

```bash
cd langraph
python run_demo.py
# or
python run_demo.py --agent all
```

## State Fields

### RSS-Specific Fields
- `feed_url`: RSS feed URL
- `feed_name`: RSS feed name

### Common Fields
- `trigger_type`: "rss" | "api" | "proquest" | "websearch"
- `source`: "rss-feed" | "court_listener" | etc.
- `workflow_step`: Set by scheduler to indicate routing target

## Adding New Source Agents

To add a new source agent (e.g., ProQuest):

1. **Create agent** in `agents/proquest_agent/`
2. **Update scheduler** to handle `trigger_type == "proquest"`
3. **Add node** to workflow: `workflow.add_node("proquest_agent", proquest_agent_node)`
4. **Update routing function** to include "proquest_agent"
5. **Add edge** from proquest_agent to classification

Example:
```python
# In scheduler/agent.py
elif trigger_type == "proquest":
    state["workflow_step"] = "proquest_agent"

# In workflow.py
workflow.add_node("proquest_agent", proquest_agent_node)
workflow.add_edge("proquest_agent", "classification")
```

## Key Points

1. **Scheduler is entry point** - All workflows start here
2. **Conditional routing** - LangGraph routes based on state values
3. **Shared downstream** - Both RSS and API flow to same Classification → Storage
4. **State-based communication** - Agents communicate through shared state, not direct calls

