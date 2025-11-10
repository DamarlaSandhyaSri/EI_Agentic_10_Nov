# LangGraph Multi-Agent Workflow

A complete LangGraph implementation showing multi-agent workflows with scheduler-based routing for RSS feeds and CourtListener API.

## 📁 Structure

```
langraph/
├── state.py                    # Typed state schema
├── workflow.py                # StateGraph workflow with scheduler routing
├── run_demo.py                # Demo runner with CLI
├── README.md                  # This file
├── SCHEDULER_ROUTING.md       # Architecture design for scheduler routing
├── requirements.txt           # Dependencies
└── agents/
    ├── scheduler/
    │   ├── __init__.py
    │   └── agent.py           # Scheduler agent (entry point)
    ├── rss_agent/
    │   ├── __init__.py
    │   ├── tools.py           # RSS agent tools
    │   └── agent.py           # RSS agent node
    ├── api_agent/
    │   ├── __init__.py
    │   ├── tools.py           # API agent tools
    │   └── agent.py           # API agent node
    ├── classification_agent/
    │   ├── __init__.py
    │   ├── tools.py           # Classification agent tools
    │   └── agent.py           # Classification agent node
    └── storage_agent/
        ├── __init__.py
        ├── tools.py           # Storage agent tools
        └── agent.py           # Storage agent node
```

## 🎯 Key Features

1. **Scheduler-Based Routing** - Entry point routes to RSS or API agent based on `trigger_type`
2. **Multi-Agent Architecture** - RSS Agent, API Agent, Classification Agent, Storage Agent
3. **Agent Communication** - Agents communicate through shared `AgentState`
4. **Real LangGraph Tools** - Uses `@tool` decorator from `langchain_core.tools`
5. **StateGraph Workflow** - LangGraph's StateGraph with conditional routing
6. **CLI Control** - Run specific agents or all flows via command line

## 🚀 Quick Start

### Installation

```bash
cd langraph
pip install -r requirements.txt
```

### Running the Demo

```bash
# Run all flows (default)
python run_demo.py

# Run RSS flow only
python run_demo.py --agent rss

# Run API flow only
python run_demo.py --agent api

# Show help
python run_demo.py --help
```

## 📊 Architecture Flow

```
Scheduler Agent (Entry Point)
    ↓ (conditional routing based on trigger_type)
    ├─→ RSS Agent → Classification Agent → Storage Agent
    └─→ API Agent → Classification Agent → Storage Agent
```

## 🔧 How It Works

### 1. Scheduler Agent

The scheduler is the **entry point** that:
- Reads `trigger_type` from state ("rss" or "api")
- Routes to appropriate source agent
- Sets `workflow_step` for conditional routing

### 2. Source Agents (RSS & API)

**RSS Agent:**
- Fetches RSS feed XML
- Parses entries
- Validates URLs
- Checks concerns with LLM (pre-filter)
- Extracts domain for queuing

**API Agent (CourtListener):**
- Searches CourtListener API
- Scrapes document pages
- Extracts content and metadata

### 3. Classification Agent

- Receives content from source agents
- Classifies using LLM
- Extracts tags, risks, NAICS codes

### 4. Storage Agent

- Formats data for S3
- Generates S3 keys
- Saves to S3 storage

### 5. Agent Communication

Agents **don't call each other directly**. Instead:

1. Agent receives state
2. Agent uses tools to do work
3. Agent updates state
4. Agent returns state
5. **LangGraph routes** to next agent based on edges

This decoupling is the power of LangGraph - agents are independent and the workflow orchestrates everything!

## 🔄 Routing Mechanism

Routing is defined in `workflow.py`:

```python
# Conditional routing from scheduler
workflow.add_conditional_edges(
    "scheduler",
    route_to_source_agent,  # Routing function
    {
        "rss_agent": "rss_agent",
        "api_agent": "api_agent"
    }
)

# Both source agents route to classification
workflow.add_edge("rss_agent", "classification")
workflow.add_edge("api_agent", "classification")

# Classification routes to storage
workflow.add_edge("classification", "storage")
workflow.add_edge("storage", END)
```

## 💡 What Makes This Agentic?

1. **Tools** - Each agent has tools it can use (defined with `@tool` decorator)
2. **Tool Calling** - Agents call tools with `.invoke()`
3. **State Communication** - Agents communicate through shared state
4. **Workflow Orchestration** - LangGraph StateGraph manages agent flow
5. **Agent Autonomy** - Each agent decides how to use its tools
6. **Checkpointing** - LangGraph checkpointing for durable execution

## ✅ Pure LangGraph Implementation

This is a **complete LangGraph agentic flow**:
- ✅ **LangGraph StateGraph** - Workflow orchestration
- ✅ **LangGraph Nodes** - Agent functions
- ✅ **LangGraph Edges** - Flow definition (including conditional edges)
- ✅ **LangGraph Checkpointing** - State persistence
- ✅ **Standard Tool Pattern** - `@tool` from `langchain_core.tools` (official LangGraph pattern)
- ✅ **State-Based Communication** - Agents communicate through shared state

**Note:** Using `langchain_core.tools` for tool definitions is the **standard, recommended approach** in LangGraph. LangGraph integrates with LangChain's tool system while providing pure LangGraph workflow orchestration.

## 📚 Additional Documentation

- **SCHEDULER_ROUTING.md** - Detailed architecture design for scheduler and multi-agent routing

## 🔧 Troubleshooting

### ModuleNotFoundError

```bash
pip install langgraph langchain-core
```

### Import Errors

Make sure you're in the `langraph` folder:
```bash
cd langraph
python run_demo.py
```

### Virtual Environment

```bash
# Activate your venv first
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Then install and run
pip install -r requirements.txt
python run_demo.py --agent rss
```

## 🎯 Summary

This implementation demonstrates:
- Multi-agent workflows with LangGraph
- Scheduler-based routing to different source agents
- Agent communication through shared state
- Real-world patterns for RSS and API processing
- Complete workflow from source → classification → storage

This is the **real LangGraph way** to build agentic workflows!
