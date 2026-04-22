from __future__ import annotations

import re
from typing import Dict, List

from app.services.nlp_service import NLPService


CLAUSE_KEYWORDS: Dict[str, List[str]] = {
    "termination": [
        "terminate",
        "termination",
        "cancel",
    ],
    "payment": [
        "pay",
        "payment",
        "invoice",
        "amount",
    ],
    "liability": [
        "liable",
        "liability",
        "damages",
    ],
}

RISK_PHRASES: List[str] = [
    "unlimited liability",
    "no termination",
    "penalty",
]

DATE_NOISE_TERMS = {
    "day",
    "days",
    "month",
    "months",
    "year",
    "years",
    "weekly",
    "monthly",
    "daily",
    "annually",
    "first",
}

ORG_HINTS = (
    "bank",
    "corp",
    "corporation",
    "company",
    "limited",
    "ltd",
    "llc",
    "inc",
    "office",
    "authority",
    "contractor",
)


def _normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _get_sentences(text: str) -> List[str]:
    cleaned = _normalize_text(text)
    if not cleaned:
        return []
    return NLPService.segment_sentences(cleaned)


def _normalize_inline_whitespace(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,;")


def _keyword_present(sentence_lower: str, keyword: str) -> bool:
    escaped = re.escape(keyword.lower()).replace(r"\ ", r"\s+")
    pattern = rf"\b{escaped}\b"
    return re.search(pattern, sentence_lower) is not None


def _clean_entity(entity_text: str, entity_label: str) -> Dict[str, str] | None:
    text = _normalize_inline_whitespace(entity_text)
    if not text or len(text) < 3:
        return None

    if re.fullmatch(r"[\W_]+", text):
        return None

    lower = text.lower()
    words = lower.split()

    if entity_label == "DATE" and lower in DATE_NOISE_TERMS:
        return None

    if entity_label in {"PERSON", "ORG"} and len(words) > 8:
        return None

    if entity_label == "PERSON" and any(hint in lower for hint in ORG_HINTS):
        entity_label = "ORG"

    # Common OCR/header/footer style noise chunks.
    if entity_label == "ORG" and lower.startswith("the ") and "&" in lower and len(words) > 5:
        return None

    return {"text": text, "label": entity_label}


ENTITY_LABELS = {"PERSON", "ORG", "DATE"}


def extract_entities(text: str) -> List[Dict[str, str]]:
    """
    Extract named entities from text using spaCy.

    Returns:
        List of dictionaries in format: {"text": str, "label": str}
    """
    cleaned = _normalize_text(text)
    if not cleaned:
        return []

    nlp = NLPService.load_model()
    doc = nlp(cleaned)

    entities: List[Dict[str, str]] = []
    seen = set()
    for ent in doc.ents:
        entity_text = ent.text.strip()
        entity_label = ent.label_
        if entity_label not in ENTITY_LABELS or not entity_text:
            continue

        cleaned_entity = _clean_entity(entity_text, entity_label)
        if not cleaned_entity:
            continue

        key = (
            cleaned_entity["text"].lower(),
            cleaned_entity["label"],
        )
        if key not in seen:
            seen.add(key)
            entities.append(cleaned_entity)

    return entities


def detect_clauses(text: str) -> Dict[str, List[Dict[str, object]]]:
    """
    Detect contract clauses using keyword-based matching.

    Returns:
        Structured dictionary keyed by clause type with sentence matches.
    """
    sentences = _get_sentences(text)
    result: Dict[str, List[Dict[str, object]]] = {
        "termination": [],
        "payment": [],
        "liability": [],
    }

    for sentence in sentences:
        normalized_sentence = _normalize_inline_whitespace(sentence)
        sentence_lower = normalized_sentence.lower()
        for clause_type, keywords in CLAUSE_KEYWORDS.items():
            matched = [kw for kw in keywords if _keyword_present(sentence_lower, kw)]
            if matched:
                result[clause_type].append(
                    {
                        "sentence": normalized_sentence,
                        "matched_keywords": matched,
                    }
                )

    return result


def detect_risks(text: str) -> List[str]:
    """
    Detect risky phrases in contract text.

    Returns:
        List of unique risky phrases found in the document.
    """
    cleaned = _normalize_text(text).lower()
    if not cleaned:
        return []

    found_risks: List[str] = []
    for phrase in RISK_PHRASES:
        if phrase in cleaned:
            found_risks.append(phrase)

    return found_risks
