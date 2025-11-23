"""
Risk analysis models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level categories"""
    CRITICAL = "critical"  # 90-100
    HIGH = "high"          # 70-89
    MEDIUM = "medium"      # 40-69
    LOW = "low"            # 0-39


class RiskFactors(BaseModel):
    """Individual risk factor scores"""
    similarity_score: float = Field(..., ge=0, le=100)
    class_overlap_score: float = Field(..., ge=0, le=100)
    status_strength_score: float = Field(..., ge=0, le=100)
    use_commerce_score: float = Field(..., ge=0, le=100)


class TrademarkRiskAnalysis(BaseModel):
    """Risk analysis for a single trademark"""
    serial_number: str
    mark_text: str
    owner_name: str

    # Overall risk
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: RiskLevel

    # Risk factors breakdown
    risk_factors: RiskFactors

    # Explanation
    risk_explanation: str
    conflict_reason: str

    # Recommendations
    recommendations: List[str] = Field(default_factory=list)

    # Optional trademark details (from TSDR API)
    goods_services_description: Optional[str] = None
    international_classes: Optional[List[str]] = None
    status: Optional[str] = None
    filing_date: Optional[str] = None
    registration_date: Optional[str] = None


class SearchResultsSummary(BaseModel):
    """AI-generated summary of all search results"""
    query: str
    total_results: int

    # Overall assessment
    overall_risk_level: RiskLevel
    risk_distribution: dict = Field(
        default_factory=dict,
        description="Count of results in each risk category"
    )

    # Key findings
    key_findings: List[str] = Field(default_factory=list)

    # Recommendations
    recommendations: List[str] = Field(default_factory=list)

    # Summary text
    summary: str

    # Timeline estimate
    estimated_timeline: Optional[str] = None
    suggested_next_steps: List[str] = Field(default_factory=list)


class RiskTierResults(BaseModel):
    """Results organized by risk tier"""
    critical: List[TrademarkRiskAnalysis] = Field(default_factory=list)
    high: List[TrademarkRiskAnalysis] = Field(default_factory=list)
    medium: List[TrademarkRiskAnalysis] = Field(default_factory=list)
    low: List[TrademarkRiskAnalysis] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    query: str
    summary: SearchResultsSummary
    results_by_tier: RiskTierResults
    total_analyzed: int
    processing_time_seconds: float
