# Contract Analyzer

A full-stack web application for analyzing contract documents. Upload PDF or DOC files to automatically extract clauses, entities, and key information.

## Features

- 📄 **PDF/DOC Upload**: Support for PDF and Word documents
- 🔍 **Clause Detection**: Automatically identifies termination, payment, liability, confidentiality, and warranty clauses
- 👥 **Entity Extraction**: Extracts names, dates, and monetary amounts
- 📝 **Text Preview**: View full extracted text from documents
- 🎨 **Modern UI**: React-based frontend with responsive design
- ⚡ **Fast API**: Python FastAPI backend for processing

## Project Structure

```
contract_analyzer/
├── frontend/                 # React + Vite application
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client services
│   │   └── styles/          # CSS styling
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── models/          # Pydantic data models
│   │   ├── services/        # Business logic services
│   │   ├── routes/          # API endpoints
│   │   ├── main.py          # FastAPI app initialization
│   │   └── config.py        # Configuration settings
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment variables template
│
└── docker-compose.yml       # Docker compose configuration
```

## Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling

### Backend
- **FastAPI** - Web framework
- **Python 3.8+** - Language
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX text extraction
- **NLTK/spaCy** - NLP utilities
- **Pydantic** - Data validation

## Setup & Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Virtual environment tool (venv or conda)

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173`

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```
Backend runs on `http://localhost:8000`

API docs available at `http://localhost:8000/docs`

### Using Docker Compose
```bash
docker-compose up -d
```

## API Endpoints

### POST /api/contracts/analyze
Upload and analyze a contract file.

**Request:**
- `file`: PDF or DOCX file (multipart/form-data)

**Response:**
```json
{
  "text": "extracted text...",
  "clauses": [
    {
      "type": "Termination",
      "text": "clause text...",
      "confidence": 0.95
    }
  ],
  "entities": {
    "names": ["John Doe", "Acme Corp"],
    "dates": ["2024-01-15", "2025-12-31"],
    "amounts": ["$10,000", "$5,000 USD"]
  }
}
```

### GET /api/contracts/health
Health check endpoint.

## File Descriptions

### Frontend Files
- **FileUpload.jsx**: File selection and upload component
- **ResultsDisplay.jsx**: Results presentation component
- **ClauseHighlight.jsx**: Clause display with confidence scoring
- **Dashboard.jsx**: Main page layout
- **api.js**: API communication service
- **App.jsx**: Main app component

### Backend Files
- **main.py**: FastAPI app initialization and routes
- **config.py**: Configuration and settings
- **contract.py**: Pydantic models (Clause, Entity, AnalysisResponse)
- **file_handler.py**: File upload and storage handling
- **text_extractor.py**: PDF/DOC text extraction
- **clause_detector.py**: Clause detection logic
- **entity_extractor.py**: Entity extraction (names, dates, amounts)

## Configuration

Create `.env` in the backend directory:
```
DEBUG=True
HOST=0.0.0.0
PORT=8000
FRONTEND_URL=http://localhost:5173
MAX_UPLOAD_SIZE=10485760
SPACY_MODEL=en_core_web_sm
```

## Future Enhancements

- [ ] Database integration for analysis history
- [ ] Advanced NLP with spaCy for better entity extraction
- [ ] User authentication and account management
- [ ] Batch file processing
- [ ] Custom clause definitions
- [ ] Export results (PDF, JSON, CSV)
- [ ] Multi-language support
- [ ] Machine learning model for clause classification

## License

MIT License
