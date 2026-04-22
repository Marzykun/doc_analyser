from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.gemini_engine import analyze_contract as gemini_analyze_contract

from app.config import get_settings
from app.services.contract_nlp import detect_clauses, detect_risks, extract_entities
from app.services.file_handler import FileHandler
from app.utils import extract_text

settings = get_settings()

app = FastAPI(
    title="Contract Analyzer API",
    description="Extract clauses and entities from contract PDFs using spaCy NLP",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# ============================================================================
# CORS Configuration
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400
)

# ============================================================================
# Error Handling
# ============================================================================
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Return clean HTTP error responses."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Normalize request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid request payload", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        }
    )

# ============================================================================
# Analysis Endpoint
# ============================================================================
@app.post("/analyze/")
async def analyze_contract_endpoint(file: UploadFile = File(...)):
    """
    Analyze uploaded contract PDF and return clauses, entities, and risks.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    if file.size is not None and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds maximum allowed (10MB)",
        )

    file_handler = FileHandler()
    file_path = None

    try:
        # 1. Receive and save file
        file_path = await file_handler.save_upload(file)

        # 2. Extract text
        text = extract_text(file_path)
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from PDF",
            )

        # 3. Run NLP functions
        entities = extract_entities(text)
        clauses = detect_clauses(text)
        risks = detect_risks(text)
        ai_analysis = gemini_analyze_contract(text)

        # 4. Return structured response
        return {
            "clauses": clauses,
            "entities": entities,
            "risks": risks,
            "ai_analysis": ai_analysis,
        }

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze uploaded contract",
        ) from exc
    finally:
        if file_path:
            FileHandler.delete_file(file_path)

# ============================================================================
# Info Endpoints
# ============================================================================
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Contract Analyzer API",
        "version": "1.0.0",
        "description": "Extract clauses and entities from contract PDFs",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Contract Analyzer API"
    }

# ============================================================================
# Development Server
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
