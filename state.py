"""State definition for LangGraph workflow - Dummy Demo"""
from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict, total=False):
    """State schema for the multi-agent workflow"""
    # Trigger & Source
    trigger_type: str  # "rss" | "api" | "proquest" | "websearch"
    source: str  # "rss-feed" | "court_listener" | "proquest" | "websearch"
    
    # RSS-specific fields
    feed_url: Optional[str]  # RSS feed URL
    feed_name: Optional[str]  # RSS feed name
    
    # Content
    url: Optional[str]
    domain: str  # For domain queuing in Content Extraction
    content: Optional[str]  # Extracted text content
    title: Optional[str]
    description: Optional[str]
    
    # Metadata (built inline by source agents)
    metadata: Dict[str, Any]  # Source-specific metadata
    
    # Pre-scraped content (for CourtListener)
    pre_scraped_content: Optional[Dict[str, str]]  # {title, description, content}
    
    # Classification results
    classification: Optional[Dict[str, Any]]  # From InsuranceTagger.process_record()
    
    # Storage
    s3_key: Optional[str]
    s3_bucket: Optional[str]
    saved: bool
    # s3_bucket_data: 
    # Control
    current_agent: str
    workflow_step: str
    errors: List[str]
    should_continue: bool
    
    # Domain queuing (for Content Extraction only)
    domain_queue_id: Optional[str]  # Domain identifier for queuing
    
    # Optional flags
    duplicate_check_enabled: bool
    skip_duplicate_check: bool

