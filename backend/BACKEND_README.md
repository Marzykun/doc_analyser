# Contract Analyzer - Backend API

A powerful FastAPI backend for analyzing contract PDFs using natural language processing. Extracts clauses and entities automatically.

## Features

✨ **Core Features:**
- 📄 PDF file upload and processing
- 🔍 Clause detection (termination, payment, liability)
- 👥 Named entity extraction (PERSON, ORG, DATE, MONEY)
- ⚡ Fast text extraction using pdfplumber
- 🧠 NLP powered by spaCy
- 🛡️ Comprehensive error handling
- 📚 Auto-generated API documentation

## Technology Stack

- **FastAPI** - Modern web framework
- **Python 3.8+** - Programming language
- **pdfplumber** - PDF text extraction
- **spaCy** - Natural Language Processing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Quick Start

### 1. Setup Backend

```bash
cd backend

# Run setup script (recommended)
python setup.py

# Or manual setup:
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 2. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env as needed
# DEBUG=True
# PORT=8000
# FRONTEND_URL=http://localhost:5173
```

### 3. Start Server

```bash
python -m app.main
```

Server runs on `http://localhost:8000`

### 4. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /analyze

Analyze a contract PDF file.

**Request:**
- `file` (form-data, required): PDF file to analyze

**Response:**
```json
{
  "text": "Full extracted text from PDF...",
  "clauses": [
    {
      "type": "Termination",
      "text": "This agreement may be terminated by either party...",
      "confidence": 0.95
    },
    {
      "type": "Payment",
      "text": "Client agrees to pay $10,000 per month...",
      "confidence": 0.88
    }
  ],
  "entities": {
    "PERSON": ["John Smith", "Jane Doe"],
    "ORG": ["Acme Corp", "Tech Solutions Inc"],
    "DATE": ["2024-01-15", "2025-12-31"],
    "MONEY": ["$10,000", "$50,000 USD"]
  }
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid file or format
- `413` - File too large (>10MB)
- `500` - Server error

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -F "file=@contract.pdf"
```

**Example Python:**
```python
import requests

with open("contract.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/analyze", files=files)
    result = response.json()
    print(result)
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Contract Analyzer API"
}
```

### GET /

API information endpoint.

**Response:**
```json
{
  "name": "Contract Analyzer API",
  "version": "1.0.0",
  "description": "Extract clauses and entities from contract PDFs",
  "docs": "/docs"
}
```

## Clause Detection

The backend detects three main types of clauses:

### 1. **Termination Clauses**
Keywords: terminate, termination, cancel, discontinue, void, end of contract

Identifies when and how the contract can be ended.

### 2. **Payment Clauses**
Keywords: payment, fee, compensation, price, invoice, salary, royalty, billing

Identifies payment terms, amounts, and schedules.

### 3. **Liability Clauses**
Keywords: liable, liability, damages, indemnify, breach, insurance, hold harmless

Identifies responsibility and liability limitations.

## Entity Extraction

Uses spaCy NLP for accurate entity recognition:

- **PERSON**: Individual names (John Smith, Jane Doe)
- **ORG**: Organization names (Acme Corp, Tech Solutions)
- **DATE**: Important dates (2024-01-15, January 15, 2024)
- **MONEY**: Monetary amounts ($10,000, €5,000 USD)
- **GPE**: Geographic locations (New York, California)
- **PRODUCT**: Product/service names

## Project Structure

```
backend/
├── app/
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # FastAPI app, CORS, routes
│   ├── config.py                   # Configuration settings
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── contract.py             # Pydantic models
│   │                               #   - Clause
│   │                               #   - Entity
│   │                               #   - AnalysisResponse
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_handler.py         # PDF upload & storage
│   │   ├── text_extractor.py       # PDF → text (pdfplumber)
│   │   ├── clause_detector.py      # Clause detection (keywords)
│   │   ├── entity_extractor.py     # Entity extraction wrapper
│   │   └── nlp_service.py          # spaCy NLP wrapper
│   │
│   └── routes/
│       ├── __init__.py
│       └── contracts.py            # API endpoints
│
├── uploads/                        # Temporary file storage
├── setup.py                        # Setup script
├── requirements.txt                # Python dependencies
├── .env.example                    # Configuration template
├── .env                            # Configuration (local)
└── .gitignore
```

