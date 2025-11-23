"""
Risk analysis API routes
"""
from fastapi import APIRouter, HTTPException
from time import time

from app.models.trademark import SearchQuery
from app.models.risk import (
    AnalysisResponse,
    TrademarkRiskAnalysis,
    RiskTierResults,
    SearchResultsSummary,
    RiskLevel
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
            # No results found - return empty response instead of 404
            processing_time = time() - start_time
            return AnalysisResponse(
                query=query.query,
                summary=SearchResultsSummary(
                    query=query.query,
                    total_results=0,
                    overall_risk_level=RiskLevel.LOW,
                    risk_distribution={"critical": 0, "high": 0, "medium": 0, "low": 0},
                    key_findings=[],
                    recommendations=[
                        "No existing trademarks found matching your search",
                        "This is a positive sign for trademark clearance",
                        "Consider conducting a comprehensive trademark search through an attorney"
                    ],
                    summary="No trademarks were found matching your search query in the USPTO database. While this is encouraging, it's recommended to conduct a comprehensive trademark search before proceeding.",
                    suggested_next_steps=[
                        "Consult with a trademark attorney for comprehensive clearance",
                        "Consider searching for phonetically similar marks",
                        "Evaluate potential common law trademark conflicts"
                    ]
                ),
                results_by_tier=RiskTierResults(),
                total_analyzed=0,
                processing_time_seconds=round(processing_time, 2)
            )

        # Step 1.5: Enrich trademark data with TSDR API for accurate owner/class info
        print(f"\n📡 Enriching {len(trademarks)} trademarks with TSDR data...")
        for i, trademark in enumerate(trademarks, 1):
            try:
                # Fetch full data from USPTO TSDR API using serial number
                tsdr_data = await uspto_client.get_trademark_by_serial(trademark.serial_number)

                if tsdr_data:
                    # Update with accurate owner name and classes from official source
                    if tsdr_data.owner_name:
                        trademark.owner_name = tsdr_data.owner_name
                        print(f"  [{i}/{len(trademarks)}] ✅ {trademark.serial_number}: Owner = {tsdr_data.owner_name}")

                    if tsdr_data.international_classes:
                        trademark.international_classes = tsdr_data.international_classes

                    # Include goods/services description from TSDR
                    if tsdr_data.goods_services_description:
                        trademark.goods_services_description = tsdr_data.goods_services_description
                else:
                    print(f"  [{i}/{len(trademarks)}] ⚠️  {trademark.serial_number}: TSDR data not available")
            except Exception as e:
                print(f"  [{i}/{len(trademarks)}] ❌ {trademark.serial_number}: Error fetching TSDR data: {e}")
                # Continue with RapidAPI data if TSDR fails

        # Step 2: Calculate risk scores
        risk_scorer = RiskScorer()
        risk_analyses = []

        for trademark in trademarks:
            risk_score, risk_factors = risk_scorer.calculate_risk_score(
                query=query.query,
                trademark=trademark,
                query_classes=query.classes or []
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
                owner_name=trademark.owner_name,
                risk_score=risk_score,
                risk_level=risk_level,
                risk_factors=risk_factors,
                risk_explanation=conflict_reason,
                conflict_reason=conflict_reason,
                recommendations=_generate_recommendations(risk_level, trademark),
                goods_services_description=trademark.goods_services_description,
                international_classes=trademark.international_classes,
                status=trademark.status,
                filing_date=trademark.filing_date,
                registration_date=trademark.registration_date
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
