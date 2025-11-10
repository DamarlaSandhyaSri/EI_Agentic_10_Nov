"""Storage Agent Node - LangGraph agent for saving to S3"""
import sys
from pathlib import Path
from datetime import datetime

# Handle imports
try:
    from ...state import AgentState
    from .tools import save_to_s3
except ImportError:
    parent_dir = str(Path(__file__).parent.parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from state import AgentState
    from agents.storage_agent.tools import save_to_s3


def storage_agent_node(state: AgentState) -> AgentState:
    """
    Storage Agent Node - Uses tools to save to S3.
    This agent receives state from Classification Agent and completes the workflow.
    """
    print(f"\n{'='*60}")
    print(f"🤖 STORAGE AGENT")
    print(f"{'='*60}")
    print("Agent activated. My tools:")
    print(f"  - {save_to_s3.name}")
    print()
    print(f"📥 Received state from: {state.get('current_agent', 'unknown')}")
    print(f"📊 Classification data: {state.get('classification', {})}")
    print()
    
    # Build S3 key
    source = state.get("source", "unknown")
    date_str = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-EST")
    source_folder = source.replace("_", "-").title()
    s3_key = f"{source_folder}/{date_str}/{source_folder}-{timestamp}.json"
    s3_bucket = "dummy-insurance-bucket"
    
    # Build payload
    payload = {
        "url": state.get("url"),
        "title": state.get("title"),
        "content": state.get("content", "")[:500],
        "classification": state.get("classification", {}),
        "metadata": state.get("metadata", {})
    }
    
    # Use tool to save
    print("📋 Saving to S3...")
    saved = save_to_s3.invoke({"bucket": s3_bucket, "key": s3_key, "data": payload})
    print(f"   ✅ Saved: s3://{s3_bucket}/{s3_key}")
    print()
    
    # Update state (workflow complete)
    state["s3_key"] = s3_key
    state["s3_bucket"] = s3_bucket
    state["saved"] = saved
    state["current_agent"] = "storage"
    state["should_continue"] = False  # End workflow
    
    print("📤 My work is done. Workflow complete!")
    return state

