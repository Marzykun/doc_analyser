# API Usage Examples

Complete examples for using the Contract Analyzer API.

## Quick Test

### Using cURL

```bash
# Test file upload
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -F "file=@contract.pdf"
```

### Health Check

```bash
curl http://localhost:8000/health
```

---

## Python Examples

### Basic Usage

```python
import requests
import json

# Analyze a contract
url = "http://localhost:8000/analyze"
files = {"file": open("contract.pdf", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(json.dumps(result, indent=2))
```

### Process and Display Results

```python
import requests

def analyze_contract(pdf_path):
    """Analyze a contract PDF and display results"""
    
    url = "http://localhost:8000/analyze"
    
    with open(pdf_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
        return
    
    result = response.json()
    
    # Display clauses
    print("=" * 60)
    print("DETECTED CLAUSES")
    print("=" * 60)
    
    for clause in result["clauses"]:
        confidence = clause["confidence"] * 100
        print(f"\n[{clause['type']}] Confidence: {confidence:.0f}%")
        print(f"Text: {clause['text'][:150]}...")
    
    # Display entities
    print("\n" + "=" * 60)
    print("EXTRACTED ENTITIES")
    print("=" * 60)
    
    entities = result["entities"]
    for entity_type, values in entities.items():
        if values:
            print(f"\n{entity_type}:")
            for value in values:
                print(f"  • {value}")
    
    # Display extracted text length
    print("\n" + "=" * 60)
    print(f"Total text extracted: {len(result['text'])} characters")
    print("=" * 60)

# Usage
if __name__ == "__main__":
    analyze_contract("contract.pdf")
```

### Batch Processing

```python
import requests
from pathlib import Path

def batch_analyze(pdf_directory):
    """Analyze multiple contracts"""
    
    pdf_dir = Path(pdf_directory)
    results = {}
    
    for pdf_file in pdf_dir.glob("*.pdf"):
        print(f"Processing {pdf_file.name}...")
        
        url = "http://localhost:8000/analyze"
        with open(pdf_file, "rb") as f:
            response = requests.post(url, files={"file": f})
        
        if response.status_code == 200:
            results[pdf_file.name] = response.json()
            print(f"  ✓ Success - Found {len(response.json()['clauses'])} clauses")
        else:
            results[pdf_file.name] = {"error": response.status_code}
            print(f"  ✗ Failed - Status {response.status_code}")
    
    return results

# Usage
if __name__ == "__main__":
    results = batch_analyze("./contracts")
    
    # Summary
    print("\nBatch Processing Summary:")
    for filename, result in results.items():
        if "error" not in result:
            clause_count = len(result.get("clauses", []))
            entity_count = sum(len(v) for v in result.get("entities", {}).values())
            print(f"{filename}: {clause_count} clauses, {entity_count} entities")
```

### Error Handling

```python
import requests
from requests.exceptions import RequestException

def safe_analyze(pdf_path):
    """Analyze with proper error handling"""
    
    try:
        # Validate file
        if not pdf_path.endswith(".pdf"):
            print("Error: File must be PDF")
            return None
        
        if not Path(pdf_path).exists():
            print("Error: File not found")
            return None
        
        file_size_mb = Path(pdf_path).stat().st_size / (1024 * 1024)
        if file_size_mb > 10:
            print("Error: File too large (>10MB)")
            return None
        
        # Upload and analyze
        url = "http://localhost:8000/analyze"
        with open(pdf_path, "rb") as f:
            response = requests.post(url, files={"file": f}, timeout=30)
        
        # Handle response
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            print("Error: Invalid request")
            print(response.json()["detail"])
        elif response.status_code == 413:
            print("Error: File too large")
        elif response.status_code == 500:
            print("Error: Server error")
        else:
            print(f"Error: {response.status_code}")
        
        return None
    
    except RequestException as e:
        print(f"Connection error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage
from pathlib import Path

if __name__ == "__main__":
    result = safe_analyze("contract.pdf")
    if result:
        print("Analysis successful!")
        print(f"Clauses: {len(result['clauses'])}")
        print(f"Entities: {sum(len(v) for v in result['entities'].values())}")
```

---

## JavaScript / Node.js Examples

### Basic Usage

```javascript
async function analyzeContract(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log(result);
        return result;
    } catch (error) {
        console.error('Error:', error);
    }
}

// Usage
const fileInput = document.getElementById('pdfInput');
fileInput.addEventListener('change', (e) => {
    analyzeContract(e.target.files[0]);
});
```

