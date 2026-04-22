import { useState } from 'react'
import { uploadContract } from '../services/api'

export default function FileUpload({ onAnalysisComplete, onLoading }) {
  const [file, setFile] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile)
        setError(null)
      } else {
        setError('Please upload a PDF or DOC file')
        setFile(null)
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return

    onLoading(true)
    try {
      const result = await uploadContract(file)
      onAnalysisComplete(result)
      setFile(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed')
    } finally {
      onLoading(false)
    }
  }

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit} className="upload-form">
        <label htmlFor="file-input" className="file-label">
          {file ? `Selected: ${file.name}` : 'Choose PDF or DOC'}
        </label>
        <input
          id="file-input"
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.doc,.docx"
          className="file-input"
        />
        <button type="submit" disabled={!file} className="analyze-btn">
          Analyze Contract
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  )
}
