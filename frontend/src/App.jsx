import React, { useState } from 'react'
import UploadForm from './components/UploadForm.jsx'
import ResultViewer from './components/ResultViewer.jsx'

export default function App() {
  const [result, setResult] = useState(null)
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-semibold">DocVision AI</h1>
          <span className="text-sm text-gray-500">Intelligent OCR SaaS</span>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <UploadForm onResult={setResult} />
        <ResultViewer result={result} />
      </main>
      <footer className="text-center text-xs text-gray-500 py-6">
        © {new Date().getFullYear()} DocVision AI
      </footer>
    </div>
  )
}