### Display Results

```javascript
function displayResults(result) {
    // Display clauses
    const clausesDiv = document.getElementById('clauses');
    clausesDiv.innerHTML = '<h2>Detected Clauses</h2>';
    
    result.clauses.forEach(clause => {
        const confidence = (clause.confidence * 100).toFixed(0);
        const clauseEl = document.createElement('div');
        clauseEl.className = 'clause-item';
        clauseEl.innerHTML = `
            <h3>${clause.type}</h3>
            <p class="text">${clause.text}</p>
            <p class="confidence">Confidence: ${confidence}%</p>
        `;
        clausesDiv.appendChild(clauseEl);
    });
    
    // Display entities
    const entitiesDiv = document.getElementById('entities');
    entitiesDiv.innerHTML = '<h2>Extracted Entities</h2>';
    
    Object.entries(result.entities).forEach(([type, values]) => {
        if (values.length > 0) {
            const section = document.createElement('div');
            section.innerHTML = `
                <h3>${type}</h3>
                <ul>
                    ${values.map(v => `<li>${v}</li>`).join('')}
                </ul>
            `;
            entitiesDiv.appendChild(section);
        }
    });
}
```

### Fetch with Progress

```javascript
async function analyzeWithProgress(file, onProgress) {
    const formData = new FormData();
    formData.append('file', file);
    
    const xhr = new XMLHttpRequest();
    
    // Progress handler
    xhr.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            onProgress(percentComplete);
        }
    });
    
    return new Promise((resolve, reject) => {
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
            } else {
                reject(new Error(`HTTP ${xhr.status}`));
            }
        });
        
        xhr.addEventListener('error', () => reject(new Error('Upload failed')));
        
        xhr.open('POST', 'http://localhost:8000/analyze');
        xhr.send(formData);
    });
}

// Usage
analyzeWithProgress(file, (progress) => {
    console.log(`Upload progress: ${progress.toFixed(0)}%`);
}).then(result => {
    console.log('Analysis complete:', result);
}).catch(error => {
    console.error('Error:', error);
});
```

---

## Example Responses

### Success Response (200)

```json
{
  "text": "This Service Agreement (\"Agreement\") is entered into as of January 15, 2024, by and between Acme Corporation, a Delaware corporation (\"Provider\") and Tech Solutions Inc., a New York corporation (\"Client\").\n\n1. TERMINATION\nThis Agreement may be terminated by either party upon thirty (30) days written notice...",
  "clauses": [
    {
      "type": "Termination",
      "text": "This Agreement may be terminated by either party upon thirty (30) days written notice.",
      "confidence": 0.95
    },
    {
      "type": "Payment",
      "text": "Client shall pay Provider a monthly fee of $10,000 for the services provided under this Agreement.",
      "confidence": 0.92
    },
    {
      "type": "Liability",
      "text": "Neither party shall be liable for indirect, incidental, or consequential damages arising from this Agreement.",
      "confidence": 0.88
    }
  ],
  "entities": {
    "PERSON": ["John Smith", "Jane Doe"],
    "ORG": ["Acme Corporation", "Tech Solutions Inc"],
    "DATE": ["January 15, 2024", "2025-01-14"],
    "MONEY": ["$10,000", "$50,000"]
  }
}
```

### Error Response (400)

```json
{
  "detail": "Only PDF files are supported"
}
```

### Error Response (413)

```json
{
  "detail": "File size exceeds maximum allowed (10MB)"
}
```

---

## Testing with Postman

### Setup

1. Open Postman
2. Create new Request
3. Method: `POST`
4. URL: `http://localhost:8000/analyze`
5. Body: 
   - Type: `form-data`
   - Key: `file`
   - Value: Select your PDF file

### Run

1. Click "Send"
2. View response in below panel

---

## Performance Tips

1. **File size**: Keep PDFs under 10MB for best performance
2. **Concurrent requests**: API handles multiple requests simultaneously
3. **Large batches**: Process in chunks of 5-10 files
4. **Connection timeout**: Set to 30+ seconds for large files

---

## Integration Checklist

- [ ] Backend running on `http://localhost:8000`
- [ ] spaCy model installed (`python -m spacy download en_core_web_sm`)
- [ ] Test endpoint with simple PDF
- [ ] Verify CORS configuration for frontend
- [ ] Handle error responses in client code
- [ ] Implement progress indication for uploads
- [ ] Cache results if needed
- [ ] Set appropriate timeouts (30+ seconds)
