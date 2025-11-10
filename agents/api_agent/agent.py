"""API Agent Node - LangGraph agent for CourtListener"""
import sys
from pathlib import Path

# Handle imports
try:
    from ...state import AgentState
    from .tools import search_courtlistener_api, scrape_document_page
except ImportError:
    parent_dir = str(Path(__file__).parent.parent.parent)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from state import AgentState
    from agents.api_agent.tools import search_courtlistener_api, scrape_document_page


def api_agent_node(state: AgentState) -> AgentState:
    """
    API Agent Node - Uses tools to query CourtListener API.
    This agent communicates with other agents through shared state.
    """
    print(f"\n{'='*60}")
    print(f"🤖 API AGENT")
    print(f"{'='*60}")
    print("Agent activated. My tools:")
    print(f"  - {search_courtlistener_api.name}")
    print(f"  - {scrape_document_page.name}")
    print()
    
    # Step 1: Use tool to search API
    print("📋 Step 1: Searching CourtListener API...")
    query_params = {"date_filed__gte": "2024-01-01", "court": "Supreme Court"}
    documents = search_courtlistener_api.invoke({"query_params": query_params})
    print(f"   ✅ Found {len(documents)} documents")
    print()
    
    # Get first document
    doc = documents[0] if documents else {}
    
    # Step 2: Use tool to scrape document
    print("📋 Step 2: Scraping document page...")
    doc_url = doc.get("url", "https://courtlistener.com/case/12345")
    scraped = scrape_document_page.invoke({"doc_url": doc_url})
    print(f"   ✅ Content scraped ({len(scraped.get('content', ''))} chars)")
    print()
    
    # Update state (this is how agents communicate)
    state["source"] = "court_listener"
    state["url"] = scraped.get("pdf_url", doc.get("url"))
    state["domain"] = "courtlistener.com"
    state["title"] = scraped.get("title")
    state["description"] = scraped.get("description")
    state["content"] = scraped.get("content")
    state["metadata"] = {
        "case_name": doc.get("case_name"),
        "docket_id": doc.get("docket_id"),
        "document_id": doc.get("document_id")
    }
    state["current_agent"] = "api_agent"
    state["should_continue"] = True
    
    print("📤 My work is done. Passing state to Classification Agent")
    return state

