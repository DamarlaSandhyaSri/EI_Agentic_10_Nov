"""RSS Agent Tools - Using @tool decorator"""
from langchain_core.tools import tool
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
import time


@tool
def fetch_rss_feed(feed_url: str) -> Dict[str, Any]:
    """
    Fetch RSS feed XML from a URL.
    
    Args:
        feed_url: URL of the RSS feed
    
    Returns:
        Dictionary with raw XML content and metadata
    """
    print(f"  🔧 TOOL: fetch_rss_feed(feed_url='{feed_url}')")
    time.sleep(0.3)
    
    # Dummy response - in real implementation, would use fetch_with_crawl4ai
    return {
        "xml_content": "<rss>...</rss>",  # Dummy XML
        "url": feed_url,
        "domain": urlparse(feed_url).netloc
    }


@tool
def parse_rss_feed(xml_content: str) -> List[Dict[str, Any]]:
    """
    Parse RSS feed XML into entries.
    
    Args:
        xml_content: Raw RSS XML content
    
    Returns:
        List of RSS entry dictionaries with title, description, link, etc.
    """
    print(f"  🔧 TOOL: parse_rss_feed(xml_content='{len(xml_content)} chars')")
    time.sleep(0.2)
    
    # Dummy response - in real implementation, would use feedparser.parse()
    return [
        {
            "title": "Insurance Regulation Update 2024",
            "description": "New regulations affecting insurance companies in 2024",
            "link": "https://example.com/article1",
            "published": "2024-01-15T10:00:00Z"
        },
        {
            "title": "Climate Risk Assessment Guidelines",
            "description": "New guidelines for assessing climate-related risks",
            "link": "https://example.com/article2",
            "published": "2024-01-14T15:30:00Z"
        }
    ]


@tool
def is_valid_url(url: str) -> bool:
    """
    Validate if a URL is properly formatted.
    
    Args:
        url: URL string to validate
    
    Returns:
        True if URL is valid, False otherwise
    """
    print(f"  🔧 TOOL: is_valid_url(url='{url}')")
    time.sleep(0.1)
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


@tool
def check_concern_with_llm(title: str, description: str) -> bool:
    """
    Check if RSS entry has insurance-related concerns using LLM.
    This is a pre-filter to skip unrelated articles before crawling.
    
    Args:
        title: Article title
        description: Article description
    
    Returns:
        True if article has concerns, False otherwise
    """
    print(f"  🔧 TOOL: check_concern_with_llm(title='{title[:50]}...')")
    time.sleep(0.5)
    
    # Dummy response - in real implementation, would use BedrockClient
    # with CONCERN_CHECK_FOR_RSS_PROMPT
    keywords = ["insurance", "risk", "regulation", "climate", "legal"]
    text = (title + " " + description).lower()
    return any(keyword in text for keyword in keywords)


@tool
def extract_domain(url: str) -> str:
    """
    Extract domain from URL for domain-based queuing.
    
    Args:
        url: Full URL
    
    Returns:
        Domain string (e.g., "example.com")
    """
    print(f"  🔧 TOOL: extract_domain(url='{url}')")
    time.sleep(0.1)
    
    try:
        return urlparse(url).netloc
    except Exception:
        return "unknown"

