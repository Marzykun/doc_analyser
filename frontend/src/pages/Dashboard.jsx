import { useState } from 'react'
import FileUpload from '../components/FileUpload'
import ResultsDisplay from '../components/ResultsDisplay'

export default function Dashboard() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <main className="dashboard">
      <div className="dashboard-layout">
        <div className="upload-section">
          <FileUpload 
            onAnalysisComplete={setAnalysisResult}
            onLoading={setLoading}
          />
          {loading && <p className="loading">Analyzing contract...</p>}
        </div>

        {analysisResult && (
          <div className="results-section">
            <ResultsDisplay data={analysisResult} />
          </div>
        )}
      </div>
    </main>
  )
}
