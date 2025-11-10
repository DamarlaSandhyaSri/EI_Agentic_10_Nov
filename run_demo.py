"""Run LangGraph workflow demo - Supports RSS and API flows"""
import asyncio
import argparse
from workflow import build_workflow
from state import AgentState


def create_initial_state(trigger_type: str = "rss", feed_url: str = None, feed_name: str = None) -> AgentState:
    """
    Create initial state for workflow.
    
    Args:
        trigger_type: "rss" or "api"
        feed_url: RSS feed URL (for RSS flow)
        feed_name: RSS feed name (for RSS flow)
    """
    state = {
        "trigger_type": trigger_type,
        "source": "",
        "url": None,
        "domain": "",
        "content": None,
        "title": None,
        "description": None,
        "metadata": {},
        "pre_scraped_content": None,
        "classification": None,
        "s3_key": None,
        "s3_bucket": None,
        "saved": False,
        "current_agent": "",
        "workflow_step": "",
        "errors": [],
        "should_continue": True,
        "domain_queue_id": None,
        "duplicate_check_enabled": False,
        "skip_duplicate_check": True
    }
    
    # Add RSS-specific fields if RSS flow
    if trigger_type == "rss":
        state["feed_url"] = feed_url or "https://example.com/feed.rss"
        state["feed_name"] = feed_name or "default-feed"
    
    return state


async def run_workflow(trigger_type: str, feed_url: str = None, feed_name: str = None):
    """Run workflow with specified trigger type"""
    print("\n" + "="*70)
    if trigger_type == "rss":
        print("🎯 LANGGRAPH AGENTIC WORKFLOW - RSS FEED FLOW")
    elif trigger_type == "api":
        print("🎯 LANGGRAPH AGENTIC WORKFLOW - COURTLISTENER API FLOW")
    else:
        print(f"🎯 LANGGRAPH AGENTIC WORKFLOW - {trigger_type.upper()} FLOW")
    print("="*70)
    print("\nThis demo shows:")
    print("  ✅ Scheduler routing to source agents")
    print("  ✅ RSS Agent and API Agent")
    print("  ✅ Agents in agents/ folder")
    print("  ✅ Tools in each agent's folder")
    print("  ✅ Agents communicating through shared state")
    print("  ✅ Real LangGraph @tool decorators")
    print("  ✅ StateGraph workflow with conditional routing")
    print("\n" + "="*70)
    
    # Build workflow
    app = build_workflow()
    print(f"\n📊 Workflow Structure:")
    print(f"   Nodes: {list(app.nodes.keys())}")
    print(f"   Entry: scheduler")
    print(f"   Flow: scheduler → ({trigger_type}_agent) → classification → storage")
    print()
    
    # Create initial state
    initial_state = create_initial_state(trigger_type, feed_url, feed_name)
    
    # Run workflow
    print("🚀 Starting workflow execution...")
    print("="*70)
    
    config = {"configurable": {"thread_id": f"{trigger_type}-demo-1"}}
    final_state = await app.ainvoke(initial_state, config)
    
    print("\n" + "="*70)
    print("📊 FINAL STATE SUMMARY")
    print("="*70)
    print(f"Trigger Type: {final_state.get('trigger_type')}")
    print(f"Source: {final_state.get('source')}")
    print(f"URL: {final_state.get('url')}")
    print(f"Title: {final_state.get('title', 'N/A')}")
    if final_state.get('classification'):
        print(f"Tag: {final_state.get('classification', {}).get('tag', 'N/A')}")
    print(f"S3 Key: {final_state.get('s3_key', 'N/A')}")
    print(f"Saved: {final_state.get('saved')}")
    if final_state.get('errors'):
        print(f"Errors: {final_state.get('errors')}")
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)


async def main():
    """Main function - can run RSS, API, or all flows"""
    parser = argparse.ArgumentParser(
        description="Run LangGraph multi-agent workflow demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_demo.py --agent rss      # Run RSS feed flow
  python run_demo.py --agent api      # Run CourtListener API flow
  python run_demo.py                  # Run all flows (default)
  python run_demo.py --agent all      # Run all flows explicitly
        """
    )
    
    parser.add_argument(
        "--agent",
        type=str,
        choices=["rss", "api", "all"],
        default="all",
        help="Which agent flow to run: 'rss', 'api', or 'all' (default: all)"
    )
    
    args = parser.parse_args()
    
    # Run workflow(s) based on arguments
    if args.agent == "all":
        print("\n" + "="*70)
        print("🚀 RUNNING ALL AGENT FLOWS")
        print("="*70)
        
        # Run RSS flow
        print("\n" + "─"*70)
        await run_workflow("rss")
        
        # Run API flow
        print("\n" + "─"*70)
        await run_workflow("api")
        
        print("\n" + "="*70)
        print("✅ ALL FLOWS COMPLETE!")
        print("="*70)
    else:
        # Run single agent flow
        await run_workflow(args.agent)


if __name__ == "__main__":
    asyncio.run(main())

