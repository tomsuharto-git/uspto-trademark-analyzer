"""
Risk scoring logic for trademark conflict analysis
"""
from typing import List, Set

# Optional dependencies for advanced similarity matching
try:
    import Levenshtein
    HAS_LEVENSHTEIN = True
except ImportError:
    HAS_LEVENSHTEIN = False

try:
    import jellyfish
    HAS_JELLYFISH = True
except ImportError:
    HAS_JELLYFISH = False

from app.models.trademark import Trademark, TrademarkStatus
from app.models.risk import RiskLevel, RiskFactors


class RiskScorer:
    """Calculate risk scores for trademark conflicts"""

    # Scoring weights
    SIMILARITY_WEIGHT = 0.40
    CLASS_OVERLAP_WEIGHT = 0.30
    STATUS_STRENGTH_WEIGHT = 0.20
    USE_COMMERCE_WEIGHT = 0.10

    # Famous/well-known marks that should automatically be CRITICAL
    FAMOUS_MARKS = {
        # Tech
        "APPLE", "THINK DIFFERENT", "GOOGLE", "MICROSOFT", "AMAZON", "FACEBOOK",
        "META", "INSTAGRAM", "YOUTUBE", "TWITTER", "X", "TESLA", "NETFLIX",
        "UBER", "AIRBNB",

        # Sports/Apparel
        "NIKE", "JUST DO IT", "ADIDAS", "PUMA", "UNDER ARMOUR", "REEBOK",

        # Food/Beverage
        "COCA-COLA", "COKE", "PEPSI", "MCDONALD'S", "I'M LOVIN' IT", "STARBUCKS",
        "BURGER KING", "KFC", "SUBWAY", "WENDY'S", "RED BULL",

        # Automotive
        "FORD", "TOYOTA", "HONDA", "BMW", "MERCEDES", "MERCEDES-BENZ", "FERRARI",
        "PORSCHE", "CHEVROLET", "DODGE",

        # Luxury/Fashion
        "GUCCI", "LOUIS VUITTON", "CHANEL", "PRADA", "ROLEX", "CARTIER",

        # Retail/General
        "WALMART", "TARGET", "COSTCO", "HOME DEPOT", "IKEA", "VISA",
        "MASTERCARD", "AMERICAN EXPRESS", "PAYPAL"
    }

    def is_famous_mark(self, mark_text: str) -> bool:
        """Check if a trademark is in the famous marks list"""
        normalized_mark = mark_text.upper().strip()
        return normalized_mark in self.FAMOUS_MARKS

    def calculate_risk_score(
        self,
        query: str,
        trademark: Trademark,
        query_classes: List[str] = []
    ) -> tuple[float, RiskFactors]:
        """
        Calculate overall risk score and individual factor scores

        Args:
            query: The search query (proposed mark)
            trademark: Existing trademark to compare against
            query_classes: User's intended international classes

        Returns:
            Tuple of (overall_risk_score, RiskFactors)
        """
        # Calculate individual factor scores
        similarity_score = self.calculate_similarity_score(query, trademark.mark_text)
        class_overlap_score = self.calculate_class_overlap_score(
            query_classes,
            trademark.international_classes,
            similarity_score=similarity_score
        )
        status_strength_score = self.calculate_status_strength_score(trademark)
        use_commerce_score = self.calculate_use_commerce_score(trademark)

        # Calculate weighted overall score
        overall_score = (
            similarity_score * self.SIMILARITY_WEIGHT +
            class_overlap_score * self.CLASS_OVERLAP_WEIGHT +
            status_strength_score * self.STATUS_STRENGTH_WEIGHT +
            use_commerce_score * self.USE_COMMERCE_WEIGHT
        )

        # Famous mark detection - elevate to CRITICAL if:
        # 1. The trademark is famous AND
        # 2. Similarity is high (80+) AND
        # 3. The mark is registered/active
        if (self.is_famous_mark(trademark.mark_text) and
            similarity_score >= 80 and
            trademark.status == TrademarkStatus.REGISTERED):
            print(f"   ⚠️  FAMOUS MARK DETECTED: '{trademark.mark_text}' - Auto-elevating to CRITICAL")
            overall_score = max(overall_score, 95.0)  # Elevate to CRITICAL

        # Debug logging
        print(f"\n🎯 Risk Score Calculation for '{trademark.mark_text}' vs '{query}':")
        print(f"   Similarity: {similarity_score:.1f}/100 (weight: {self.SIMILARITY_WEIGHT}) = {similarity_score * self.SIMILARITY_WEIGHT:.1f}")
        print(f"   Class Overlap: {class_overlap_score:.1f}/100 (weight: {self.CLASS_OVERLAP_WEIGHT}) = {class_overlap_score * self.CLASS_OVERLAP_WEIGHT:.1f}")
        print(f"   Status/Strength: {status_strength_score:.1f}/100 (weight: {self.STATUS_STRENGTH_WEIGHT}) = {status_strength_score * self.STATUS_STRENGTH_WEIGHT:.1f}")
        print(f"   Use in Commerce: {use_commerce_score:.1f}/100 (weight: {self.USE_COMMERCE_WEIGHT}) = {use_commerce_score * self.USE_COMMERCE_WEIGHT:.1f}")
        print(f"   Overall Score: {overall_score:.1f}/100 → Risk Level: {self.get_risk_level(overall_score).value.upper()}")
        print(f"   Trademark Status: {trademark.status.value}")
        print(f"   Trademark Classes: {trademark.international_classes}")
        print(f"   Query Classes: {query_classes or 'None specified'}")

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
        - Levenshtein distance (edit distance) - if available
        - Soundex (phonetic similarity) - if available
        - Metaphone (phonetic similarity) - if available
        - Basic string comparison (fallback)
        """
        query = query.upper().strip()
        mark_text = mark_text.upper().strip()

        # Exact match
        if query == mark_text:
            return 100.0

        scores = []

        # Levenshtein similarity (normalized)
        if HAS_LEVENSHTEIN:
            lev_distance = Levenshtein.distance(query, mark_text)
            max_len = max(len(query), len(mark_text))
            lev_similarity = (1 - lev_distance / max_len) * 100 if max_len > 0 else 0
            scores.append(lev_similarity)
        else:
            # Fallback: simple character-based similarity
            max_len = max(len(query), len(mark_text))
            if max_len > 0:
                matching_chars = sum(1 for a, b in zip(query, mark_text) if a == b)
                simple_similarity = (matching_chars / max_len) * 100
                scores.append(simple_similarity)

        # Phonetic similarity (Soundex)
        if HAS_JELLYFISH:
            soundex_match = jellyfish.soundex(query) == jellyfish.soundex(mark_text)
            soundex_score = 80.0 if soundex_match else 0.0
            scores.append(soundex_score)

            # Phonetic similarity (Metaphone)
            metaphone_match = jellyfish.metaphone(query) == jellyfish.metaphone(mark_text)
            metaphone_score = 80.0 if metaphone_match else 0.0
            scores.append(metaphone_score)

        # Check if one contains the other
        contains_score = 0.0
        if query in mark_text or mark_text in query:
            contains_score = 70.0
        scores.append(contains_score)

        # Take the maximum score from all methods
        similarity_score = max(scores) if scores else 0.0

        return min(similarity_score, 100.0)

    def calculate_class_overlap_score(
        self,
        query_classes: List[str],
        mark_classes: List[str],
        similarity_score: float = 0.0
    ) -> float:
        """
        Calculate international class overlap score (0-100)

        When user specifies classes: calculate actual overlap
        When no classes specified: infer risk based on similarity
        When mark classes missing: assume high risk for exact/similar matches (conservative)
        """
        # If mark classes are missing but similarity is high, assume high class overlap risk
        # Conservative approach: warn users when we don't have complete data
        if not mark_classes:
            if similarity_score >= 95:  # Exact or near-exact match
                return 85.0  # Assume high likelihood of class conflict
            elif similarity_score >= 80:  # Very similar
                return 70.0
            elif similarity_score >= 60:  # Similar
                return 55.0
            else:  # Different marks
                return 30.0  # Lower but still notable risk when data missing

        # If user specified classes, calculate actual overlap
        if query_classes:
            # Normalize class numbers (pad to 3 digits)
            normalized_query = {c.zfill(3) for c in query_classes}
            normalized_mark = {c.zfill(3) for c in mark_classes}

            # Calculate overlap
            overlap = normalized_query & normalized_mark

            if overlap:
                # Same class = 100% risk
                overlap_ratio = len(overlap) / len(normalized_query)
                return min(100.0, 80.0 + (overlap_ratio * 20.0))
            else:
                # Different classes = lower risk
                # But still some risk for highly similar marks
                if similarity_score >= 95:
                    return 40.0  # Exact match in different classes = medium risk
                elif similarity_score >= 80:
                    return 25.0
                else:
                    return 10.0  # Different marks, different classes = low risk

        # When user hasn't specified classes, infer risk based on similarity
        # High similarity = assume high class overlap risk (conservative approach)
        if similarity_score >= 95:  # Exact or near-exact match
            return 90.0  # Assume very high likelihood of class conflict
        elif similarity_score >= 80:  # Very similar
            return 75.0
        elif similarity_score >= 60:  # Similar
            return 60.0
        else:  # Somewhat similar or different
            return 40.0  # Lower but still notable risk

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
