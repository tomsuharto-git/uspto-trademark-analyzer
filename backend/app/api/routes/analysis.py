"""
Risk analysis API routes
"""
from fastapi import APIRouter, HTTPException
from time import time

from app.models.trademark import SearchQuery
from app.models.risk import (
    AnalysisResponse,
    TrademarkRiskAnalysis,
    RiskTierResults
)
from app.services.uspto import USPTOClient
from app.services.risk_scorer import RiskScorer
from app.services.ai_analyzer import AIAnalyzer

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_trademark(query: SearchQuery):
    """
    Comprehensive trademark risk analysis

    This endpoint:
    1. Searches USPTO database
    2. Calculates risk scores for each result
    3. Generates AI-powered summary and recommendations
    4. Returns results tiered by risk level

    Args:
        query: SearchQuery with trademark to analyze

    Returns:
        AnalysisResponse with AI summary and risk-tiered results
    """
    start_time = time()

    try:
        # Step 1: Search USPTO database
        uspto_client = USPTOClient()
        trademarks = await uspto_client.search_trademarks(
            query=query.query,
            limit=query.limit
        )

        if not trademarks:
            # No results found
            raise HTTPException(
                status_code=404,
                detail="No trademarks found matching your search"
            )

        # Step 2: Calculate risk scores
        risk_scorer = RiskScorer()
        risk_analyses = []

        for trademark in trademarks:
            risk_score, risk_factors = risk_scorer.calculate_risk_score(
                query=query.query,
                trademark=trademark
            )

            risk_level = risk_scorer.get_risk_level(risk_score)
            conflict_reason = risk_scorer.get_conflict_reason(
                query=query.query,
                trademark=trademark,
                risk_factors=risk_factors
            )

            risk_analysis = TrademarkRiskAnalysis(
                serial_number=trademark.serial_number,
                mark_text=trademark.mark_text,
                risk_score=risk_score,
                risk_level=risk_level,
                risk_factors=risk_factors,
                risk_explanation=conflict_reason,
                conflict_reason=conflict_reason,
                recommendations=_generate_recommendations(risk_level, trademark)
            )

            risk_analyses.append(risk_analysis)

        # Step 3: Organize by risk tier
        results_by_tier = RiskTierResults(
            critical=[r for r in risk_analyses if r.risk_level.value == "critical"],
            high=[r for r in risk_analyses if r.risk_level.value == "high"],
            medium=[r for r in risk_analyses if r.risk_level.value == "medium"],
            low=[r for r in risk_analyses if r.risk_level.value == "low"]
        )

        # Step 4: Generate AI summary
        ai_analyzer = AIAnalyzer()
        summary = await ai_analyzer.generate_summary(
            query=query.query,
            risk_analyses=risk_analyses
        )

        processing_time = time() - start_time

        return AnalysisResponse(
            query=query.query,
            summary=summary,
            results_by_tier=results_by_tier,
            total_analyzed=len(risk_analyses),
            processing_time_seconds=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing trademark: {str(e)}"
        )


def _generate_recommendations(risk_level, trademark) -> list[str]:
    """Generate specific recommendations based on risk level"""

    if risk_level.value == "critical":
        return [
            "Do not proceed without legal consultation",
            "Consider alternative brand names",
            f"Review {trademark.owner_name}'s trademark portfolio"
        ]
    elif risk_level.value == "high":
        return [
            "Consult trademark attorney before proceeding",
            "Conduct comprehensive clearance search",
            "Evaluate name modifications or alternatives"
        ]
    elif risk_level.value == "medium":
        return [
            "Monitor this trademark's status",
            "Consider filing in different international classes",
            "Document your independent creation and use"
        ]
    else:
        return [
            "Note this mark for awareness",
            "Proceed with standard clearance process"
        ]
