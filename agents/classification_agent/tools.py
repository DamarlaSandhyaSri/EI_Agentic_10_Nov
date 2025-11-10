"""Classification Agent Tools - Using @tool decorator"""
from langchain_core.tools import tool
from typing import Dict, Any
import time


@tool
def classify_content(content: str) -> Dict[str, Any]:
    """
    Classify content using LLM to extract tags, risks, and NAICS codes.
    
    Args:
        content: Text content to classify
    
    Returns:
        Dictionary with classification results (tag, risks, naics, etc.)
    """
    print(f"  🔧 TOOL: classify_content(content_length={len(content)})")
    print(f"      🤖 [DUMMY LLM CALL] Classifying content...")
    time.sleep(0.5)
    
    # Dummy classification
    return {
        "tag": "Current",
        "risks": ["Climate Risk", "Regulatory Compliance"],
        "naics_codes": ["524126", "524113"],
        "summary": "Article discusses insurance regulations related to climate risk."
    }

