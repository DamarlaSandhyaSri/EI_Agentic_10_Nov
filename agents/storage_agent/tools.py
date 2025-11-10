"""Storage Agent Tools - Using @tool decorator"""
from langchain_core.tools import tool
from typing import Dict, Any
import time


@tool
def save_to_s3(bucket: str, key: str, data: Dict[str, Any]) -> bool:
    """
    Save data to S3 bucket.
    
    Args:
        bucket: S3 bucket name
        key: S3 object key  
        data: Data dictionary to save
    
    Returns:
        True if successful, False otherwise
    """
    print(f"  🔧 TOOL: save_to_s3(bucket='{bucket}', key='{key}')")
    print(f"      💾 [DUMMY S3 WRITE] Saving to S3...")
    time.sleep(0.3)
    
    # Dummy save
    return True

