"""
Risk scoring logic for trademark conflict analysis
"""
import Levenshtein
import jellyfish
from typing import List, Set

from app.models.trademark import Trademark, TrademarkStatus
from app.models.risk import RiskLevel, RiskFactors


class RiskScorer:
    """Calculate risk scores for trademark conflicts"""

    # Scoring weights
    SIMILARITY_WEIGHT = 0.40
    CLASS_OVERLAP_WEIGHT = 0.30
    STATUS_STRENGTH_WEIGHT = 0.20
    USE_COMMERCE_WEIGHT = 0.10

    def calculate_risk_score(
        self,
        query: str,
        trademark: Trademark
    ) -> tuple[float, RiskFactors]:
        """
        Calculate overall risk score and individual factor scores

        Args:
            query: The search query (proposed mark)
            trademark: Existing trademark to compare against

        Returns:
            Tuple of (overall_risk_score, RiskFactors)
        """
        # Calculate individual factor scores
        similarity_score = self.calculate_similarity_score(query, trademark.mark_text)
        class_overlap_score = self.calculate_class_overlap_score([], trademark.international_classes)
        status_strength_score = self.calculate_status_strength_score(trademark)
        use_commerce_score = self.calculate_use_commerce_score(trademark)

        # Calculate weighted overall score
        overall_score = (
            similarity_score * self.SIMILARITY_WEIGHT +
            class_overlap_score * self.CLASS_OVERLAP_WEIGHT +
            status_strength_score * self.STATUS_STRENGTH_WEIGHT +
            use_commerce_score * self.USE_COMMERCE_WEIGHT
        )

        risk_factors = RiskFactors(
            similarity_score=similarity_score,
            class_overlap_score=class_overlap_score,
            status_strength_score=status_strength_score,
            use_commerce_score=use_commerce_score
        )

        return overall_score, risk_factors

    def calculate_similarity_score(self, query: str, mark_text: str) -> float:
        """
        Calculate text similarity score (0-100)

        Uses multiple algorithms:
        - Levenshtein distance (edit distance)
        - Soundex (phonetic similarity)
        - Metaphone (phonetic similarity)
        """
        query = query.upper().strip()
        mark_text = mark_text.upper().strip()

        # Exact match
        if query == mark_text:
            return 100.0

        # Levenshtein similarity (normalized)
        lev_distance = Levenshtein.distance(query, mark_text)
        max_len = max(len(query), len(mark_text))
        lev_similarity = (1 - lev_distance / max_len) * 100 if max_len > 0 else 0

        # Phonetic similarity (Soundex)
        soundex_match = jellyfish.soundex(query) == jellyfish.soundex(mark_text)
        soundex_score = 80.0 if soundex_match else 0.0

        # Phonetic similarity (Metaphone)
        metaphone_match = jellyfish.metaphone(query) == jellyfish.metaphone(mark_text)
        metaphone_score = 80.0 if metaphone_match else 0.0

        # Check if one contains the other
        contains_score = 0.0
        if query in mark_text or mark_text in query:
            contains_score = 70.0

        # Take the maximum score from all methods
        similarity_score = max(
            lev_similarity,
            soundex_score,
            metaphone_score,
            contains_score
        )

        return min(similarity_score, 100.0)

    def calculate_class_overlap_score(
        self,
        query_classes: List[str],
        mark_classes: List[str]
    ) -> float:
        """
        Calculate international class overlap score (0-100)

        For MVP, we'll assume query doesn't specify classes yet
        In production, user would input their intended class(es)
        """
        if not mark_classes:
            return 0.0

        # For MVP: assume medium risk since we don't know query's classes
        # In production, calculate actual overlap
        # Same class = 100
        # Related classes = 60
        # Different classes = 20

        return 50.0  # Medium default for MVP

    def calculate_status_strength_score(self, trademark: Trademark) -> float:
        """
        Calculate score based on trademark status and strength (0-100)
        """
        status_scores = {
            TrademarkStatus.REGISTERED: 100.0,  # Highest risk
            TrademarkStatus.PENDING: 70.0,      # Medium-high risk
            TrademarkStatus.ABANDONED: 20.0,    # Low risk
            TrademarkStatus.CANCELLED: 20.0,    # Low risk
            TrademarkStatus.EXPIRED: 30.0,      # Low-medium risk
            TrademarkStatus.UNKNOWN: 50.0,      # Medium default
        }

        return status_scores.get(trademark.status, 50.0)

    def calculate_use_commerce_score(self, trademark: Trademark) -> float:
        """
        Calculate score based on use in commerce (0-100)

        For MVP, we use status as proxy
        In production, consider:
        - Years in use
        - Geographic scope
        - Market presence
        - Famous mark status
        """
        if trademark.status == TrademarkStatus.REGISTERED:
            return 80.0
        elif trademark.status == TrademarkStatus.PENDING:
            return 50.0
        else:
            return 20.0

    def get_risk_level(self, risk_score: float) -> RiskLevel:
        """Convert numeric risk score to RiskLevel enum"""
        if risk_score >= 90:
            return RiskLevel.CRITICAL
        elif risk_score >= 70:
            return RiskLevel.HIGH
        elif risk_score >= 40:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def get_conflict_reason(
        self,
        query: str,
        trademark: Trademark,
        risk_factors: RiskFactors
    ) -> str:
        """Generate human-readable explanation of conflict risk"""
        reasons = []

        # Similarity
        if risk_factors.similarity_score >= 80:
            reasons.append(f"Very similar to '{trademark.mark_text}'")
        elif risk_factors.similarity_score >= 60:
            reasons.append(f"Similar to '{trademark.mark_text}'")

        # Status
        if trademark.status == TrademarkStatus.REGISTERED:
            reasons.append("Active registered trademark")
        elif trademark.status == TrademarkStatus.PENDING:
            reasons.append("Pending application")

        # Classes
        if risk_factors.class_overlap_score >= 80:
            reasons.append(f"Same product/service class ({', '.join(trademark.international_classes)})")

        if not reasons:
            reasons.append("Potential similarity detected")

        return "; ".join(reasons)
