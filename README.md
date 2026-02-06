# DocVision AI - Intelligent OCR SaaS Platform

## Run with Docker
- Recommended for consistent environment
- Requirements: Docker and Docker Compose
- Steps:
  - Copy `.env.example` to `.env` and adjust values
  - Build and start:
    - `docker-compose up --build -d`
  - Health check:
    - `curl http://localhost:8000/api/health`
- The backend runs on `http://localhost:8000`
- Outputs are persisted to `./outputs` on the host

<p align="center">
  <a href="https://github.com/neeraj214/DocVision-AI-OCR-SaaS/stargazers"><img src="https://img.shields.io/github/stars/neeraj214/DocVision-AI-OCR-SaaS?style=social" alt="Stars"></a>
  <a href="https://github.com/neeraj214/DocVision-AI-OCR-SaaS/fork"><img src="https://img.shields.io/github/forks/neeraj214/DocVision-AI-OCR-SaaS?style=social" alt="Forks"></a>
  <a href="https://github.com/neeraj214/DocVision-AI-OCR-SaaS/actions"><img src="https://github.com/neeraj214/DocVision-AI-OCR-SaaS/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.x-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/TailwindCSS-3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind">
  <img src="https://img.shields.io/badge/OpenCV-4-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/EasyOCR-%20-FF6F00?style=for-the-badge" alt="EasyOCR">
</p>

<h1 align="center">🔎📄 DocVision AI – Intelligent OCR SaaS Platform 🤖</h1>

<p align="center">
  Modern OCR SaaS that turns images and scanned documents into clean, structured, machine‑readable text with an end‑to‑end AI pipeline.
</p>

<p align="center">
  <a href="#installation--setup">Install</a> •
  <a href="#api-endpoints">API</a> •
  <a href="#system-architecture">Architecture</a> •
  <a href="#folder-structure">Structure</a> •
  <a href="#sample-input--output">Samples</a> •
  <a href="#future-enhancements">Roadmap</a>
</p>

## Problem Statement
- Organizations handle diverse documents where raw OCR output is noisy and unstructured.
- Teams need reliable extraction, language handling, confidence scoring, and production‑ready delivery formats.
- Academic projects often stop at basic OCR; industry demands a scalable pipeline with web UI, APIs, and export features.

## Solution Overview
- Web app for image uploads with a FastAPI backend processing pipeline.
- OpenCV preprocessing improves OCR performance: denoise, grayscale, threshold, deskew.
- OCR via EasyOCR with Tesseract fallback for portability.
- NLP post‑processing cleans and structures text into lines and paragraphs.
- Outputs: text, structured JSON, and searchable PDF.
- Optional language detection and multilingual OCR support.

## Key Features
- 🖼️ Upload UI with language selection and instant results
- 🔠 CV preprocessing (denoise, grayscale, threshold, deskew)
- 🧠 OCR via EasyOCR with Tesseract fallback
- ✨ Text cleanup and paragraph structuring
- 📦 Export to .txt, .json, and generated searchable PDF
- 🌐 CORS‑enabled backend for local frontend dev

## System Architecture
- Frontend (React + Tailwind) sends images to backend.
- Backend (FastAPI) orchestrates CV preprocessing, OCR, and NLP post‑processing.
- Output artifacts are persisted to disk and exposed via static route.
- Optional detection picks language when none is provided.

```
+-----------------+        +-------------------+        +------------------+        +-------------------+
|  React Frontend | -----> |  FastAPI Router   | -----> |  AI Pipeline     | -----> |  Export & Storage |
|  Upload & View  |        |  /api/ocr, health |        |  Preprocess OCR  |        |  .txt .json .pdf  |
+-----------------+        +-------------------+        +------------------+        +-------------------+
                                 |                              |
                                 v                              v
                          CORS Middleware               Post‑processing (NLP)
```

## Tech Stack
- Frontend: React.js, Tailwind CSS, Vite, TypeScript
- Backend: Python, FastAPI
- AI/ML: OpenCV, EasyOCR, Tesseract (fallback), langdetect
- Evaluation: Custom CER/WER metrics (Levenshtein), pytest
- NLP: Lightweight regex heuristics; plug‑and‑play for spaCy/NLTK
- Export: reportlab (searchable PDF)
- Storage: Disk outputs; optional SQLite expansion

## 🧠 Phase 2A: Document Classification

The system now includes a CNN-based document classifier (ResNet18) to categorize documents into 4 types:
- Invoice
- Receipt
- Form
- Note

### 📁 Dataset Structure
Place training images in `datasets/doc_classification/train/{class_name}`.
Place validation images in `datasets/doc_classification/val/{class_name}`.

### 🚀 Training
To train the classifier:
```bash
python backend/app/ml/train_classifier.py --epochs 10
```
This will save `best_model.pth` and `classes.json` to `backend/app/ml/artifacts`.

### 📊 Evaluation
To evaluate the model:
```bash
python backend/app/ml/evaluate_classifier.py --model_path backend/app/ml/artifacts/best_model.pth
```

### 🔮 Inference API
Endpoint: `POST /api/ml/classify`
Input: Image file
Output:
```json
{
  "document_type": "invoice",
  "confidence": 0.98
}
```

## ML Evaluation System (OCR)
The project includes a comprehensive evaluation pipeline to measure OCR accuracy.

### Metrics
- **CER (Character Error Rate)**: `(S + D + I) / N` where S=substitutions, D=deletions, I=insertions, N=total characters.
- **WER (Word Error Rate)**: Similar to CER but operates on word tokens.

### Running Evaluation
1. **Prepare Dataset**:
   - Place images in `datasets/ocr_eval/images/`
   - Place corresponding ground truth text files in `datasets/ocr_eval/labels/` (filename must match image, e.g., `doc1.png` -> `doc1.txt`)
