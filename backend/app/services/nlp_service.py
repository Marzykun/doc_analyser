import spacy
from typing import List, Dict, Any

class NLPService:
    """NLP service for named entity recognition using spaCy"""
    
    _nlp_model = None
    
    @classmethod
    def load_model(cls, model_name: str = "en_core_web_sm"):
        """Load spaCy model (lazy loading)"""
        if cls._nlp_model is None:
            try:
                cls._nlp_model = spacy.load(model_name)
            except OSError:
                raise RuntimeError(
                    f"spaCy model '{model_name}' not found. "
                    f"Download it with: python -m spacy download {model_name}"
                )
        return cls._nlp_model
    
    @classmethod
    def extract_entities(cls, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from text using spaCy.
        
        Returns entities with types: PERSON, ORG, DATE, etc.
        """
        nlp = cls.load_model()
        doc = nlp(text)
        
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "DATE", "GPE", "MONEY", "PRODUCT"]:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
        
        return entities
    
    @classmethod
    def extract_by_type(cls, text: str) -> Dict[str, List[str]]:
        """Extract entities grouped by type"""
        entities = cls.extract_entities(text)
        
        grouped = {
            "PERSON": [],
            "ORG": [],
            "DATE": [],
            "GPE": [],
            "MONEY": [],
            "PRODUCT": []
        }
        
        seen = set()  # Avoid duplicates
        for ent in entities:
            key = (ent["label"], ent["text"])
            if key not in seen:
                seen.add(key)
                if ent["label"] in grouped:
                    grouped[ent["label"]].append(ent["text"])
        
        # Return only non-empty categories
        return {k: v for k, v in grouped.items() if v}

    @classmethod
    def segment_sentences(cls, text: str) -> List[str]:
        """Split text into sentences using spaCy sentence segmentation."""
        if not text or not text.strip():
            return []

        nlp = cls.load_model()
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents if sent.text.strip()]