## File Descriptions

### `main.py`
FastAPI application initialization, CORS configuration, global error handling, and route inclusion.

### `config.py`
Configuration management using Pydantic. Loads settings from `.env` file.

### `models/contract.py`
Pydantic models for data validation:
- `Clause`: Single detected clause
- `Entity`: Grouped entities by type
- `AnalysisResponse`: API response structure

### `services/file_handler.py`
Handles PDF file uploads, validation, and cleanup.

### `services/text_extractor.py`
Extracts text from PDF using pdfplumber for accurate, fast extraction.

### `services/clause_detector.py`
Detects contract clauses using keyword matching. Configurable patterns and confidence scoring.

### `services/nlp_service.py`
Wrapper around spaCy for entity recognition. Handles model loading and entity grouping.

### `services/entity_extractor.py`
High-level entity extraction using spaCy NLP.

### `routes/contracts.py`
API endpoint definitions. Handles file validation, processing pipeline, and response formatting.

## Error Handling

The API includes comprehensive error handling:

| Scenario | Status | Message |
|----------|--------|---------|
| No file provided | 400 | Bad Request |
| Non-PDF file | 400 | Only PDF files are supported |
| File >10MB | 413 | File size exceeds maximum |
| Empty PDF | 400 | Could not extract text from PDF |
| Processing error | 500 | Internal server error |

## Configuration

Edit `.env` to customize:

```ini
# Server
DEBUG=True                          # Debug mode
HOST=0.0.0.0                       # Bind address
PORT=8000                          # Port

# CORS
FRONTEND_URL=http://localhost:5173 # Frontend URL for CORS

# Upload
MAX_UPLOAD_SIZE=10485760           # Max file size (10MB)

# NLP
SPACY_MODEL=en_core_web_sm         # spaCy model name
```

## Usage Examples

### Upload and Analyze

```python
import requests
import json

url = "http://localhost:8000/analyze"
files = {"file": open("contract.pdf", "rb")}

response = requests.post(url, files=files)
result = response.json()

# Print detected clauses
for clause in result["clauses"]:
    print(f"{clause['type']}: {clause['confidence']*100:.0f}%")
    print(f"  {clause['text']}\n")

# Print entities
for entity_type, entities in result["entities"].items():
    print(f"{entity_type}: {', '.join(entities)}")
```

### JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    body: formData
});

const result = await response.json();
console.log(result);
```

## Performance

- **Typical processing time**: 1-3 seconds per page
- **Max file size**: 10MB
- **Concurrent requests**: Unlimited (async)

## Troubleshooting

### spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### CORS errors
Check `FRONTEND_URL` in `.env` matches your frontend URL.

### File upload fails
- Check file size < 10MB
- Ensure file is valid PDF
- Check disk space in `uploads/` directory

### Slow processing
- Large PDFs take longer to process
- Consider breaking large PDFs into smaller files

## Development

### Run with auto-reload
```bash
python -m app.main
```

### Run tests
```bash
pytest
```

### Generate API docs
Visit `http://localhost:8000/docs`

## Deployment

### Docker
```bash
docker build -t contract-analyzer-backend .
docker run -p 8000:8000 contract-analyzer-backend
```

### Production
```bash
export DEBUG=False
export FRONTEND_URL=https://yourdomain.com
python -m app.main
```

## Future Enhancements

- [ ] Database integration for analysis history
- [ ] Advanced NLP models for better accuracy
- [ ] Custom clause definitions
- [ ] Batch processing API
- [ ] Webhook notifications
- [ ] Result caching
- [ ] Rate limiting
- [ ] Authentication/authorization

## License

MIT License

## Support

For issues or questions:
1. Check API documentation: `http://localhost:8000/docs`
2. Review this README
3. Check `.env` configuration
4. Verify spaCy model is installed
