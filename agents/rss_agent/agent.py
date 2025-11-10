"""RSS Agent Node - LangGraph agent for RSS feed processing"""
import sys
from pathlib import Path

# Handle imports
try:
    from ...state import AgentState
    from .tools import (
        fetch_rss_feed,
        parse_rss_feed,
        is_valid_url,
        check_concern_with_llm,
        extract_domain
    )
except ImportError:
    parent_dir = str(Path(__file__).parent.parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from state import AgentState
    from agents.rss_agent.tools import (
        fetch_rss_feed,
        parse_rss_feed,
        is_valid_url,
        check_concern_with_llm,
        extract_domain
    )


def rss_agent_node(state: AgentState) -> AgentState:
    """
    RSS Agent Node - Uses tools to fetch and process RSS feeds.
    This agent communicates with other agents through shared state.
    
    Flow:
    1. Fetch RSS feed XML
    2. Parse RSS entries
    3. For each entry:
       - Validate URL
       - LLM pre-filter (check concerns)
       - Build metadata
       - Pass to next agent (Content Extraction/Classification)
    """
    print(f"\n{'='*60}")
    print(f"🤖 RSS AGENT")
    print(f"{'='*60}")
    print("Agent activated. My tools:")
    print(f"  - {fetch_rss_feed.name}")
    print(f"  - {parse_rss_feed.name}")
    print(f"  - {is_valid_url.name}")
    print(f"  - {check_concern_with_llm.name}")
    print(f"  - {extract_domain.name}")
    print()
    
    # Get feed URL from state (could come from config or scheduler)
    feed_url = state.get("feed_url", "https://example.com/feed.rss")
    feed_name = state.get("feed_name", "default-feed")
    
    # Step 1: Fetch RSS feed
    print("📋 Step 1: Fetching RSS feed...")
    feed_data = fetch_rss_feed.invoke({"feed_url": feed_url})
    print(f"   ✅ Fetched feed from {feed_data['domain']}")
    print()
    
    # Step 2: Parse RSS entries
    print("📋 Step 2: Parsing RSS entries...")
    entries = parse_rss_feed.invoke({"xml_content": feed_data["xml_content"]})
    print(f"   ✅ Found {len(entries)} entries")
    print()
    
    # Step 3: Process first entry (for demo - in real flow, would process all)
    if not entries:
        print("   ⚠️ No entries found, ending workflow")
        state["should_continue"] = False
        return state
    
    entry = entries[0]  # Process first entry for demo
    link = entry.get("link", "")
    title = entry.get("title", "")
    description = entry.get("description", "")
    
    # Step 4: Validate URL
    print(f"📋 Step 3: Validating URL...")
    if not is_valid_url.invoke({"url": link}):
        print(f"   ❌ Invalid URL: {link}")
        state["should_continue"] = False
        return state
    print(f"   ✅ URL valid: {link}")
    print()
    
    # Step 5: LLM pre-filter (check concerns)
    print(f"📋 Step 4: Checking concerns with LLM...")
    has_concerns = check_concern_with_llm.invoke({
        "title": title,
        "description": description
    })
    if not has_concerns:
        print(f"   ❌ No concerns found, skipping article")
        state["should_continue"] = False
        return state
    print(f"   ✅ Concerns found, proceeding")
    print()
    
    # Step 6: Extract domain for queuing
    print(f"📋 Step 5: Extracting domain...")
    domain = extract_domain.invoke({"url": link})
    print(f"   ✅ Domain: {domain}")
    print()
    
    # Update state (this is how agents communicate)
    state["source"] = "rss-feed"
    state["url"] = link
    state["domain"] = domain
    state["title"] = title
    state["description"] = description
    # In real flow, Content Extraction Agent would crawl URL and extract content
    # For demo, we use description as placeholder content
    state["content"] = f"{title}\n\n{description}\n\n[Full content would be extracted by Content Extraction Agent]"
    state["metadata"] = {
        "title": title,
        "rss_name": feed_name,
        "published": entry.get("published")
    }
    state["pre_scraped_content"] = None  # RSS doesn't pre-scrape
    state["current_agent"] = "rss_agent"
    state["should_continue"] = True
    
    print("📤 My work is done. Passing state to Classification Agent")
    return state

