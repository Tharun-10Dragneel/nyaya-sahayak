from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

# Create the router
router = APIRouter(prefix="/api/legal", tags=["legal"])

@router.get("/info")
async def get_legal_info(topic: str, language: str = "english"):
    """Endpoint to get legal information on specific topics"""
    legal_topics = {
        "rights": "Information about fundamental rights in India",
        "fir": "Process to file a First Information Report",
        "rti": "Right to Information application process",
        "bail": "Information about bail procedures",
        "divorce": "Legal process for divorce in India"
    }
    
    if topic.lower() in legal_topics:
        return {
            "topic": topic,
            "language": language,
            "info": legal_topics[topic.lower()]
        }
    
    return {
        "topic": topic,
        "language": language,
        "info": "Information not available for this topic. Please try another topic."
    }

@router.get("/emergency")
async def emergency_services(service_type: Optional[str] = None):
    """Information about emergency legal services"""
    services = {
        "women": "Women Helpline: 181",
        "child": "Child Helpline: 1098",
        "police": "Police Emergency: 112"
    }
    
    if service_type and service_type.lower() in services:
        return {"service": service_type, "contact": services[service_type.lower()]}
    
    return {"available_services": services}

@router.get("/documents/{doc_type}")
async def document_guidance(doc_type: str, language: str = "english"):
    """Get guidance for filing specific legal documents"""
    document_info = {
        "fir": "Steps to file an FIR: 1) Visit local police station, 2) Provide incident details...",
        "rti": "RTI application process: 1) Draft application, 2) Pay fee (₹10), 3) Submit to PIO...",
        "consumer": "Consumer complaint filing: 1) Write formal complaint, 2) Attach proof of purchase..."
    }
    
    if doc_type.lower() in document_info:
        return {
            "document_type": doc_type,
            "language": language,
            "guidance": document_info[doc_type.lower()]
        }
    
    raise HTTPException(status_code=404, detail=f"Document type '{doc_type}' not found")
