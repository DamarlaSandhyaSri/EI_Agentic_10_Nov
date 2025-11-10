"""Scheduler Agent Node - Routes to RSS or API agent based on trigger_type"""
import sys
from pathlib import Path

# Handle imports
try:
    from ...state import AgentState
except ImportError:
    parent_dir = str(Path(__file__).parent.parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from state import AgentState


def scheduler_node(state: AgentState) -> AgentState:
    """
    Scheduler Agent Node - Routes to appropriate source agent.
    
    This is the entry point that reads trigger_type and routes to:
    - "rss" → RSS Agent
    - "api" → API Agent (CourtListener)
    - "proquest" → ProQuest Agent (future)
    - "websearch" → WebSearch Agent (future)
    
    The scheduler doesn't do any processing itself - it just sets up
    the state for the next agent and lets LangGraph route to it.
    """
    print(f"\n{'='*60}")
    print(f"📅 SCHEDULER AGENT")
    print(f"{'='*60}")
    
    trigger_type = state.get("trigger_type", "").lower()
    
    print(f"📋 Trigger Type: {trigger_type}")
    print(f"📋 Current State:")
    print(f"   - Source: {state.get('source', 'not set')}")
    print(f"   - URL: {state.get('url', 'not set')}")
    print()
    
    # Set up state based on trigger type
    if trigger_type == "rss":
        print("✅ Routing to RSS Agent")
        # Set feed info if not already set
        if not state.get("feed_url"):
            state["feed_url"] = "https://example.com/feed.rss"
        if not state.get("feed_name"):
            state["feed_name"] = "default-feed"
        state["current_agent"] = "scheduler"
        state["workflow_step"] = "rss_agent"
        
    elif trigger_type == "api":
        print("✅ Routing to API Agent (CourtListener)")
        state["current_agent"] = "scheduler"
        state["workflow_step"] = "api_agent"
        
    elif trigger_type == "proquest":
        print("⚠️ ProQuest Agent not yet implemented")
        state["should_continue"] = False
        state["errors"].append("ProQuest Agent not implemented")
        
    elif trigger_type == "websearch":
        print("⚠️ WebSearch Agent not yet implemented")
        state["should_continue"] = False
        state["errors"].append("WebSearch Agent not implemented")
        
    else:
        print(f"❌ Unknown trigger_type: {trigger_type}")
        print("   Valid types: 'rss', 'api', 'proquest', 'websearch'")
        state["should_continue"] = False
        state["errors"].append(f"Unknown trigger_type: {trigger_type}")
    
    print()
    return state