2. **Run CLI Tool**:
   ```bash
   python scripts/evaluate_ocr.py --dataset datasets/ocr_eval --output results.json
   ```
3. **Run Unit Tests**:
   ```bash
   pytest
   ```

## Folder Structure
```
DocVision-AI-OCR-SaaS/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ datasets/
│  ├─ ocr_eval/
│  └─ doc_classification/
├─ scripts/
│  ├─ evaluate_ocr.py
│  ├─ create_sample_dataset.py
│  └─ validate_classification_dataset.py
├─ backend/
│  └─ app/
│     ├─ main.py
│     ├─ core/
│     ├─ api/
│     │  └─ routes.py
│     ├─ ml/
│     │  ├─ models/
│     │  │  └─ cnn_classifier.py
│     │  ├─ train_classifier.py
│     │  ├─ evaluate_classifier.py
│     │  ├─ inference_classifier.py
│     │  ├─ utils.py
│     │  ├─ metrics.py
│     │  ├─ dataset_loader.py
│     │  └─ evaluate.py
│     ├─ schemas/
│     ├─ services/
│     ├─ utils/
│     ├─ output/            (runtime)
│     └─ tmp/               (runtime)
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.ts
│  ├─ index.html
│  └─ src/
│     ├─ main.tsx
│     ├─ App.tsx
│     └─ pages/
│        ├─ Home/
│        ├─ Upload/
│        └─ Results/
└─ docs/
   └─ (add design notes as needed)
```

## Screenshots & Demo
- UI Screenshot
  - ![Upload and Results](https://raw.githubusercontent.com/neeraj214/DocVision-AI-OCR-SaaS/main/docs/assets/ui-screenshot-1.png)
- Processing GIF
  - ![Processing Demo](https://raw.githubusercontent.com/neeraj214/DocVision-AI-OCR-SaaS/main/docs/assets/processing-demo.gif)
- Demo Video
  - https://youtu.be/xxxxxxxxxxx

## Installation & Setup
- ⚙️ Backend
  - Python 3.10+
  - Install Tesseract OCR engine (required for fallback): https://github.com/UB-Mannheim/tesseract/wiki
  - Install deps: `pip install -r requirements.txt`
  - Run: `uvicorn backend.app.main:app --reload --port 8000`
- 🎨 Frontend
  - Node.js 18+
  - In `frontend`: `npm install` then `npm run dev`
  - App runs at `http://localhost:5173`, backend at `http://localhost:8000`

## API Endpoints
- GET /api/health
  - Returns `{ "status": "ok" }`
- POST /api/ocr
  - FormData: `file` (PNG/JPG/JPEG)
  - Query: `lang` optional, default `en`
  - Response:
    ```
    {
      "text": "<cleaned_text>",
      "structured": { "paragraphs": [ { "lines": [...] }, ... ] },
      "confidence": 0.87,
      "language": "en",
      "pdf_url": "/outputs/<file>.pdf"
    }
```

## Sample Input / Output
- 📥 Input: A skewed, slightly noisy scanned image.
- 🧾 Output (text):
  ```
  Invoice 12345
  Date: 2026-01-01
  Total: $199.99
  ```
- 🗂️ Output (structured JSON):
  ```
  {
    "paragraphs": [
      { "lines": ["Invoice 12345", "Date: 2026-01-01", "Total: $199.99"] }
    ]
  }
  ```
- 📄 PDF: Generated searchable PDF available at the `pdf_url`.

## Future Enhancements
- 🗃️ Database persistence with job history, pagination, and RBAC
- ⏱️ Async job queue for batch OCR with WebSocket status
- 🧩 Layout analysis for tables, forms, and key‑value extraction
- 🧪 Model fine‑tuning and domain dictionaries for higher accuracy
- 🧬 spaCy pipelines for NER and structure enrichment
- ☁️ Cloud storage and CDN for output artifacts

## Why This Project Is Industry‑Relevant
- Mirrors production pipelines with preprocessing, OCR, NLP, and export layers.
- Clear separation of concerns and extensible architecture.
- Provides a functional UI, REST API, confidence scoring, and multi‑format outputs.
- Ready for deployment and portfolio demonstration with recruiter‑friendly code.

## Key Files
- Backend entry: [main.py](file:///c:/Users/neera/OneDrive/Documents/OCR-SAAS%20PROJECT/backend/app/main.py)
- API routes: [routes.py](file:///c:/Users/neera/OneDrive/Documents/OCR-SAAS%20PROJECT/backend/app/api/routes.py)
- OCR pipeline: [ocr_pipeline.py](file:///c:/Users/neera/OneDrive/Documents/OCR-SAAS%20PROJECT/backend/app/services/ocr_pipeline.py)
- Preprocessing: [preprocessing.py](file:///c:/Users/neera/OneDrive/Documents/OCR-SAAS%20PROJECT/backend/app/services/preprocessing.py)
- Post‑processing: [postprocessing.py](file:///c:/Users/neera/OneDrive/Documents/OCR-SAAS%20PROJECT/backend/app/services/postprocessing.py)
- PDF export: [pdf_utils.py](file:///c:/Users/neera/OneDrive/Documents/OCR-SAAS%20PROJECT/backend/app/utils/pdf_utils.py)
- Frontend App: [App.jsx](file:///c:/Users/neera/OneDrive/Documents/OCR-SAAS%20PROJECT/frontend/src/App.jsx)

## Running Locally
- Start backend: `uvicorn backend.app.main:app --reload --port 8000`
- Start frontend: `npm run dev` in `frontend`
- Upload an image and view outputs. Open the generated PDF via the button.
