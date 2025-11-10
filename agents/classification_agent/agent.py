"""Classification Agent Node - LangGraph agent for content classification"""
import sys
from pathlib import Path

# Handle imports
try:
    from ...state import AgentState
    from .tools import classify_content
except ImportError:
    parent_dir = str(Path(__file__).parent.parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from state import AgentState
    from agents.classification_agent.tools import classify_content


def classification_agent_node(state: AgentState) -> AgentState:
    """
    Classification Agent Node - Uses tools to classify content.
    This agent receives state from API Agent and passes to Storage Agent.
    """
    print(f"\n{'='*60}")
    print(f"🤖 CLASSIFICATION AGENT")
    print(f"{'='*60}")
    print("Agent activated. My tools:")
    print(f"  - {classify_content.name}")
    print()
    print(f"📥 Received state from: {state.get('current_agent', 'unknown')}")
    print(f"📊 Content to process: {len(state.get('content', ''))} chars")
    print()
    
    # Use tool to classify
    print("📋 Classifying content...")
    content = state.get("content", "")
    classification = classify_content.invoke({"content": content})
    print(f"   ✅ Classification complete:")
    print(f"      - Tag: {classification['tag']}")
    print(f"      - Risks: {classification['risks']}")
    print(f"      - NAICS: {classification['naics_codes']}")
    print()
    
    # Update state (this is how agents communicate)
    state["classification"] = classification
    state["current_agent"] = "classification"
    state["should_continue"] = True
    
    print("📤 My work is done. Passing state to Storage Agent")
    return state

