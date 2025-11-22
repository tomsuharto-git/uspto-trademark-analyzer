"""
Data models for USPTO trademark information
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum


class TrademarkStatus(str, Enum):
    """Trademark status categories"""
    REGISTERED = "registered"
    PENDING = "pending"
    ABANDONED = "abandoned"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    UNKNOWN = "unknown"


class Trademark(BaseModel):
    """USPTO Trademark information"""
    serial_number: str
    registration_number: Optional[str] = None
    mark_text: str
    owner_name: str
    status: TrademarkStatus
    status_date: Optional[date] = None
    filing_date: Optional[date] = None
    registration_date: Optional[date] = None

    # Classification
    international_classes: List[str] = Field(default_factory=list)
    goods_services_description: Optional[str] = None

    # Additional info
    mark_type: Optional[str] = None  # "word", "design", "composite"
    attorney_name: Optional[str] = None
    correspondence_address: Optional[str] = None

    # For image marks
    mark_image_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "serial_number": "88234567",
                "registration_number": "5678901",
                "mark_text": "ACME WIDGETS",
                "owner_name": "Acme Corporation",
                "status": "registered",
                "filing_date": "2020-01-15",
                "registration_date": "2021-06-30",
                "international_classes": ["009", "035"],
                "goods_services_description": "Computer software; retail services"
            }
        }


class SearchQuery(BaseModel):
    """Search query from user"""
    query: str = Field(..., min_length=1, max_length=200)
    search_type: str = Field(default="text", pattern="^(text|serial|owner)$")
    limit: int = Field(default=50, ge=1, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "ACME",
                "search_type": "text",
                "limit": 50
            }
        }
