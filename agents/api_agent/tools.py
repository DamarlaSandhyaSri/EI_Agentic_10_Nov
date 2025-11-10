"""API Agent Tools - Using @tool decorator"""
from langchain_core.tools import tool
from typing import Dict, Any, List
import time


@tool
def search_courtlistener_api(query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Search CourtListener API for legal documents.
    
    Args:
        query_params: Dictionary with search parameters (date_filed__gte, court, etc.)
    
    Returns:
        List of document dictionaries with case_name, docket_id, document_id, url
    """
    print(f"  🔧 TOOL: search_courtlistener_api({query_params})")
    time.sleep(0.3)
    
    # Dummy response
    return [
        {
            "case_name": "State v. Insurance Company",
            "docket_id": "2024-CL-001",
            "document_id": "doc-12345",
            "url": "https://courtlistener.com/case/12345"
        }
    ]


@tool
def scrape_document_page(doc_url: str) -> Dict[str, Any]:
    """
    Scrape CourtListener document page to extract content.
    
    Args:
        doc_url: URL of the document page
    
    Returns:
        Dictionary with title, description, content, and pdf_url
    """
    print(f"  🔧 TOOL: scrape_document_page(doc_url='{doc_url}')")
    time.sleep(0.4)
    
    # Dummy response
    return {
        "title": "State v. Insurance Company",
        "description": "Court case 2024-CL-001 filed on 2024-01-15",
        "content": "This is dummy pre-scraped content from the court document. It contains information about insurance regulations and legal precedents that may impact the industry.",
        "pdf_url": "https://courtlistener.com/pdf/12345.pdf"
    }

