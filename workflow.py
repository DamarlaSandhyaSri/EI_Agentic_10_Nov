"""LangGraph Workflow - Multi-Agent Flow with Scheduler"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import sys
from pathlib import Path

# Handle imports
try:
    from .state import AgentState
    from .agents.scheduler.agent import scheduler_node
    from .agents.rss_agent.agent import rss_agent_node
    from .agents.api_agent.agent import api_agent_node
    from .agents.classification_agent.agent import classification_agent_node
    from .agents.storage_agent.agent import storage_agent_node
except ImportError:
    parent_dir = str(Path(__file__).parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from state import AgentState
    from agents.scheduler.agent import scheduler_node
    from agents.rss_agent.agent import rss_agent_node
    from agents.api_agent.agent import api_agent_node
    from agents.classification_agent.agent import classification_agent_node
    from agents.storage_agent.agent import storage_agent_node


def route_to_source_agent(state: AgentState) -> str:
    """
    Route function - determines which source agent to call based on trigger_type.
    This is used by LangGraph's conditional edges.
    """
    trigger_type = state.get("trigger_type", "").lower()
    workflow_step = state.get("workflow_step", "")
    
    # If scheduler just ran, route based on trigger_type
    if workflow_step == "rss_agent":
        return "rss_agent"
    elif workflow_step == "api_agent":
        return "api_agent"
    
    # Default fallback
    return "rss_agent"


def build_workflow():
    """
    Build LangGraph workflow with scheduler routing.
    
    Flow:
    Scheduler → (RSS Agent | API Agent) → Classification Agent → Storage Agent
    
    The scheduler reads trigger_type and routes to the appropriate source agent.
    Both RSS and API agents then flow to classification, then storage.
    
    IMPORTANT: Agents don't call each other directly!
    - Agents just return updated state
    - LangGraph's edges (defined below) route to next agent
    - Conditional edges route based on state values
    """
    # Create StateGraph with typed state
    workflow = StateGraph(AgentState)
    
    # Add agent nodes (from agents/ folder)
    workflow.add_node("scheduler", scheduler_node)
    workflow.add_node("rss_agent", rss_agent_node)
    workflow.add_node("api_agent", api_agent_node)
    workflow.add_node("classification", classification_agent_node)
    workflow.add_node("storage", storage_agent_node)
    
    # Set entry point to scheduler
    workflow.set_entry_point("scheduler")
    
    # Define flow with edges - THIS IS WHERE ROUTING HAPPENS
    # Scheduler routes to RSS or API agent based on trigger_type
    workflow.add_conditional_edges(
        "scheduler",
        route_to_source_agent,
        {
            "rss_agent": "rss_agent",
            "api_agent": "api_agent"
        }
    )
    
    # Both RSS and API agents route to classification
    workflow.add_edge("rss_agent", "classification")
    workflow.add_edge("api_agent", "classification")
    
    # Classification routes to storage
    workflow.add_edge("classification", "storage")
    
    # Storage routes to END
    workflow.add_edge("storage", END)
    
    # Compile with checkpointing
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    
    return app


if __name__ == "__main__":
    app = build_workflow()
    print("✅ LangGraph workflow built successfully!")
    print(f"   Entry: scheduler")
    print(f"   Nodes: {list(app.nodes.keys())}")
    print(f"   Flow: scheduler → (rss_agent | api_agent) → classification → storage")

