"""
AWS Batch Job Entry Point for LangGraph Workflow

This script is the entry point for AWS Batch jobs.
It accepts command-line arguments to specify which agent to run.
"""
import asyncio
import sys
import argparse
from workflow import build_workflow
from state import AgentState


def create_initial_state(trigger_type: str = "rss") -> AgentState:
    """
    Create initial state for workflow.
    
    Args:
        trigger_type: "rss", "api", or "all"
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
        import os
        state["feed_url"] = os.getenv("RSS_FEED_URL", "https://example.com/feed.rss")
        state["feed_name"] = os.getenv("RSS_FEED_NAME", "default-feed")
    
    return state


async def run_workflow(trigger_type: str):
    """Run workflow with specified trigger type"""
    print(f"\n{'='*70}")
    print(f"🚀 AWS BATCH JOB - LangGraph Workflow")
    print(f"   Agent: {trigger_type}")
    print(f"{'='*70}\n")
    
    try:
        # Build workflow
        app = build_workflow()
        print(f"✅ Workflow built successfully")
        print(f"   Nodes: {list(app.nodes.keys())}\n")
        
        # Create initial state
        initial_state = create_initial_state(trigger_type)
        
        # Run workflow
        print("🚀 Starting workflow execution...")
        print("="*70)
        
        config = {"configurable": {"thread_id": f"batch-{trigger_type}-{asyncio.get_event_loop().time()}"}}
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
        print("="*70)
        print("✅ WORKFLOW COMPLETE!")
        print("="*70)
        
        return 0  # Success
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1  # Failure


async def main():
    """Main function for AWS Batch job"""
    parser = argparse.ArgumentParser(
        description="AWS Batch job for LangGraph multi-agent workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--agent",
        type=str,
        choices=["rss", "api", "all"],
        default="all",
        help="Which agent flow to run: 'rss', 'api', or 'all' (default: all)"
    )
    
    args = parser.parse_args()
    
    # Run workflow(s)
    if args.agent == "all":
        print("\n" + "="*70)
        print("🚀 RUNNING ALL AGENT FLOWS")
        print("="*70)
        
        # Run RSS flow
        print("\n" + "─"*70)
        rss_result = await run_workflow("rss")
        if rss_result != 0:
            sys.exit(rss_result)
        
        # Run API flow
        print("\n" + "─"*70)
        api_result = await run_workflow("api")
        if api_result != 0:
            sys.exit(api_result)
        
        print("\n" + "="*70)
        print("✅ ALL FLOWS COMPLETE!")
        print("="*70)
        sys.exit(0)
    else:
        # Run single agent flow
        result = await run_workflow(args.agent)
        sys.exit(result)


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

