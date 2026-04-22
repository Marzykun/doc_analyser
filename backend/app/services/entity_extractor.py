from app.models.contract import Entity
from app.services.contract_nlp import extract_entities as nlp_extract_entities

class EntityExtractor:
    """Extracts entities from contract text using spaCy NLP"""
    
    @staticmethod
    def extract_entities(text: str) -> Entity:
        """
        Extract named entities from contract text using spaCy.
        
        Returns Entity object populated from PERSON, ORG, and DATE entities.
        """
        try:
            entities = nlp_extract_entities(text)

            names = []
            dates = []
            amounts = []

            for entity in entities:
                value = entity.get("text", "")
                label = entity.get("label", "")
                if label in {"PERSON", "ORG"}:
                    names.append(value)
                elif label == "DATE":
                    dates.append(value)

            # Keep output stable and deduplicated.
            names = list(dict.fromkeys(names))
            dates = list(dict.fromkeys(dates))
            amounts = list(dict.fromkeys(amounts))
            
            return Entity(
                names=names,
                dates=dates,
                amounts=amounts,
            )
        except Exception as e:
            # Fallback: return empty entities if NLP fails
            print(f"Warning: NLP extraction failed: {str(e)}")
            return Entity(names=[], dates=[], amounts=[])
