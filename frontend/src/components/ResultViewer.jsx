import React from 'react'

export default function ResultViewer({ result }) {
  if (!result) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="text-lg font-medium mb-2">Results</h2>
        <p className="text-sm text-gray-500">Upload an image to see OCR output.</p>
      </div>
    )
  }
  const downloadText = () => {
    const blob = new Blob([result.text || ''], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'docvision-output.txt'
    a.click()
    URL.revokeObjectURL(url)
  }
  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(result.structured || {}, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'docvision-output.json'
    a.click()
    URL.revokeObjectURL(url)
  }
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h2 className="text-lg font-medium mb-4">Results</h2>
      <div className="space-y-3">
        <div className="text-sm text-gray-600">Language: <span className="font-mono">{result.language}</span></div>
        <div className="text-sm text-gray-600">Confidence: <span className="font-mono">{Number(result.confidence || 0).toFixed(2)}</span></div>
        <div className="flex gap-2">
          <button onClick={downloadText} className="border px-3 py-1 rounded text-sm">Download .txt</button>
          <button onClick={downloadJSON} className="border px-3 py-1 rounded text-sm">Download .json</button>
          {result.pdf_url ? (
            <a href={'http://localhost:8000' + result.pdf_url} target="_blank" rel="noreferrer" className="border px-3 py-1 rounded text-sm">Open PDF</a>
          ) : null}
        </div>
        <div className="border rounded p-3 h-96 overflow-auto">
          <pre className="whitespace-pre-wrap text-sm">{result.text || ''}</pre>
        </div>
      </div>
    </div>
  )
}

