from typing import List

from app.models.contract import Clause
from app.services.contract_nlp import detect_clauses as nlp_detect_clauses


class ClauseDetector:
    """
    Detects contract clauses using keyword matching.
    Focuses on: termination, payment, and liability clauses.
    """

    @staticmethod
    def detect_clauses(text: str) -> List[Clause]:
        """
        Detect clauses in contract text using keyword matching.

        Returns list of detected clauses with confidence scores.
        """
        if not text or not text.strip():
            return []

        structured = nlp_detect_clauses(text)
        clauses: List[Clause] = []

        for clause_type, matches in structured.items():
            for match in matches:
                sentence = str(match.get("sentence", "")).strip()
                keywords = match.get("matched_keywords", [])

                if not sentence:
                    continue

                keyword_count = len(keywords) if isinstance(keywords, list) else 0
                confidence = min(0.99, 0.5 + (0.15 * keyword_count))

                clauses.append(
                    Clause(
                        type=clause_type.capitalize(),
                        text=sentence[:300],
                        confidence=round(confidence, 2),
                    )
                )

        # Remove near-duplicates and return top 10 by confidence.
        unique_clauses: List[Clause] = []
        seen = set()
        for clause in clauses:
            key = (clause.type, clause.text[:100])
            if key not in seen:
                seen.add(key)
                unique_clauses.append(clause)

        unique_clauses.sort(key=lambda c: c.confidence, reverse=True)
        return unique_clauses[:10]
