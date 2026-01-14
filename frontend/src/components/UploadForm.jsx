import React, { useState } from 'react'
import axios from 'axios'

export default function UploadForm({ onResult }) {
  const [file, setFile] = useState(null)
  const [lang, setLang] = useState('en')
  const [loading, setLoading] = useState(false)
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    const form = new FormData()
    form.append('file', file)
    try {
      const res = await axios.post('http://localhost:8000/api/ocr?lang=' + lang, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      onResult(res.data)
    } catch (err) {
      onResult({ text: '', structured: null, confidence: 0, language: lang, pdf_url: '', error: 'Request failed' })
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h2 className="text-lg font-medium mb-4">Upload Document</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input type="file" accept="image/png,image/jpeg" onChange={(e) => setFile(e.target.files?.[0] || null)} className="block w-full text-sm" />
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-600">Language</label>
          <select value={lang} onChange={(e) => setLang(e.target.value)} className="border rounded px-2 py-1 text-sm">
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="fr">French</option>
            <option value="es">Spanish</option>
          </select>
        </div>
        <button type="submit" disabled={loading} className="bg-indigo-600 text-white px-4 py-2 rounded">
          {loading ? 'Processing...' : 'Extract Text'}
        </button>
      </form>
    </div>
  )
}

