from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pathlib import Path
from app.models.contract import AnalysisResponse
from app.services import FileHandler, TextExtractor, ClauseDetector, EntityExtractor
from app.config import get_settings

router = APIRouter(tags=["contracts"])
settings = get_settings()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_contract(file: UploadFile = File(...)):
    """
    Analyze a contract PDF file.
    
    - **file**: PDF file to analyze
    
    Returns: JSON with extracted clauses and entities
    - clauses: List of detected clauses (termination, payment, liability, etc.)
    - entities: Named entities (PERSON, ORG, DATE, MONEY)
    """
    file_handler = FileHandler()
    
    # Validate file extension
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Validate file size (max 10MB)
    if file.size and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds maximum allowed (10MB)"
        )
    
    file_path = None
    try:
        # Save uploaded file
        file_path = await file_handler.save_upload(file)
        
        # Extract text from PDF
        text = TextExtractor.extract_text(file_path)
        
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from PDF"
            )
        
        # Detect clauses using keyword matching
        clauses = ClauseDetector.detect_clauses(text)
        
        # Extract named entities using spaCy
        entities = EntityExtractor.extract_entities(text)
        
        return AnalysisResponse(
            text=text,
            clauses=clauses,
            entities=entities
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error processing file"
        )
    finally:
        # Cleanup: delete temporary file
        if file_path:
            FileHandler.delete_file(file_path)

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Contract Analyzer"}
