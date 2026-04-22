import { useState } from 'react'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>📄 Contract Analyzer</h1>
        <p>Extract insights from contracts instantly</p>
      </header>
      <Dashboard />
    </div>
  )
}

export default App
