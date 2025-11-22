"""
AI-powered trademark risk analysis using Claude
"""
from typing import List
import anthropic
import json

from app.config import settings
from app.models.trademark import Trademark
from app.models.risk import (
    TrademarkRiskAnalysis,
    SearchResultsSummary,
    RiskLevel,
    RiskTierResults
)


class AIAnalyzer:
    """AI-powered risk analysis using Claude"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = settings.CLAUDE_MODEL

    async def generate_summary(
        self,
        query: str,
        risk_analyses: List[TrademarkRiskAnalysis]
    ) -> SearchResultsSummary:
        """
        Generate TL;DR summary of all search results with recommendations

        Args:
            query: Original search query
            risk_analyses: List of all risk analyses

        Returns:
            SearchResultsSummary with AI-generated insights
        """
        # Calculate risk distribution
        risk_distribution = {
            "critical": sum(1 for r in risk_analyses if r.risk_level == RiskLevel.CRITICAL),
            "high": sum(1 for r in risk_analyses if r.risk_level == RiskLevel.HIGH),
            "medium": sum(1 for r in risk_analyses if r.risk_level == RiskLevel.MEDIUM),
            "low": sum(1 for r in risk_analyses if r.risk_level == RiskLevel.LOW),
        }

        # Determine overall risk level
        if risk_distribution["critical"] > 0:
            overall_risk = RiskLevel.CRITICAL
        elif risk_distribution["high"] >= 2:
            overall_risk = RiskLevel.HIGH
        elif risk_distribution["high"] >= 1 or risk_distribution["medium"] >= 3:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.LOW

        # Prepare context for Claude
        context = self._prepare_summary_context(query, risk_analyses, risk_distribution)

        # Generate AI summary
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": context
                }]
            )

            response_text = message.content[0].text

            # Parse Claude's response
            summary_data = self._parse_summary_response(response_text)

            return SearchResultsSummary(
                query=query,
                total_results=len(risk_analyses),
                overall_risk_level=overall_risk,
                risk_distribution=risk_distribution,
                key_findings=summary_data.get("key_findings", []),
                recommendations=summary_data.get("recommendations", []),
                summary=summary_data.get("summary", ""),
                estimated_timeline=summary_data.get("timeline"),
                suggested_next_steps=summary_data.get("next_steps", [])
            )

        except Exception as e:
            print(f"Error generating AI summary: {e}")
            # Fallback to basic summary
            return self._generate_fallback_summary(
                query, risk_analyses, overall_risk, risk_distribution
            )

    def _prepare_summary_context(
        self,
        query: str,
        risk_analyses: List[TrademarkRiskAnalysis],
        risk_distribution: dict
    ) -> str:
        """Prepare context for Claude to generate summary"""

        # Get top 5 highest risk items
        top_risks = sorted(risk_analyses, key=lambda x: x.risk_score, reverse=True)[:5]

        context = f"""You are a trademark attorney analyzing search results for potential conflicts.

SEARCH QUERY: "{query}"

RESULTS OVERVIEW:
- Total trademarks found: {len(risk_analyses)}
- Critical risk: {risk_distribution['critical']}
- High risk: {risk_distribution['high']}
- Medium risk: {risk_distribution['medium']}
- Low risk: {risk_distribution['low']}

TOP RISK ITEMS:
"""

        for i, risk in enumerate(top_risks, 1):
            context += f"\n{i}. {risk.mark_text} (Risk: {risk.risk_score:.0f}/100 - {risk.risk_level.upper()})"
            context += f"\n   Reason: {risk.conflict_reason}\n"

        context += """
Generate a concise analysis in JSON format with:

{
  "summary": "2-3 sentence overview of the trademark landscape and overall risk",
  "key_findings": ["finding 1", "finding 2", "finding 3"],
  "recommendations": ["actionable recommendation 1", "recommendation 2", "recommendation 3"],
  "timeline": "estimated timeline for next steps (e.g., '2-4 weeks for initial clearance')",
  "next_steps": ["specific next step 1", "step 2", "step 3"]
}

Be direct, professional, and action-oriented. Focus on what the user should do."""

        return context

    def _parse_summary_response(self, response_text: str) -> dict:
        """Parse Claude's JSON response"""
        try:
            # Extract JSON from response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except:
            pass

        return {
            "summary": response_text,
            "key_findings": [],
            "recommendations": [],
            "next_steps": []
        }

    def _generate_fallback_summary(
        self,
        query: str,
        risk_analyses: List[TrademarkRiskAnalysis],
        overall_risk: RiskLevel,
        risk_distribution: dict
    ) -> SearchResultsSummary:
        """Generate basic summary if AI fails"""

        if overall_risk == RiskLevel.CRITICAL:
            summary = f"Found {risk_distribution['critical']} critical conflicts for '{query}'. Immediate legal review recommended."
            recommendations = [
                "Consult a trademark attorney immediately",
                "Consider alternative brand names",
                "Do not proceed without legal clearance"
            ]
        elif overall_risk == RiskLevel.HIGH:
            summary = f"Found {risk_distribution['high']} high-risk conflicts for '{query}'. Professional review strongly advised."
            recommendations = [
                "Conduct comprehensive trademark search",
                "Consult with trademark attorney",
                "Evaluate alternative names or modifications"
            ]
        elif overall_risk == RiskLevel.MEDIUM:
            summary = f"Found some potential conflicts for '{query}'. Further analysis recommended."
            recommendations = [
                "Review similar marks in detail",
                "Consider filing in different classes",
                "Consult attorney for risk assessment"
            ]
        else:
            summary = f"No significant conflicts found for '{query}'. Preliminary clearance looks favorable."
            recommendations = [
                "Proceed with comprehensive search",
                "Consider trademark registration",
                "Monitor for new applications"
            ]

        return SearchResultsSummary(
            query=query,
            total_results=len(risk_analyses),
            overall_risk_level=overall_risk,
            risk_distribution=risk_distribution,
            key_findings=[f"Analyzed {len(risk_analyses)} existing trademarks"],
            recommendations=recommendations,
            summary=summary,
            suggested_next_steps=["Contact trademark attorney", "Conduct full search"]
        )

    async def enhance_risk_explanation(
        self,
        risk_analysis: TrademarkRiskAnalysis,
        query: str
    ) -> str:
        """
        Use Claude to generate detailed risk explanation for a single trademark

        Args:
            risk_analysis: The risk analysis to enhance
            query: Original search query

        Returns:
            Enhanced explanation string
        """
        try:
            prompt = f"""Briefly explain why the trademark "{risk_analysis.mark_text}" poses a {risk_analysis.risk_level.upper()} risk to the proposed mark "{query}".

Risk Score: {risk_analysis.risk_score:.0f}/100
Conflict: {risk_analysis.conflict_reason}

Provide a 1-2 sentence explanation focusing on the specific conflict issues."""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return message.content[0].text.strip()

        except Exception as e:
            print(f"Error enhancing explanation: {e}")
            return risk_analysis.risk_explanation
